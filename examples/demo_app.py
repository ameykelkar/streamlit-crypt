import time
import streamlit as st
from streamlit_crypt.crypto.wrappers import (
    encrypt_text, decrypt_text,
    encrypt_json, decrypt_json
)
from streamlit_crypt.streamlit_component import (
    get_key, encrypt_uploader, decrypt_uploader
)

st.set_page_config(page_title="🔒 Streamlit Crypt Demo", layout="wide")
st.title("🔒 Streamlit Crypt 🎉")
st.markdown("Simple two-tab UI for encryption and decryption.")

# Create two tabs: Encrypt and Decrypt
tab_encrypt, tab_decrypt = st.tabs(["Encrypt", "Decrypt"])

with tab_encrypt:
    st.header("🔐 Encrypt")
    enc_algo = st.selectbox("Algorithm", ["AESGCM", "ChaCha20Poly1305"], key="enc_algo")
    enc_mode = st.radio("Mode", ["Text", "JSON", "File"], key="enc_mode")
    enc_key = get_key(enc_algo)

    if enc_mode == "Text":
        plaintext = st.text_area("Enter message", placeholder="Type something secret…")
        if st.button("Encrypt Text") and plaintext:
            with st.spinner("Encrypting…"):
                ciphertext = encrypt_text(plaintext, enc_key)
            st.download_button("Download ciphertext", ciphertext, file_name="message.enc")

    elif enc_mode == "JSON":
        sample = {"user": "alice", "amount": 42}
        st.json(sample)
        if st.button("Encrypt JSON"):
            with st.spinner("Encrypting…"):
                ciphertext = encrypt_json(sample, enc_key)
            st.download_button("Download JSON cipher", ciphertext, file_name="data.enc")

    else:  # File
        upload = st.file_uploader("Upload file to encrypt", key="enc_file")
        if upload and st.button("Encrypt File"):
            with st.spinner("Encrypting file…"):
                ciphertext = encrypt_uploader(upload, enc_key, algorithm=enc_algo)
            st.download_button(
                "Download encrypted file", ciphertext,
                file_name=f"{upload.name}.enc"
            )

with tab_decrypt:
    st.header("🔓 Decrypt")
    dec_algo = st.selectbox("Algorithm", ["AESGCM", "ChaCha20Poly1305"], key="dec_algo")
    dec_mode = st.radio("Mode", ["Text", "JSON", "File"], key="dec_mode")
    dec_key = get_key(dec_algo)

    if dec_mode == "Text":
        uploaded_ct = st.file_uploader("Upload ciphertext (.enc)", type=["enc"], key="dec_text")
        if uploaded_ct and st.button("Decrypt Text", key="btn_dec_text"):
            with st.spinner("Decrypting…"):
                plaintext = decrypt_text(uploaded_ct.getvalue(), dec_key)
            if isinstance(plaintext, (bytes, bytearray)):
                plaintext = plaintext.decode("utf-8")
            st.code(plaintext)

    elif dec_mode == "JSON":
        uploaded_ct = st.file_uploader("Upload JSON cipher (.enc)", type=["enc"], key="dec_json")
        if uploaded_ct and st.button("Decrypt JSON", key="btn_dec_json"):
            with st.spinner("Decrypting…"):
                obj = decrypt_json(uploaded_ct.getvalue(), dec_key)
            st.json(obj)

    else:  # File
        uploaded_ct = st.file_uploader("Upload encrypted file (.enc)", type=["enc"], key="dec_file")
        if uploaded_ct and st.button("Decrypt File", key="btn_dec_file"):
            with st.spinner("Decrypting file…"):
                plaintext = decrypt_uploader(uploaded_ct, dec_key, algorithm=dec_algo)
            st.download_button(
                "Download decrypted file", plaintext,
                file_name=uploaded_ct.name.replace(".enc", ".dec")
            )
