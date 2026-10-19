const chatForm = document.getElementById("chatForm");
const userInput = document.getElementById("userInput");
const chatMessages = document.getElementById("chatMessages");
const sendButton = document.getElementById("sendButton");

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addMessage(text, className) {
    const message = document.createElement("div");

    message.classList.add("message", className);
    message.textContent = text;

    chatMessages.appendChild(message);
    scrollToBottom();

    return message;
}

function showTypingIndicator() {
    const indicator = document.createElement("div");

    indicator.className = "typing-indicator";
    indicator.setAttribute("aria-label", "Bot is typing");

    for (let i = 0; i < 3; i++) {
        indicator.appendChild(document.createElement("span"));
    }

    chatMessages.appendChild(indicator);
    scrollToBottom();

    return indicator;
}

async function sendMessage(text) {
    const question = text.trim();

    if (!question || sendButton.disabled) {
        return;
    }

    addMessage(question, "user-message");

    userInput.value = "";
    userInput.disabled = true;
    sendButton.disabled = true;

    const typingIndicator = showTypingIndicator();

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: question
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.answer || "Request failed.");
        }

        addMessage(data.answer, "bot-message");

    } catch (error) {
        addMessage(
            "Sorry, I couldn't connect to the server. Please try again.",
            "bot-message"
        );

        console.error("Chat error:", error);

    } finally {
        typingIndicator.remove();
        userInput.disabled = false;
        sendButton.disabled = false;
        userInput.focus();
        scrollToBottom();
    }
}

chatForm.addEventListener("submit", function (event) {
    event.preventDefault();
    sendMessage(userInput.value);
});

function sendSuggestion(question) {
    sendMessage(question);
}

