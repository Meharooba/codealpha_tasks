# Transly – Language Translator

A web-based language translation application built using Python and Django. Transly helps users translate text between multiple languages through a simple, responsive, and user-friendly interface.

## Features

- Translate text between supported languages.
- Select source and target languages.
- Swap source and target languages.
- Copy translated text to the clipboard.
- Listen to translated text using browser text-to-speech.
- Responsive interface for desktop and mobile devices.
- Sunset-themed user interface.
- Character counter for input text.
- Error handling for translation requests.

## Technologies Used

- Python
- Django
- HTML5
- CSS3
- JavaScript
- Requests
- Browser Speech Synthesis API

## Project Structure

Language-Translator/
│
├── manage.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── translator_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
└── translator/
    ├── views.py
    ├── urls.py
    ├── models.py
    └── templates/
        └── translator/
            └── index.html

*The structure above is illustrative; your project may contain additional files.*

## Installation and Setup

### 1. Clone the repository

git clone <your-github-repository-url>
cd Language-Translator

Replace the repository URL with your actual GitHub repository URL.

### 2. Create a virtual environment

python -m venv .venv

### 3. Activate the virtual environment

**Windows PowerShell:**

.\.venv\Scripts\Activate.ps1

### 4. Install dependencies

pip install -r requirements.txt

### 5. Run database migrations

python manage.py migrate

### 6. Start the development server

python manage.py runserver

Open the application in your browser:

http://127.0.0.1:8000/

## How to Use

1. Select the source language.
2. Select the target language.
3. Enter the text you want to translate.
4. Click **Translate Text**.
5. Copy the translation or click **Speak Translation** to hear it.

## Translation Services

The application uses external translation endpoints. Translation availability and accuracy depend on those services and the selected language pair.

The Speak Translation feature uses the browser's built-in speech synthesis functionality. Available voices depend on the browser, operating system, and installed language voices.

## Future Improvements

- Improve translation reliability.
- Add translation history.
- Support additional language pairs.
- Improve speech and voice compatibility.
- Deploy the application online.

## Author
Meharooba A

Developed as a Python and Django project.