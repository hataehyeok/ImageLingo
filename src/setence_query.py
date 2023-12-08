import openai
import requests

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

# # Example usage
# api_key = "sk-qwer"
# vocab_list = ["serendipity", "ephemeral", "solitude"]
# example_sentences = generate_example_sentences(api_key, vocab_list)

def download_image(image_url, save_path):
    try:
        # Send a GET request to the image URL
        response = requests.get(image_url)

        # Raise an exception if the request was unsuccessful
        response.raise_for_status()

        # Write the content of the response to a file
        with open(save_path, 'wb') as file:
            file.write(response.content)

        print(f"Image successfully downloaded to {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the image: {e}")

def generate_image(api_key, sentence, image_path):
    openai.api_key = api_key
    image_prompt = GPT4Query(GPT_Prompt_Generator, "Generate a prompts using the sentence : " + sentence, [])
 
    response = openai.Image.create(
    model="dall-e-3",
    prompt= image_prompt,
    size="1024x1024",
    quality="standard",
    n=1,
    )

    image_url = response.data[0].url
    # print(image_url)
    # Example usage
    # save_path = "path_to_save_image.jpg"  # Replace with your desired path and file name
    download_image(image_url, image_path)


def generate_image(api_key, sentence, image_path):
    openai.api_key = api_key
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
    except openai.error.InvalidRequestError as e:
        # Handle the specific error
        print(f"Image generation request rejected: {e}")
        # Optional: Adjust the sentence or prompt and retry
        # ...
    except Exception as e:
        # Handle other potential errors
        print(f"An error occurred: {e}")

        
# for sentence in example_sentences:
#     generate_image(api_key,sentence)