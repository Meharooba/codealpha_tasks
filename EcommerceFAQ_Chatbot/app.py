import string
from flask import Flask, render_template, request, jsonify
from nltk.tokenize import wordpunct_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)


faqs = [
    {
        "question": "How can I track my order?",
        "answer": "You can track your order using the tracking link sent to your registered email."
    },
    {
        "question": "What is your return policy?",
        "answer": "You can return eligible products within 7 days of delivery."
    },
    {
        "question": "How long does delivery take?",
        "answer": "Delivery usually takes 3 to 5 business days."
    },
    {
        "question": "Which payment methods do you accept?",
        "answer": "We accept UPI, debit cards, credit cards, and net banking."
    },
    {
        "question": "How can I cancel my order?",
        "answer": "You can cancel your order before it is shipped by visiting your orders page."
    },
    {
        "question": "How can I contact customer support?",
        "answer": "You can contact customer support through the Help section on our website."
    },
    {
        "question": "Can I get a refund?",
        "answer": "Refunds are processed after the returned product is approved, according to the refund policy."
    },
    {
        "question": "Do you offer free shipping?",
        "answer": "Free shipping is available on eligible orders. Check the shipping details at checkout."
    },
    {
        "question": "Can I change my delivery address?",
        "answer": "You may be able to change your delivery address before your order is shipped."
    },
    {
        "question": "How do I create an account?",
        "answer": "Click the Sign Up button on our website and enter the required details."
    },
    {
        "question": "What should I do if my order is delayed?",
        "answer": "If your order is delayed, check the tracking link for the latest delivery updates or contact customer support."
    },

    {
        "question": "Can I exchange a product?",
        "answer": "You can exchange eligible products according to our exchange policy. Please check the product's eligibility before requesting an exchange."
    },
    {
        "question": "How can I check my order status?",
        "answer": "Visit the My Orders section of your account to check the current status of your order."
    },
    {
        "question": "What should I do if I receive a damaged product?",
        "answer": "If you receive a damaged product, contact customer support with your order details and photos of the damage."
    },
    {
        "question": "What should I do if I receive the wrong item?",
        "answer": "Contact customer support with your order details so they can help resolve the issue."
    },
    {
        "question": "How long does a refund take?",
        "answer": "Refund processing time depends on the payment method and the refund policy. You will be notified once your refund is processed."
    },
    {
        "question": "Can I place an order without creating an account?",
        "answer": "Guest checkout may be available if our website supports it. Otherwise, you need to create an account to place an order."
    },
    {
        "question": "How can I reset my password?",
        "answer": "Click the Forgot Password option on the login page and follow the instructions to reset your password."
    },
    {
        "question": "Is cash on delivery available?",
        "answer": "Cash on delivery may be available for eligible products and delivery locations. Check the available payment options at checkout."
    },
    {
        "question": "How can I apply a discount coupon?",
        "answer": "Enter your valid coupon code in the promo code field at checkout and apply it to receive the eligible discount."
    },
    {
        "question": "Why was my payment declined?",
        "answer": "Your payment may have been declined due to insufficient funds, incorrect details, or a bank issue. Please verify your details or try another payment method."
    },
    {
        "question": "Can I order from outside India?",
        "answer": "International shipping availability depends on our delivery locations. Please check the shipping information on our website."
    },
    {
        "question": "Will I receive an order confirmation?",
        "answer": "Yes, an order confirmation is usually sent to your registered email address after your order is placed successfully."
    },
    {
        "question": "Can I cancel my order after it has been shipped?",
        "answer": "Orders that have already been shipped may not be eligible for cancellation. Please contact customer support for assistance."
    },
    {
        "question": "How can I delete my account?",
        "answer": "Please contact customer support or check your account settings for available account deletion options."
    },
    {
        "question": "Are my payment details secure?",
        "answer": "We use appropriate security measures to protect payment information. Always complete payments through the official checkout page."
    },
    {
        "question": "What happens if I miss my delivery?",
        "answer": "The delivery partner may attempt delivery again or contact you to arrange another delivery attempt."
    },
    {
        "question": "Do you provide an invoice for my order?",
        "answer": "An invoice may be available in your order details or sent to your registered email after purchase."
    },
    {
        "question": "How can I update my phone number?",
        "answer": "Log in to your account and check the profile settings to update your phone number, if the option is available."
    },
    {
        "question": "Why is my order showing as cancelled?",
        "answer": "An order may be cancelled due to payment issues, stock availability, or other reasons. Check your order details or contact customer support for clarification."
    }
]


def preprocess_text(text):
    text = text.lower()
    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )
    tokens = wordpunct_tokenize(text)
    return " ".join(tokens)


questions = [
    preprocess_text(faq["question"])
    for faq in faqs
]

vectorizer = TfidfVectorizer()
faq_vectors = vectorizer.fit_transform(questions)

def get_answer(user_question):
    processed_question = preprocess_text(user_question)

    if not processed_question.strip():
        return "Please enter a question."

    greetings = [
        "hi", "hello", "hey",
        "good morning", "good evening"
    ]

    if processed_question in greetings:
        return "Hello! Welcome to our store. How can I help you today?"

    if processed_question in [
        "thanks", "thank you", "thank you very much"
    ]:
        return "You're welcome! Happy shopping!"

    if processed_question in [
        "how are you",
        "how are you doing"
    ]:
        return "I'm doing great! 😊 How can I help you with your shopping today?"

    if processed_question in [
            "bye",
            "goodbye",
            "tata"
    ]:
        return "Bye! 😊 Have a great day!"

    if "your name" in processed_question or "who are you" in processed_question:
        return "I'm QueryCart , your friendly online shopping assistant ! 😊"
    
    
    user_vector = vectorizer.transform(
        [processed_question]
    )

    similarities = cosine_similarity(
        user_vector, faq_vectors
    )[0]

    best_match_index = similarities.argmax()
    best_score = similarities[best_match_index]

    if best_score < 0.15:
        return (
            "Sorry, I couldn't find a suitable answer. "
            "Please contact customer support."
        )

    return faqs[best_match_index]["answer"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    question = data.get("message", "")

    if not isinstance(question, str):
        return jsonify({"answer": "Please enter a valid question."}), 400

    answer = get_answer(question)

    return jsonify({"answer": answer})


if __name__ == "__main__":
    app.run(debug=True)