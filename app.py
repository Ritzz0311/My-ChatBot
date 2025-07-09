import re
import requests
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- IMPORTANT: PASTE YOUR API KEYS HERE ---
GUARDIAN_API_KEY = "446e78ea-63c2-4c7d-ab57-e263de9567a2"
OPENWEATHERMAP_API_KEY = "85a0089efbc7264efef6b170e25f555e"

app = Flask(__name__)
CORS(app)

GUARDIAN_API_URL = "https://content.guardianapis.com/search"

class AdvancedChatbot:
    def __init__(self):
        self.responses = {
            r"hello|hi|hey": "Hello! How can I help you?",
            r"how are you|how's it going|how do you do": "I'm just a bot, but I'm doing great! How about you?",
            r"what's your name|who are you": "I'm an advanced chatbot. You can call me ChatBot!",
            r"tell me a joke|say something funny|joke": self.get_joke,
            r"weather in (.+)": self.get_weather,
            r"what's the time|tell me the time|what time is it|time": self.get_time,
            r"what's the date|tell me the date|what date is it|date": self.get_date,
            r"news|latest news|top headlines": self.get_news,
            r"bye|goodbye": "Goodbye! Have a great day!",
            "default": "I'm sorry, I don't understand that. Can you please rephrase?"
        }

    def get_response(self, user_input):
        user_input = user_input.lower()
        for pattern, response in self.responses.items():
            match = re.search(pattern, user_input)
            if match:
                if callable(response):
                    return response(match)
                return response
        return self.responses["default"]

    def get_joke(self, match):
        try:
            response = requests.get("https://official-joke-api.appspot.com/random_joke")
            joke = response.json()
            return f"{joke['setup']}... {joke['punchline']}"
        except:
            return "Sorry, I couldn't fetch a joke right now."

    def get_weather(self, match):
        city = match.group(1)
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()
            if data["cod"] == 200:
                weather = data["weather"][0]["description"]
                temp = data["main"]["temp"]
                return f"The weather in {city.title()} is {weather} with a temperature of {temp}°C."
            else:
                return f"Sorry, I couldn't find the weather for {city}."
        except:
            return "Sorry, there was an issue fetching the weather."

    def get_time(self, match):
        now = datetime.now()
        return f"The current time is {now.strftime('%H:%M:%S')}."

    def get_date(self, match):
        now = datetime.now()
        return f"Today's date is {now.strftime('%A, %B %d, %Y')}."

    def get_news(self, match):
        if GUARDIAN_API_KEY == "your_guardian_api_key":
            return "Sorry, the Guardian API key is not configured on the server."
        try:
            params = {
                "api-key": GUARDIAN_API_KEY,
                "show-fields": "headline",
                "page-size": 5
            }
            response = requests.get(GUARDIAN_API_URL, params=params)
            data = response.json()
            if "response" in data and "results" in data["response"]:
                articles = data["response"]["results"]
                if articles:
                    headlines = [article["webTitle"] for article in articles]
                    return "Here are the latest news headlines: " + ". ".join(headlines)
                else:
                    return "Sorry, no news articles were found."
            else:
                return "Sorry, I couldn't fetch the news right now."
        except Exception as e:
            print(f"Error fetching news: {e}")
            return "Sorry, there was an issue fetching the news."

chatbot = AdvancedChatbot()

@app.route("/", methods=["GET"])
def index():
    return """
    <h2>🤖 Welcome to My Chatbot!</h2>
    <p>Send a POST request to <code>/chat</code> with JSON like:</p>
    <pre>{
  "message": "hello"
}</pre>
    """

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"response": "Invalid input."}), 400

    response = chatbot.get_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
