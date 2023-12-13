import streamlit as st
import os
import glob
import src.openai_query as openai_query
import src.design_page as design_page
import src.image_to_text as image_to_text

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

    vocab = image_to_text.extract_voca_list(image_path)
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
    design_page.display_logo()
    design_page.display_centered_markdown(f"{collection_name}")
    if st.button("Back"):
        st.session_state.page = 'collection_creation'
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

        _, col2, _ = st.columns([1, 6, 1])
        with col2:
            st.image(image, caption=f"Image {i}")

            with open(word, 'r') as file:
                word_content = file.read()
            # st.write(f"Word {i}: {word_content}")

            with open(sentence, 'r') as file:
                sentence_content = file.read()
            # st.write(f"Sentence {i}: {sentence_content}")
            st.markdown(f"""
                <div style="background-color: white; border: 1px solid #ccc; padding: 10px; 
                            border-radius: 5px; margin: 10px 0;">
                    <p style="font-weight: bold; font-size: 18px;"> {word_content}</p>
                    <p style="font-weight: bold; font-size: 18px;"> {sentence_content}</p>
                </div>
                """, unsafe_allow_html=True)
