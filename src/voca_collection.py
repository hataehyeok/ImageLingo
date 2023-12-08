import streamlit as st
import os
import glob
import src.test_analysis as test_analysis
import src.openai_query as openai_query


def create_collection(collection_name, uploaded_file):
    path = f"./data/{collection_name}"
    os.makedirs(path, exist_ok=True)
    os.makedirs(f"{path}/image", exist_ok=True)
    os.makedirs(f"{path}/word", exist_ok=True)
    os.makedirs(f"{path}/sentence", exist_ok=True)
    os.makedirs(f"{path}/source_image", exist_ok=True)

    image_path = os.path.join(path, "source_image", uploaded_file.name)
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    vocab = test_analysis.extract_highlighted_text(image_path)
    vocab_list = vocab.split()
    print("vocabularies list")
    print(vocab)
    print(vocab_list)
    
    if st.session_state.api_key:
        example_sentences = openai_query.generate_example_sentences(st.session_state.api_key, vocab_list)
    
        for i, sentence in enumerate(example_sentences):
            sentence_path = os.path.join(path, "sentence", str(i) + ".txt")
            with open(sentence_path, "w") as f:
                f.write(sentence)

        for i, sentence in enumerate(example_sentences):
            image_path = os.path.join(path, "image", str(i) + ".jpg")
            openai_query.generate_image(st.session_state.api_key, sentence, image_path)

        for i, word in enumerate(vocab_list):
            word_path = os.path.join(path, "word", str(i) + ".txt")
            with open(word_path, "w") as f:
                f.write(word)
    else:
        st.error("API key is not set. Please upload the API key file.")


def get_collections():
    return os.listdir("./data")


def collection_screen(collection_name):
    st.title(f"{collection_name} 컬렉션")
    if st.button("뒤로가기"):
        st.session_state.page = 'main'
    display_collection_content(collection_name)


def display_collection_content(collection_name):

    image_path = f"./data/{collection_name}/image"
    word_path = f"./data/{collection_name}/word"
    sentence_path = f"./data/{collection_name}/sentence"

    images = sorted(glob.glob(f"{image_path}/*"))
    words = sorted(glob.glob(f"{word_path}/*"))
    sentences = sorted(glob.glob(f"{sentence_path}/*"))

    min_length = min(len(images), len(words), len(sentences))

    for i in range(min_length):
        image, word, sentence = images[i], words[i], sentences[i]

        st.image(image, caption=f"Image {i}")

        with open(word, 'r') as file:
            word_content = file.read()
        st.write(f"Word {i}: {word_content}")

        with open(sentence, 'r') as file:
            sentence_content = file.read()
        st.write(f"Sentence {i}: {sentence_content}")
