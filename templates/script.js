// script.js
document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const micBtn = document.getElementById('mic-btn');
    const chatWindow = document.getElementById('chat-window');

    const flaskApiUrl = 'http://127.0.0.1:5000/chat';

    // --- Event Listeners ---
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    micBtn.addEventListener('click', toggleSpeechRecognition);

    // Add initial bot message
    addMessageToWindow("Hello! I'm your friendly chatbot. How can I assist you today?", 'bot');

    // --- Functions ---
    function sendMessage() {
        const messageText = userInput.value.trim();
        if (messageText === '') return;

        addMessageToWindow(messageText, 'user');
        userInput.value = '';
        getBotResponse(messageText);
    }

    function addMessageToWindow(message, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);
        messageElement.textContent = message;
        chatWindow.appendChild(messageElement);
        chatWindow.scrollTop = chatWindow.scrollHeight; // Auto-scroll to the latest message
    }

    async function getBotResponse(userMessage) {
        try {
            const response = await fetch(flaskApiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userMessage }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            const botResponse = data.response;

            addMessageToWindow(botResponse, 'bot');
            // speak(botResponse); // Read the bot's response aloud
        } catch (error) {
            console.error('Error fetching bot response:', error);
            const errorMessage = "Sorry, I'm having trouble connecting to my brain right now. Please try again later.";
            addMessageToWindow(errorMessage, 'bot');
            // speak(errorMessage);
        }
    }

    function speak(text) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'en-US';
        window.speechSynthesis.speak(utterance);
    }

    // --- Web Speech API for Voice Recognition ---
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition;
    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.lang = 'en-US';

        recognition.onstart = () => {
            micBtn.classList.add('is-listening');
        };

        recognition.onend = () => {
            micBtn.classList.remove('is-listening');
        };

        recognition.onresult = (event) => {
            const current = event.resultIndex;
            const transcript = event.results[current][0].transcript;
            userInput.value = transcript;
            sendMessage();
        };

        recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            micBtn.classList.remove('is-listening');
        };
    } else {
        micBtn.style.display = 'none'; // Hide mic button if not supported
        console.log("Speech Recognition not supported in this browser.");
    }

    function toggleSpeechRecognition() {
        if (!recognition) return;

        if (micBtn.classList.contains('is-listening')) {
            recognition.stop();
        } else {
            recognition.start();
        }
    }
});
