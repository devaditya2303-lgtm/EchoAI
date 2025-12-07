from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# ---------------------------
# Google Search Scraper
# ---------------------------
def google_answer(query):
    try:
        url = "https://www.google.com/search?q=" + query.replace(" ", "+")
        headers = {"User-Agent": "Mozilla/5.0"}
        html = requests.get(url, headers=headers)
        soup = BeautifulSoup(html.text, "html.parser")

        # Try to extract Google's answer box
        answer = soup.find("div", class_="BNeawe").text
        return answer

    except:
        return "I tried checking Google, macha… but I couldn't find it 🥲"


# ---------------------------
# EchoAI Brain
# ---------------------------
def echo_ai_reply(message):
    message_low = message.lower()

    # Human-like fun responses (not from Google)
    if "hi" in message_low or "hello" in message_low:
        return "Hi machaaaa 😎🔥 what’s cooking?"

    if "who are you" in message_low:
        return "I'm EchoAI, your goofy corporate-grade AI companion 🤖💼✨"

    if "love" in message_low:
        return "Ayy macha… love is like biryani—layers and surprises 😘🍛"

    # If it's a study / math / knowledge question → use Google
    if "what" in message_low or "why" in message_low or "how" in message_low or any(x.isdigit() for x in message_low):
        return google_answer(message)

    # Default human-like response
    return "Macha I didn’t get that 😅 say it again in simple words!"


# ---------------------------
# Flask Route (API)
# ---------------------------
@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")

    reply = echo_ai_reply(user_msg)

    return jsonify({
        "user": user_msg,
        "echo_ai": reply
    })


# Home route
@app.route("/")
def home():
    return "EchoAI is LIVE machaaaa! Use POST /chat to talk 🤖🔥"


# ---------------------------
# Run locally
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
