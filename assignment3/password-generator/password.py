import streamlit as st
import random
import string

def generate_password(length, use_digits, use_special_chars):
    charactors = string.ascii_letters

    if use_digits:
        charactors += string.digits

    if use_special_chars:
        charactors += string.punctuation

    return ''.join(random.choice(charactors) for _ in range(length))

st.title("Password Generator")

length = st.slider("Select Password Length", min_value=6, max_value=32, value=12)

use_digits = st.checkbox("Include Digits")

use_special_chars = st.checkbox("Include Special Characters")

if st.button("Generate Password"):
    password = generate_password(length, use_digits, use_special_chars)
    st.write(f"Generated Password: `{password}`")

st.write("--------------------------------")

st.write("Build with 💖 by [Kiran Ahmed](https://github.com/KIRANAHMED)")
    