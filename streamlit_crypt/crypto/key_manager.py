import os
import toml
from base64 import urlsafe_b64encode, urlsafe_b64decode
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

SECRETS_PATH = os.path.join(
    os.getcwd(),
    ".streamlit", "secrets.toml"
)

def generate_key(algorithm: str = "AESGCM") -> bytes:
    """Generate a new symmetric key for the specified algorithm."""
    if algorithm == "AESGCM":
        return AESGCM.generate_key(bit_length=256)
    elif algorithm == "ChaCha20Poly1305":
        return ChaCha20Poly1305.generate_key()
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

def save_key_to_secrets(key: bytes, name: str = "streamlit_crypt_key"):
    """Save key under `name` in .streamlit/secrets.toml."""
    os.makedirs(os.path.dirname(SECRETS_PATH), exist_ok=True)
    try:
        with open(SECRETS_PATH, 'r') as f:
            data = toml.load(f)
    except (FileNotFoundError, toml.TomlDecodeError):
        data = {}
    b64key = urlsafe_b64encode(key).decode()
    data[name] = b64key
    with open(SECRETS_PATH, 'w') as f:
        toml.dump(data, f)

def load_key_from_secrets(name: str = "streamlit_crypt_key") -> bytes:
    """Load key from .streamlit/secrets.toml by `name`."""
    try:
        with open(SECRETS_PATH, 'r') as f:
            data = toml.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Secrets file not found at {SECRETS_PATH}")
    if name not in data:
        raise KeyError(f"Key '{name}' not found in secrets.")
    b64key = data[name]
    return urlsafe_b64decode(b64key)

def derive_key_from_passphrase(passphrase: str, salt: bytes = None) -> bytes:
    """Derive a strong key from a passphrase using PBKDF2-HMAC-SHA256.
    Returns salt||key, where salt is 16 bytes and key is 32 bytes.
    """
    if salt is None:
        salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    key = kdf.derive(passphrase.encode('utf-8'))
    return salt + key
