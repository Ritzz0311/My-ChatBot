# 🤖 Flask AI Chatbot

Welcome to the Flask AI Chatbot, an interactive and intelligent chatbot built with a Python/Flask backend and an HTML/JavaScript frontend. This bot integrates with external APIs to provide real-time information like the latest news, weather forecasts, jokes, and more.

## Chatbot Demo
![image](https://github.com/user-attachments/assets/af805307-ca33-4c5c-8133-21be5c44b775)



---

## ✨ Features

-   **Client-Server Architecture**: A robust backend powered by Flask that serves a clean HTML/CSS/JavaScript frontend.
-   **Real-time Weather**: Ask for the weather in any city (e.g., `"what's the weather in London?"`).
-   **Latest News Headlines**: Get the top technology headlines from The Guardian API.
-   **Tell Me a Joke**: Lighten the mood with a random joke from a joke API.
-   **Current Time & Date**: Ask for the current time or date.
-   **API Endpoints**: The backend exposes clear API endpoints for the frontend to communicate with.

---

## 🛠️ Tech Stack

-   **Backend**: Python, Flask
-   **Frontend**: HTML, CSS, JavaScript
-   **APIs**:
    -   [OpenWeatherMap](https://openweathermap.org/api) for weather data.
    -   [The Guardian](https://open-platform.theguardian.com/) for news headlines.
    -   [Official Joke API](https://github.com/15Dkatz/official_joke_api) for jokes.

---

## 🚀 How to Use: Setup and Running the Chatbot

Follow these instructions to get the project running on your local machine.

### Step 1: Clone the Repository

Open your terminal (CMD, PowerShell, etc.) and clone this repository:
```sh
git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
cd your-repository-name
```

### Step 2: Set Up the Project Environment

1.  **Create the Folder Structure** (if it doesn't exist)
    Your HTML file should be inside a folder named `templates`.
    ```sh
    mkdir templates
    # Now, move your HTML file into the 'templates' folder.
    ```

2.  **Install Dependencies**
    Install all the required Python libraries using the `requirements.txt` file:
    ```sh
    pip install -r requirements.txt
    ```

3.  **Add Your API Keys**
    Open the `app.py` file and find the placeholders for the API keys. Paste your keys directly into the file.
    > **Note**: This method is for development only. For production, it's better to use environment variables.
    ```python
    # Inside app.py
    GUARDIAN_API_KEY = "your_guardian_api_key_here"
    OPENWEATHERMAP_API_KEY = "your_openweathermap_api_key_here"
    ```

### Step 3: Run the Chatbot

1.  **Start the Flask Server**
    Run the `app.py` file from your terminal. This will start the backend server.
    ```sh
    python app.py
    ```
    You should see output indicating that the Flask server is running, usually on `http://127.0.0.1:5000`.

2.  **Open the Chatbot in Your Browser**
    Open your favorite web browser and navigate to the following address:
    ```
    [http://127.0.0.1:5000](http://127.0.0.1:5000)
    ```
    The Flask server will automatically load your `index.html` page. You do not need to open the HTML file manually.

### Step 4: Use Commands to Access the Bot

Now that the chatbot is loaded in your browser, you can start interacting with it. Type your messages into the input field and press Enter.

#### User Examples:

Try some of these commands to see the bot in action:

-   `"Hello"`
-   `"How are you?"`
-   `"What is the weather in Tokyo?"`
-   `"Tell me some news"`
-   `"Can you tell me a joke?"`
-   `"What time is it?"`
-   `"Bye"`

---

## 🤝 Contributing

Contributions are welcome! If you have ideas for new features or improvements, feel free to fork the repository, make your changes, and submit a pull request.

---

## 📄 License

This project is licensed under the MIT License.
