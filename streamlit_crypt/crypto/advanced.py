import hmac
from hashlib import sha256
from .key_manager import load_key_from_secrets, generate_key, save_key_to_secrets

def rotate_key(name: str = "streamlit_crypt_key"):
    """Rotate the key in secrets.toml and return the new key."""
    new_key = generate_key()
    save_key_to_secrets(new_key, name)
    return new_key

def sign_data(data: bytes, key: bytes) -> bytes:
    """Compute HMAC-SHA256 of data for non-repudiation."""
    return hmac.new(key, data, sha256).digest()

def verify_signature(data: bytes, signature: bytes, key: bytes) -> bool:
    """Verify HMAC-SHA256 signature."""
    expected = hmac.new(key, data, sha256).digest()
    return hmac.compare_digest(expected, signature)

def encrypt_with_kms(data: bytes, kms_client, key_id: str) -> bytes:
    raise NotImplementedError("KMS integration not implemented.")

def decrypt_with_kms(cipher: bytes, kms_client) -> bytes:
    raise NotImplementedError("KMS integration not implemented.")
