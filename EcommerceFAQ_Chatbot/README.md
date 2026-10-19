
# QueryCart - E-commerce FAQ Chatbot

QueryCart is a Python-based FAQ chatbot that helps customers
find answers to common e-commerce questions about orders,
delivery, returns, refunds, and payment methods.

## Features

- Answers frequently asked e-commerce questions
- Text preprocessing using NLTK
- FAQ matching using TF-IDF and cosine similarity
- Interactive web interface using HTML, CSS, and JavaScript
- Flask backend for processing chat messages
- Quick-question buttons
- Friendly greeting and fallback responses
- Responsive chatbot interface

## Technologies Used

- Python
- Flask
- NLTK
- Scikit-learn
- HTML5
- CSS3
- JavaScript

## Project Structure

```text
Ecommerce_Faq_Chatbot/
├── app.py
├── main.py
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
├── README.md
├── .gitignore
└── requirements.txt
```

## Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Ecommerce_Faq_Chatbot
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Run the application

```bash
python app.py
```

### 4. Open in your browser

Visit:

http://127.0.0.1:5000

## How It Works

1. The user enters a question in the chatbot interface.
2. JavaScript sends the question to the Flask backend.
3. Python preprocesses the question.
4. TF-IDF converts the question into a numerical vector.
5. Cosine similarity compares it with stored FAQ questions.
6. The chatbot returns the best matching answer.

## Future Improvements

- Add more FAQs
- Improve intent recognition
- Store FAQs in a database
- Add conversation history
- Deploy the chatbot online

## Author

Meharooba A

## Disclaimer

This project uses sample e-commerce questions and answers
for educational purposes.