import streamlit as st
import os

# 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = 'main'

# 메인 화면 함수
def main_screen():
    st.session_state.page = 'main'
    st.title("ImageLingo")

    # 컬렉션 생성
    with st.form(key='new_collection_form'):
        new_collection_name = st.text_input("새 컬렉션 이름:")
        submit_button = st.form_submit_button(label='컬렉션 생성')
        if submit_button:
            create_collection(new_collection_name)

    # 컬렉션 목록 표시
    collections = get_collections()
    selected_collection = st.selectbox("컬렉션 선택", collections)
    if st.button("컬렉션 보기"):
        st.session_state.collection_name = selected_collection
        st.session_state.page = 'collection'

# 컬렉션 화면 함수
def collection_screen(collection_name):
    st.title(f"{collection_name} 컬렉션")
    if st.button("뒤로가기"):
        st.session_state.page = 'main'

    # 컬렉션 내용 표시
    display_collection_content(collection_name)

# 컬렉션 생성 함수
def create_collection(collection_name):
    path = f"./collections/{collection_name}"
    os.makedirs(path, exist_ok=True)

# 컬렉션 목록 가져오기 함수
def get_collections():
    return os.listdir("./collections")

# 컬렉션 내용 표시 함수
def display_collection_content(collection_name):
    path = f"./collections/{collection_name}"
    # 여기에 이미지, 단어, 예시 문장을 표시하는 로직 추가

# 앱 실행 로직
if st.session_state.page == 'main':
    main_screen()
elif st.session_state.page == 'collection' and 'collection_name' in st.session_state:
    collection_screen(st.session_state.collection_name)
