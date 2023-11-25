import streamlit as st
import os
import glob
import cv2
import pytesseract
from PIL import Image
import numpy as np

# Tesseract 실행 파일 경로 설정
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

# 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = 'main'

# 텍스트 추출 함수
def extract_highlighted_text(image_path):
    image = cv2.imread(image_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([20, 80, 80])
    upper = np.array([40, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    highlighted = cv2.bitwise_and(image, image, mask=mask)
    pil_image = Image.fromarray(cv2.cvtColor(highlighted, cv2.COLOR_BGR2RGB))
    text = pytesseract.image_to_string(pil_image)
    return text

# 메인 화면 함수
def main_screen():
    st.session_state.page = 'main'
    st.title("ImageLingo")

    with st.form(key='new_collection_form'):
        new_collection_name = st.text_input("새 컬렉션 이름:")
        uploaded_file = st.file_uploader("이미지 업로드", type=['png', 'jpg', 'jpeg'])
        submit_button = st.form_submit_button(label='컬렉션 생성')
        if submit_button and uploaded_file:
            create_collection(new_collection_name, uploaded_file)

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

    display_collection_content(collection_name)

# 컬렉션 생성 함수
def create_collection(collection_name, uploaded_file):
    path = f"./collections/{collection_name}"
    os.makedirs(path, exist_ok=True)
    os.makedirs(f"{path}/image", exist_ok=True)
    os.makedirs(f"{path}/word", exist_ok=True)
    os.makedirs(f"{path}/sentence", exist_ok=True)
    os.makedirs(f"{path}/source_image", exist_ok=True)
    os.makedirs(f"{path}/raw_string", exist_ok=True)

    # 이미지 저장
    image_path = os.path.join(path, "source_image", uploaded_file.name)
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # 추출된 텍스트 저장
    extracted_text = extract_highlighted_text(image_path)
    text_path = os.path.join(path, "raw_string", uploaded_file.name + ".txt")
    with open(text_path, "w") as f:
        f.write(extracted_text)

# 컬렉션 목록 가져오기 함수
def get_collections():
    return os.listdir("./collections")

# 컬렉션 내용 표시 함수
def display_collection_content(collection_name):
    # 각 디렉토리 경로 설정
    image_path = f"./collections/{collection_name}/image"
    word_path = f"./collections/{collection_name}/word"
    sentence_path = f"./collections/{collection_name}/sentence"

    # 파일 리스트 가져오기
    images = sorted(glob.glob(f"{image_path}/*"))
    words = sorted(glob.glob(f"{word_path}/*"))
    sentences = sorted(glob.glob(f"{sentence_path}/*"))

    # 파일이 가장 적은 디렉토리의 길이를 기준으로 함
    min_length = min(len(images), len(words), len(sentences))

    # 각 인덱스에 대해 이미지, 단어, 문장 표시
    for i in range(min_length):
        image, word, sentence = images[i], words[i], sentences[i]

        # 이미지 표시
        st.image(image, caption=f"Image {i}")

        # 단어 표시 (텍스트 파일 읽기)
        with open(word, 'r') as file:
            word_content = file.read()
        st.write(f"Word {i}: {word_content}")

        # 문장 표시 (텍스트 파일 읽기)
        with open(sentence, 'r') as file:
            sentence_content = file.read()
        st.write(f"Sentence {i}: {sentence_content}")

# 앱 실행 로직
if st.session_state.page == 'main':
    main_screen()
elif st.session_state.page == 'collection' and 'collection_name' in st.session_state:
    collection_screen(st.session_state.collection_name)
