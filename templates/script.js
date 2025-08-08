
document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const micBtn = document.getElementById('mic-btn');
    const chatWindow = document.getElementById('chat-window');

    
    const flaskApiUrl = 'https://chatbot-back.up.railway.app/chat'; 

    // --- Event Listeners ---
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
    micBtn.addEventListener('click', toggleSpeechRecognition);

    addMessageToWindow({ type: 'text', content: "Hello! I'm your friendly chatbot. How can I assist you today?" }, 'bot');

    // --- Functions ---
    function sendMessage() {
        const messageText = userInput.value.trim();
        if (messageText === '') return;

        addMessageToWindow({ type: 'text', content: messageText }, 'user');
        userInput.value = '';
        getBotResponse(messageText);
    }

    function addMessageToWindow(response, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);

        if (response.type === 'youtube_link') {
            const textNode = document.createTextNode(response.text + ' ');
            messageElement.appendChild(textNode);

            const linkElement = document.createElement('a');
            linkElement.href = response.url;
            linkElement.textContent = "Click here to watch.";
            linkElement.target = "_blank";
            messageElement.appendChild(linkElement);
        } else {
            messageElement.textContent = response.content;
        }
        
        chatWindow.appendChild(messageElement);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    async function getBotResponse(userMessage) {
        try {
            const response = await fetch(flaskApiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMessage }),
            });

            if (!response.ok) {
                // This will create a more specific error message
                throw new Error(`Network response was not ok (status: ${response.status})`);
            }

            const data = await response.json();
            const botResponse = data.response; 

            addMessageToWindow(botResponse, 'bot');

        } catch (error) {
            console.error('Error fetching bot response:', error);
            // --- IMPROVED ERROR DISPLAY ---
            // This will now show the exact error in the chat window.
            const errorMessage = `Connection Error: ${error.message}. Please check the flaskApiUrl in the HTML file and ensure the backend server is running.`;
            addMessageToWindow({ type: 'text', content: errorMessage }, 'bot');
        }
    }

    // --- Web Speech API (No changes needed here) ---
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition;
    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.lang = 'en-US';
        recognition.onstart = () => micBtn.classList.add('is-listening');
        recognition.onend = () => micBtn.classList.remove('is-listening');
        recognition.onresult = (event) => {
            const transcript = event.results[event.resultIndex][0].transcript;
            userInput.value = transcript;
            sendMessage();
        };
        recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            micBtn.classList.remove('is-listening');
        };
    } else {
        micBtn.style.display = 'none';
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

