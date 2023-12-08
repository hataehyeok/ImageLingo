import streamlit as st
import os
import glob
import pytesseract
import src.test_analysis as test_analysis
import src.openai_query as openai_query
import src.json_query as json_query

pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

if 'page' not in st.session_state:
    st.session_state.page = 'main'
if 'api_key' not in st.session_state:
    st.session_state.api_key = None

def main_screen():
    st.session_state.page = 'main'
    st.title("ImageLingo")

    api_key_file = st.file_uploader("API 키 파일 업로드 (JSON)", type=['json'])
    if api_key_file is not None:
        st.session_state.api_key = json_query.load_api_key(api_key_file)

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
    path = f"./data/{collection_name}"
    os.makedirs(path, exist_ok=True)
    os.makedirs(f"{path}/image", exist_ok=True)
    os.makedirs(f"{path}/word", exist_ok=True)
    os.makedirs(f"{path}/sentence", exist_ok=True)
    os.makedirs(f"{path}/source_image", exist_ok=True)

    # 이미지 저장
    image_path = os.path.join(path, "source_image", uploaded_file.name)
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # 추출된 텍스트 저장
    vocab = test_analysis.extract_highlighted_text(image_path)
    vocab_list = vocab.split()
    print("vocabularies list")
    print(vocab)
    print(vocab_list)
    
    if st.session_state.api_key:
        example_sentences = openai_query.generate_example_sentences(st.session_state.api_key, vocab_list)
    
        for i, sentence in enumerate(example_sentences):
            sentence_path = os.path.join(path, "sentence", str(i) + ".txt") # Ensure file extension is added
            with open(sentence_path, "w") as f:
                f.write(sentence)

        for i, sentence in enumerate(example_sentences):
            image_path = os.path.join(path, "image", str(i) + ".jpg") # Ensure file extension is added
            openai_query.generate_image(st.session_state.api_key, sentence, image_path)

        for i, word in enumerate(vocab_list):
            word_path = os.path.join(path, "word", str(i) + ".txt")
            with open(word_path, "w") as f:
                f.write(word)
    else:
        st.error("API key is not set. Please upload the API key file.")

# 컬렉션 목록 가져오기 함수
def get_collections():
    return os.listdir("./data")

# 컬렉션 내용 표시 함수
def display_collection_content(collection_name):
    # 각 디렉토리 경로 설정
    image_path = f"./data/{collection_name}/image"
    word_path = f"./data/{collection_name}/word"
    sentence_path = f"./data/{collection_name}/sentence"

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
