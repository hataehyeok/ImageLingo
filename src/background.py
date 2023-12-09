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

    col1, col2 = st.columns([1, 6])
    with col1:
        st.image("image/logo.png")
    with col2:
        st.markdown("<h1 text-align: center; color: black;'>ImageLingo</h1>", unsafe_allow_html=True)