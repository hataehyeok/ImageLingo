import openai
import requests
import time

GPT_Sentence_Generator_Easy = [{"role": "system", "content":
                 "You are a sentence generator. You are to generate a random sentence using a word that we give you. The sentence should use the word in a context where the word can be visualized."}]
GPT_Prompt_Generator = [{"role": "system", "content":
                 "You are a DALLE-3 prompt generator. You are to create a detailed, imaginative image generation prompt for DALL-E 3 that best describes the scene depicted by a given sentence."}]

def GPT4Query(role, instruction, context):
    messages = role
    message = "User : " + instruction
    context.extend([{"role": "user", "content": message}])
    messages = context + messages
    chat = openai.ChatCompletion.create(
        model="gpt-4", messages=messages, max_tokens=5000, temperature=0.8, top_p=0.7)
    print(f"ChatGPT: {chat.choices[0].message.content}")
    context.append(
        {"role": "assistant", "content": chat.choices[0].message.content})
    return chat.choices[0].message.content

def generate_example_sentences(api_key, vocab_list):
    openai.api_key = api_key

    example_sentences = []

    for word in vocab_list:
        example_sentences.append(GPT4Query(GPT_Sentence_Generator_Easy, "Generate a sentence using the word : " + word, []))

    return example_sentences

def download_image(image_url, save_path):
    try:
        response = requests.get(image_url)
        response.raise_for_status()

        with open(save_path, 'wb') as file:
            file.write(response.content)

        print(f"Image successfully downloaded to {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the image: {e}")

def generate_image(api_key, sentence, image_path):
    openai.api_key = api_key
    max_retries = 3
    retry_delay = 5

    for attempt in range(max_retries):
        try:
            image_prompt = GPT4Query(GPT_Prompt_Generator, "Generate prompts using the sentence : " + sentence, [])
            response = openai.Image.create(
                model="dall-e-3",
                prompt=image_prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            image_url = response.data[0].url
            download_image(image_url, image_path)
            break  # Break out of the loop if successful
        except openai.error.InvalidRequestError as e:
            print(f"Attempt {attempt + 1} - Image generation request rejected: {e}")
            if attempt < max_retries - 1:  # If not the last attempt, wait and then retry
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                # Optional: Modify the sentence or prompt before retrying
                # sentence = modify_sentence(sentence)
            else:
                print("Maximum retry attempts reached. Unable to generate image.")
        except Exception as e:
            print(f"An error occurred: {e}")
            break  # Exit loop on other types of exceptions

# Define the modify_sentence function if you plan to modify the sentence for retries
# def modify_sentence(sentence):
#     # Logic to modify the sentence
#     return modified_sentence