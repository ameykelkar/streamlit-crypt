import streamlit as st
from .crypto.key_manager import load_key_from_secrets, generate_key, save_key_to_secrets
from .crypto.cipher import encrypt_bytes, decrypt_bytes

def get_key(algorithm: str = "AESGCM") -> bytes:
    """Retrieve or generate a symmetric key, persisted in Streamlit secrets."""
    try:
        return load_key_from_secrets()
    except Exception:
        key = generate_key(algorithm)
        save_key_to_secrets(key)
        return key

def encrypt_uploader(uploader, key: bytes, algorithm: str = "AESGCM") -> bytes:
    """Encrypt a file uploaded via Streamlit's uploader widget."""
    data = uploader.getvalue()
    return encrypt_bytes(data, key, algorithm)

def decrypt_uploader(uploader, key: bytes, algorithm: str = "AESGCM") -> bytes:
    """Decrypt a file uploaded via Streamlit's uploader widget."""
    data = uploader.getvalue()
    return decrypt_bytes(data, key, algorithm)

def main_ui():
    """Define Streamlit UI for encryption/decryption workflows."""
    st.title("🔒 Streamlit Crypt")
    algorithm = st.selectbox("Algorithm", ["AESGCM", "ChaCha20Poly1305"])
    action = st.radio("Action", ["Encrypt", "Decrypt"])
    key = get_key(algorithm)

    uploaded = st.file_uploader("Upload file")
    if uploaded:
        try:
            if action == "Encrypt":
                result = encrypt_uploader(uploaded, key, algorithm)
                st.download_button(
                    "Download Encrypted", result,
                    file_name=uploaded.name + ".enc"
                )
            else:
                plain = decrypt_uploader(uploaded, key, algorithm)
                st.download_button(
                    "Download Decrypted", plain,
                    file_name=uploaded.name + ".dec"
                )
        except Exception as e:
            st.error(f"{action}ion failed: {e}")

if __name__ == '__main__':
    main_ui()
