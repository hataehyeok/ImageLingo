import src.openai_query as openai_query
import src.translate as translate
import os

HarderSentenceMaker= [{"role": "system", "content":
                 "You are a sentence generator. Your role is receiving a sentence in a certain language and making the sentence harder in that language."}]
EasierSentenceMaker= [{"role": "system", "content":
                 "ou are a sentence generator. Your role is receiving a sentence in a certain language and making the sentence easier in that language."}]

def revise_original_sentence(collection_name, sentence, index, target_lang):
    path = f"./data/{collection_name}"
    sentence_dir = f"{path}/sentence"
    translation_dir = f"{path}/translation"

    os.makedirs(sentence_dir, exist_ok=True)
    os.makedirs(translation_dir, exist_ok=True)

    sentence_path = os.path.join(sentence_dir, f"{index}.txt")
    with open(sentence_path, "w") as file:
        file.write(sentence)
    
    translation_path = os.path.join(translation_dir, f"{index}.txt")
    with open(translation_path, "w") as file:
        file.write(translate.translate(sentence, target_lang))


def makeEasier(collection_name, sentence, target_word, index, target_lang):
    instructions =  """The vocabulary of this sentence is too harder. Make the sentence a bit easier. However, maintain the usage of the word :""" + target_word + """ Maintain language of the sentence, which has a code of"""+ target_lang + "This is the sentence: " + sentence 
    EasierRes = openai_query.GPT4Query(EasierSentenceMaker, instructions, [])
    revise_original_sentence(collection_name, EasierRes, index, target_lang)

def makeHarder(collection_name, sentence, target_word, index, target_lang):
    instructions = """The vocabulary of this sentence is too easy. Make the sentence a bit harder. However, maintain the usage of the word :""" + target_word + """ Maintain language of the sentence, which has a code of"""+ target_lang + "This is the sentence: " + sentence 
    HarderRes = openai_query.GPT4Query(EasierSentenceMaker, instructions, [])
    revise_original_sentence(collection_name, HarderRes, index, target_lang)


