import streamlit as st
import os
import glob
import src.openai_query as openai_query
import src.design_page as design_page
import src.generate_voca_list as generate_voca_list
import src.translate as translate


def create_collection(collection_name, uploaded_file):
    path = f"./data/{collection_name}"
    os.makedirs(path, exist_ok=True)
    os.makedirs(f"{path}/image", exist_ok=True)
    os.makedirs(f"{path}/word", exist_ok=True)
    os.makedirs(f"{path}/sentence", exist_ok=True)
    os.makedirs(f"{path}/translation", exist_ok=True)
    os.makedirs(f"{path}/source_image", exist_ok=True)

    image_path = os.path.join(path, "source_image", uploaded_file.name)
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    (vocab, target_lang) = generate_voca_list.extract_voca_list(image_path)
    print(target_lang)

    vocab_list = vocab.split()
    print("vocabularies list")
    print(vocab)
    print(vocab_list)
    
    if st.session_state.api_key:
        example_sentences = openai_query.generate_example_sentences(st.session_state.api_key, vocab_list, target_lang)
    
        for i, sentence in enumerate(example_sentences):
            sentence_path = os.path.join(path, "sentence", str(i) + ".txt")
            with open(sentence_path, "w") as f:
                f.write(sentence)

            translation_path = os.path.join(path, "translation", str(i) + ".txt")
            with open(translation_path, "w") as f:
                f.write(translate.translate(sentence, target_lang))

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
    traslation_path = f"./data/{collection_name}/translation"

    images = sorted(glob.glob(f"{image_path}/*"))
    words = sorted(glob.glob(f"{word_path}/*"))
    sentences = sorted(glob.glob(f"{sentence_path}/*"))
    trans_list = sorted(glob.glob(f"{traslation_path}/*"))

    min_length = min(len(images), len(words), len(sentences), len(trans_list))

    if 'show_contents' not in st.session_state:
        st.session_state.show_contents = [False] * min_length

    for i in range(min_length):
        image, word, sentence, trans_word = images[i], words[i], sentences[i], trans_list[i]

        _, col2, _ = st.columns([1, 6, 1])
        with col2:
            st.image(image, caption=f"Image {i}")

            with open(word, 'r') as file:
                word_content = file.read()

            with open(sentence, 'r') as file:
                sentence_content = file.read()
            
            with open(trans_word, 'r') as file:
                trans_word_content = file.read()

            st.markdown(f"""
                <div style="background-color: white; border: 1px solid #ccc; padding: 10px; 
                            border-radius: 5px; margin: 10px 0;">
                    <p style="font-weight: bold; font-size: 18px;"> {word_content}</p>
                    <p style="font-weight: bold; font-size: 18px;"> {sentence_content}</p>
                </div>
                """, unsafe_allow_html=True)

            if st.button(f"Show/Hide Traslate {i}", key=f"button_{i}"):
                st.session_state.show_contents[i] = not st.session_state.show_contents[i]

            if st.session_state.show_contents[i]:
                st.markdown(f"""
                <div style="background-color: white; border: 1px solid #ccc; padding: 10px; 
                            border-radius: 5px; margin: 10px 0;">
                    <p style="font-weight: bold; font-size: 18px;"> {trans_word_content}</p>
                </div>
                """, unsafe_allow_html=True)
