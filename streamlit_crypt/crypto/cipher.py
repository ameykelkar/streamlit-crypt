import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305

def encrypt_bytes(
    plaintext: bytes,
    key: bytes,
    algorithm: str = "AESGCM",
    aad: bytes = None
) -> bytes:
    """Encrypt bytes payload with AEAD cipher and return nonce + ciphertext."""
    if algorithm == "AESGCM":
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)
        ct = aesgcm.encrypt(nonce, plaintext, aad)
    elif algorithm == "ChaCha20Poly1305":
        chacha = ChaCha20Poly1305(key)
        nonce = os.urandom(12)
        ct = chacha.encrypt(nonce, plaintext, aad)
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
    return nonce + ct

def decrypt_bytes(
    ciphertext: bytes,
    key: bytes,
    algorithm: str = "AESGCM",
    aad: bytes = None
) -> bytes:
    """Decrypt ciphertext and return plaintext."""
    if len(ciphertext) < 12:
        raise ValueError("Ciphertext too short to contain nonce.")
    nonce, ct = ciphertext[:12], ciphertext[12:]
    if algorithm == "AESGCM":
        aesgcm = AESGCM(key)
        return aesgcm.decrypt(nonce, ct, aad)
    elif algorithm == "ChaCha20Poly1305":
        chacha = ChaCha20Poly1305(key)
        return chacha.decrypt(nonce, ct, aad)
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
