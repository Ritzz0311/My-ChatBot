import re
import os
import requests
from dotenv import load_dotenv
from datetime import datetime
from urllib.parse import urlencode
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# Load environment variables from .env
load_dotenv()
GUARDIAN_API_KEY = os.getenv("GUARDIAN_API_KEY")
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# Guardian API configuration
GUARDIAN_API_URL = "https://content.guardianapis.com/search"


class AdvancedChatbot:
    def __init__(self):
        self.responses = {
            r"weather in (.+)": self.get_weather,
            r"hello|hi|hey": "Hello! How can I help you?",
            r"how are you|how's it going|how do you do": "I'm just a bot, but I'm doing great! How about you?",
            r"what's your name|who are you": "I'm an advanced chatbot. You can call me ChatBot!",
            r"tell me a joke|say something funny|joke": self.get_joke,
            r"what's the time|tell me the time|what time is it|time": self.get_time,
            r"what's the date|tell me the date|what date is it|date": self.get_date,
            r"news|latest news|top headlines": self.get_news,
            r"bye|goodbye": "Goodbye! Have a great day!",
            "default": None
        }

    def get_response(self, user_input):
        normalized_input = user_input.lower()

        # Keyword-based check for playing songs
        if normalized_input.startswith('play '):
            song_name = user_input[5:].strip()
            return self.get_youtube_link(song_name)

        # Check other regex-based rules
        for pattern, response in self.responses.items():
            match = re.search(pattern, normalized_input)
            if match:
                if callable(response):
                    return {"type": "text", "content": response(match)}
                return {"type": "text", "content": response}
        
        # Fallback to Gemini
        gemini_response = self.ask_gemini(user_input)
        return {"type": "text", "content": gemini_response}

    def get_youtube_link(self, song_name):
        """Generates a structured response for a YouTube search."""
        query_string = urlencode({"search_query": song_name})
        video_url = f"https://www.youtube.com/results?{query_string}"
        return {
            "type": "youtube_link",
            "text": f"I found results for '{song_name}'.",
            "url": video_url
        }

    def get_joke(self, match):
        try:
            response = requests.get("https://official-joke-api.appspot.com/random_joke")
            response.raise_for_status()
            joke = response.json()
            return f"{joke['setup']}... {joke['punchline']}"
        except requests.exceptions.RequestException:
            return "Sorry, I couldn't fetch a joke right now."

    def get_weather(self, match):
        city = match.group(1).strip()
        if not OPENWEATHERMAP_API_KEY:
            return "Sorry, the weather service is not configured."
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data.get("cod") == 200:
                weather = data["weather"][0]["description"]
                temp = data["main"]["temp"]
                return f"The weather in {city.title()} is {weather} with a temperature of {temp}°C."
            else:
                return f"Sorry, I couldn't find the weather for {city.title()}."
        except requests.exceptions.RequestException:
            return "Sorry, there was an issue fetching the weather."

    def get_time(self, match):
        now = datetime.now()
        return f"The current time is {now.strftime('%H:%M:%S')}."

    def get_date(self, match):
        now = datetime.now()
        return f"Today's date is {now.strftime('%A, %B %d, %Y')}."

    def get_news(self, match):
        if not GUARDIAN_API_KEY or GUARDIAN_API_KEY == "your_guardian_api_key":
            return "Sorry, the Guardian API key is not configured on the server."
        try:
            params = {"api-key": GUARDIAN_API_KEY, "show-fields": "headline", "page-size": 5}
            response = requests.get(GUARDIAN_API_URL, params=params)
            response.raise_for_status()
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
        except requests.exceptions.RequestException:
            return "Sorry, there was an issue fetching the news."

    def ask_gemini(self, user_input):
        if not GEMINI_API_KEY:
            return "Sorry, the AI model is not configured."
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(user_input)
            return response.text.strip()
        except Exception as e:
            print(f"Gemini Error: {e}")
            return "Sorry, I couldn't process your request with the AI model right now."

# Create a single chatbot instance
chatbot = AdvancedChatbot()

# Define the API endpoint for the chatbot
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"response": {"type": "text", "content": "Invalid input."}}), 400
    
    response_data = chatbot.get_response(user_input)
    return jsonify({"response": response_data})

# Run the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
