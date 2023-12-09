import streamlit as st
import pytesseract
import src.json_query as json_query
import src.voca_collection as voca_collection
import src.design_page as design_page

pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

if 'page' not in st.session_state:
    st.session_state.page = 'login_session'
if 'api_key' not in st.session_state:
    st.session_state.api_key = None

def login_screen():
    design_page.display_logo()
    _, col2, _ = st.columns([1, 6, 1])
    with col2:
        design_page.display_centered_markdown("Login")
        st.text_input("ID")
        st.text_input("Password", type='password')
        if st.button("Login"):
            st.session_state.page = 'api_key_selection'


def api_key_selection_screen():
    design_page.display_logo()

    st.markdown("## API Key Selection")
    api_key_file = st.file_uploader("Upload API Key (JSON)", type=['json'])
    if api_key_file is not None:
        st.session_state.api_key = json_query.load_api_key(api_key_file)
    
    if st.button("NEXT"):
        st.session_state.page = 'collection_creation'

def collection_creation_screen():
    design_page.display_logo()

    design_page.display_centered_markdown("Welcome to Image Lingo")
    with st.form(key='new_collection_form'):
        new_collection_name = st.text_input("Create a new collection")
        uploaded_file = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'])
        submit_button = st.form_submit_button(label='Create Collection')
        if submit_button and uploaded_file:
            voca_collection.create_collection(new_collection_name, uploaded_file)

    collections = voca_collection.get_collections()
    selected_collection = st.selectbox("Select Collection", collections)
    if st.button("Enter Collection"):
        st.session_state.collection_name = selected_collection
        st.session_state.page = 'collection'

# Page Routing
if st.session_state.page == 'login_session':
    login_screen()
elif st.session_state.page == 'api_key_selection':
    api_key_selection_screen()
elif st.session_state.page == 'collection_creation':
    collection_creation_screen()
elif st.session_state.page == 'collection' and 'collection_name' in st.session_state:
    voca_collection.collection_screen(st.session_state.collection_name)