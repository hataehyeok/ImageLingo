import streamlit as st
import base64

def add_bg_image_from_local(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded_string}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def display_logo():
    background_image_path = "image/background.png"
    add_bg_image_from_local(background_image_path)

    _, col2, _ = st.columns([1, 6, 1])
    with col2:
        st.image("image/logo_text.png")

def display_centered_markdown(text):
    st.markdown(f"<h1 style='text-align: center;'>{text}</h1>", unsafe_allow_html=True)