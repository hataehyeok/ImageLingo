import streamlit as st
import pytesseract
import src.json_query as json_query
import src.voca_collection as voca_collection

pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("src/style.css")

if 'page' not in st.session_state:
    st.session_state.page = 'main'
if 'api_key' not in st.session_state:
    st.session_state.api_key = None

def main_screen():
    st.session_state.page = 'main'
    col1, col2 = st.columns([1, 6])
    with col1:
        st.image("image/logo.png")
    with col2:
        st.markdown("<h1 style='background-color: mintcream; text-align: center; color: black;'>ImageLingo</h1>", unsafe_allow_html=True)


    api_key_file = st.file_uploader("API 키 파일 업로드 (JSON)", type=['json'])
    if api_key_file is not None:
        st.session_state.api_key = json_query.load_api_key(api_key_file)

    with st.form(key='new_collection_form'):
        new_collection_name = st.text_input("새 컬렉션 이름:")
        uploaded_file = st.file_uploader("이미지 업로드", type=['png', 'jpg', 'jpeg'])
        submit_button = st.form_submit_button(label='컬렉션 생성')
        if submit_button and uploaded_file:
            voca_collection.create_collection(new_collection_name, uploaded_file)

    collections = voca_collection.get_collections()
    selected_collection = st.selectbox("컬렉션 선택", collections)
    if st.button("컬렉션 보기"):
        st.session_state.collection_name = selected_collection
        st.session_state.page = 'collection'

if st.session_state.page == 'main':
    main_screen()
elif st.session_state.page == 'collection' and 'collection_name' in st.session_state:
    voca_collection.collection_screen(st.session_state.collection_name)
