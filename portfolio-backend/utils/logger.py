"""
Logging utilities for Flask application
"""

import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logging(app):
    """
    Setup logging for Flask application
    Args:
        app: Flask application instance
    Returns:
        logging.Logger: Configured logger
    """
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create rotating file handler
    file_handler = RotatingFileHandler(
        'logs/portfolio_api.log',
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(logging.DEBUG)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Add formatter to handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


class RequestLogger:
    """Class to log HTTP requests and responses"""

    def __init__(self, app):
        self.app = app
        self.logger = logging.getLogger(__name__)

    def log_request(self):
        """Log incoming request details"""
        try:
            from flask import request
            self.logger.info(
                f"Request: {request.method} {request.path} - "
                f"Remote: {request.remote_addr}"
            )
        except Exception as e:
            self.logger.error(f"Error logging request: {e}")

    def log_response(self, response):
        """Log response details"""
        try:
            from flask import request
            self.logger.info(
                f"Response: {request.method} {request.path} - "
                f"Status: {response.status_code}"
            )
        except Exception as e:
            self.logger.error(f"Error logging response: {e}")