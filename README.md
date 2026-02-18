# Spider Translator 🕷️

A smart AI-powered machine translation tool that automatically detects the source language and translates it to your desired target language.

## Features

- **Automatic Language Detection**: Uses `xlm-roberta-base-language-detection` to identify the input language from over 20 languages.
- **Multilingual Translation**: Uses `facebook/m2m100_418M` to translate text between 100 languages.
- **Smart Interface**: Includes both a command-line script and a user-friendly Streamlit web application.

## Installation

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone <repository-url>
    cd machine-translation
    ```

2.  **Install Dependencies**:
    Make sure you have Python installed, then run:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Web Interface (Streamlit)

The easiest way to use the translator is via the web app.

```bash
streamlit run app.py
```

This will open the interface in your browser. You can type text, see the detected language, and select a target language for translation.

### Command Line

You can also run the translator directly in your terminal:

```bash
python main.py
```

Follow the prompts to enter text. Type `quit` to exit.

## Note on First Run

⚠️ **Important**: The first time you run this application, it will download necessary pre-trained models from Hugging Face. This download is approximately **2GB** and may take a few minutes depending on your internet connection. 

Once downloaded, the models are cached locally, and subsequent runs will be fast!

## Project Structure

- `app.py`: The Streamlit web application.
- `main.py`: Core logic for detection and translation.
- `requirements.txt`: List of Python dependencies.
