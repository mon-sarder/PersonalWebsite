"""
Rate limiting middleware to prevent API abuse
"""

from flask import request, jsonify
from functools import wraps
from datetime import datetime, timedelta
from collections import defaultdict
import threading

# In-memory storage for rate limiting (use Redis in production)
rate_limit_storage = defaultdict(list)
storage_lock = threading.Lock()


def rate_limit(max_requests=10, window_seconds=60):
    """
    Rate limiting decorator
    Usage: @rate_limit(max_requests=5, window_seconds=60)
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get client identifier (IP address)
            client_id = request.remote_addr

            # Get current time
            now = datetime.utcnow()
            window_start = now - timedelta(seconds=window_seconds)

            with storage_lock:
                # Clean old entries
                rate_limit_storage[client_id] = [
                    timestamp for timestamp in rate_limit_storage[client_id]
                    if timestamp > window_start
                ]

                # Check if limit exceeded
                if len(rate_limit_storage[client_id]) >= max_requests:
                    return jsonify({
                        "error": "Rate limit exceeded. Please try again later."
                    }), 429

                # Add current request
                rate_limit_storage[client_id].append(now)

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def cleanup_rate_limits():
    """Cleanup old rate limit entries (run periodically)"""
    with storage_lock:
        now = datetime.utcnow()
        for client_id in list(rate_limit_storage.keys()):
            # Remove entries older than 1 hour
            cutoff = now - timedelta(hours=1)
            rate_limit_storage[client_id] = [
                timestamp for timestamp in rate_limit_storage[client_id]
                if timestamp > cutoff
            ]

            # Remove client if no entries
            if not rate_limit_storage[client_id]:
                del rate_limit_storage[client_id]