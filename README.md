# ImageLingo

ImageLingo is a Streamlit-based web application designed to create and manage collections of images, words, and sentences extracted from images using Optical Character Recognition (OCR). It provides a user-friendly interface for uploading images, extracting highlighted text, and generating example sentences and corresponding images.

## Features

- **API Key Upload**: Securely upload your API key in JSON format.
- **Collection Creation**: Create new collections of images and extracted text.
- **Collection Browsing**: Browse through existing collections and view images, words, and example sentences.
- **Responsive Design**: With a background image and a clean UI, enjoy a responsive design that adapts to different screen sizes.

## Installation

To run Image Lingo on your local machine, you need to have Python installed. Follow these steps:

1. Clone the repository

    ```bash
    git clone https://github.com/your-username/image-lingo.git
    cd image-lingo
    ```

2. Install the required Python packages

    ```bash
    pip install -r requirements.txt
    ```

3. Run the Streamlit application

    ```bash
    streamlit run app.py
    ```

## Usage

Upon launching the app, you will be greeted with a login screen. After logging in, you can:

- Upload an API key file to authenticate.
- Create new collections by uploading images.
- Select and view existing collections.

### Login Screen

The login screen is the entry point of the application. Enter your credentials to proceed to the main features.

### API Key Selection

For features that require external API interaction, upload your API key in JSON format.

### Collection Management

Create and manage your collections:

- Create Collection: Upload an image to create a new collection.
- View Collection: Select from existing collections to view details.

## Development

This application is built using the Streamlit framework, which allows for rapid development of data applications. For contributions or modifications, refer to the Streamlit documentation to understand the structure and capabilities of the framework.

## License

MIT License

## Contact

For any additional questions or comments, please contact the repository owner.
