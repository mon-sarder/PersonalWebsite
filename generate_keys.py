#!/usr/bin/env python3
"""
Generate secure keys for .env file
Run this script and copy the output into your .env file
"""

import secrets

print("=" * 60)
print("🔐 Secure Key Generator for .env File")
print("=" * 60)
print()

print("Copy these values into your .env file:")
print()

# Generate SECRET_KEY
secret_key = secrets.token_hex(32)
print("SECRET_KEY:")
print(f"  {secret_key}")
print()

# Generate SETUP_KEY
setup_key = secrets.token_urlsafe(32)
print("SETUP_KEY:")
print(f"  {setup_key}")
print()

print("=" * 60)
print("✅ Keys generated successfully!")
print()
print("Add these to your portfolio-backend/.env file:")
print()
print(f"SECRET_KEY={secret_key}")
print(f"SETUP_KEY={setup_key}")
print()
print("=" * 60)