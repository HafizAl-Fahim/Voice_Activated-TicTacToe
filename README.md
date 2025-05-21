# 🎮Accessible Voice-Activated Tic Tac Toe

**About It:**
An inclusive and interactive Tic Tac Toe game built with Python and Tkinter that allows users to play using voice commands, mouse clicks, or even claps to restart the game. Designed for both able-bodied and visually impaired players, this project combines speech recognition, text-to-speech, and sound-based gesture detection to ensure an accessible and fun experience for all.

![image](https://github.com/user-attachments/assets/034c967b-175e-476d-86ed-5588f78e0efe)


### **🚀 Features**
🎙️ Voice Command Support
Say positions like "top left" or "middle middle" to place your mark.

🗣️ Text-to-Speech Feedback
Announces each player's move, game status, and instructions clearly.

👆 Manual Interaction Support
Click on the board cells to play using the mouse.

 👏 Clap to Restart
After the game ends, clap once to start a new round.

♿ Accessibility Focused Design
Built with features that support visually impaired users.

### 📦 Requirements
Make sure Python 3 is installed, then install the necessary dependencies:
- pip install SpeechRecognition
- pip install pyaudio
- pip install pyttsx3
- pip install numpy

### 💡 If pyaudio installation fails on Windows:
- pip install pipwin
- pipwin install pyaudio

### 🛠️ Tech Stack
|Component|Purpose|
|Python3|Core Language|
|Tkinter|GUI Library| 
|SpeechRecognition|Capturing and processing voice commands|
|PyAudio|Microphone access & clap detection|
|pyttsx3|Offline text to speech|
|Numpy|Sound signal processing and clap detection|

### ▶️ How to Run
After installing all the dependencies, simply run:
- python voice_tic_tac_toe.py

### 🌱 Future Enhancements
🌍 Add multi-language support
🤖 Difficulty modes with an AI opponent
📊 Score tracking across sessions
🎵 Enhanced UI with sound effects and animations
