# utils.py
import hashlib
import os
import base64

# Configuration
HASH_NAME = "sha256"
ITERATIONS = 100_000
SALT_SIZE = 16  # 128-bit salt

def hash_password(password: str) -> str:
    salt = os.urandom(SALT_SIZE)
    hash_bytes = hashlib.pbkdf2_hmac(
        HASH_NAME, password.encode('utf-8'), salt, ITERATIONS
    )
    return base64.b64encode(salt + hash_bytes).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    decoded = base64.b64decode(hashed)
    salt = decoded[:SALT_SIZE]
    original_hash = decoded[SALT_SIZE:]
    new_hash = hashlib.pbkdf2_hmac(
        HASH_NAME, password.encode('utf-8'), salt, ITERATIONS
    )
    return new_hash == original_hash
