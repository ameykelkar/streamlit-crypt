import io
import json
import pickle
from .cipher import encrypt_bytes, decrypt_bytes

def encrypt_file(src_path: str, dst_path: str, key: bytes):
    """Encrypt entire file and write to destination."""
    with open(src_path, 'rb') as f:
        data = f.read()
    ct = encrypt_bytes(data, key)
    with open(dst_path, 'wb') as f:
        f.write(ct)

def decrypt_file(src_path: str, dst_path: str, key: bytes):
    """Decrypt entire file and write plaintext to destination."""
    with open(src_path, 'rb') as f:
        ct = f.read()
    pt = decrypt_bytes(ct, key)
    with open(dst_path, 'wb') as f:
        f.write(pt)

def encrypt_text(text: str, key: bytes, encoding: str = "utf-8") -> bytes:
    """Encrypt a text string."""
    return encrypt_bytes(text.encode(encoding), key)

def decrypt_text(cipher: bytes, key: bytes, encoding: str = "utf-8") -> str:
    """Decrypt to a text string."""
    plain = decrypt_bytes(cipher, key)
    return plain.decode(encoding)

def encrypt_json(data: dict, key: bytes) -> bytes:
    """Serialize JSON and encrypt."""
    raw = json.dumps(data).encode('utf-8')
    return encrypt_bytes(raw, key)

def decrypt_json(cipher: bytes, key: bytes) -> dict:
    """Decrypt and parse JSON."""
    raw = decrypt_bytes(cipher, key)
    return json.loads(raw.decode('utf-8'))
