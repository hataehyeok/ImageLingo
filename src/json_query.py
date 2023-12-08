import streamlit as st
import json

def load_api_key(json_file):
    try:
        json_data = json.load(json_file)
        return json_data.get('api_key')
    except json.JSONDecodeError:
        st.error("Invalid JSON file")
        return None