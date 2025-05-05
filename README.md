# 🎉 streamlit-crypt

[![PyPI Version](https://img.shields.io/pypi/v/streamlit-crypt)](https://pypi.org/project/streamlit-crypt) [![Python Versions](https://img.shields.io/pypi/pyversions/streamlit-crypt)](https://pypi.org/project/streamlit-crypt) [![License](https://img.shields.io/pypi/l/streamlit-crypt)](LICENSE)

A **fun**, **easy-to-use** Streamlit addon that brings modern cryptography to your apps! Encrypt files, text, JSON, and more in just a few lines of code. Perfect for demos, side projects, or even production prototypes.

---

## 🚀 Features

- **AEAD Encryption:** AES-GCM & ChaCha20-Poly1305 with built-in integrity checks  
- **Key Management:** Automatic key generation & secure storage in `secrets.toml`  
- **Passphrase KDF:** Derive keys from memorable passwords via PBKDF2-HMAC-SHA256  
- **Serializers & Wrappers:**
  - Text, JSON, Python objects (pickle)
  - Files & streams
  - (Optionally) NumPy arrays, pandas DataFrames, images & archives
- **Advanced Tools:**  
  <details>
  <summary>Click to expand</summary>

  - Key rotation & versioning
  - HMAC-SHA256 signing & verification
  - (Planned) KMS integration (AWS/GCP/Azure)
  - Secure in-memory zeroization & shredding helpers

  </details>

---

## 💿 Installation

Install via **Poetry** or **pip**:

<details>
<summary>Poetry</summary>

```bash
poetry add streamlit-crypt
```
</details>

<details>
<summary>pip</summary>

```bash
pip install streamlit-crypt
```
</details>

---

## 🎬 Quickstart

1. **Import & initialize**:

   ```python
   import streamlit as st
   from streamlit_crypt import get_key, encrypt_uploader, decrypt_uploader

   # Auto-load or generate your key
   key = get_key()
   ```

2. **Encrypt a file**:

   ```python
   uploaded = st.file_uploader("Choose a file to encrypt")
   if uploaded:
       cipher = encrypt_uploader(uploaded, key)
       st.download_button("Download 🔐", cipher, file_name=uploaded.name + ".enc")
   ```

3. **Decrypt**:

   ```python
   uploaded_enc = st.file_uploader("Upload encrypted file")
   if uploaded_enc:
       plain = decrypt_uploader(uploaded_enc, key)
       st.download_button("Download 🔓", plain, file_name=uploaded_enc.name.replace('.enc','.dec'))
   ```

Try it yourself—**no config** required beyond a couple of imports! 🎈

---

## 🛠️ Detailed Usage

### Key Management

```python
from streamlit_crypt import generate_key, save_key_to_secrets, load_key_from_secrets

# Generate & store
key = generate_key("ChaCha20Poly1305")
save_key_to_secrets(key, name="my_app_key")

# Later…
key = load_key_from_secrets(name="my_app_key")
```

### Text & JSON

```python
from streamlit_crypt import encrypt_text, decrypt_text, encrypt_json, decrypt_json

cipher = encrypt_text("Hello, world!", key)
plain  = decrypt_text(cipher, key)

obj     = {"foo": "bar"}
cipher2 = encrypt_json(obj, key)
plain2  = decrypt_json(cipher2, key)
```

<details>
<summary>More wrappers: Files, pickle, NumPy, pandas, images…</summary>

Simply call `encrypt_file`, `decrypt_file`, or use serializers from `crypto/wrappers.py`!

</details>

---

## 🎨 Demo App

Check out the **interactive demo** in `examples/demo_app.py`:

```bash
streamlit run examples/demo_app.py
```

It showcases spinners, progress bars, balloons, and more—encryption has never been this fun! 🎉

---

## 🤝 Contributing

We ❤️ contributions! To get started:

1. Fork this repo & create a feature branch.
2. Install dev dependencies:
   ```bash
   poetry install
   pre-commit install
   ```
3. Write code & tests (pytest + Hypothesis).
4. Format with **Black** & check lints:
   ```bash
   black . && isort . && flake8 && mypy
   ```
5. Open a PR & enjoy the 🎵 of CI passing!

<details>
<summary>Type of contributions</summary>

- Bug fixes 🐛
- New encryption algorithms 🛡️
- KMS integration ☁️
- Improved serializers or UI components 📦
- Docs, demos, and examples 📚

</details>

---

## 📜 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for more information.

---

> Built with ❤️ by the **streamlit-crypt** community. Let's make encryption **fun** and **accessible**! 🎊
