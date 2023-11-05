from vosk import Model, KaldiRecognizer
from dotenv import load_dotenv
import pyaudio
import playsound
import requests
import json
from gtts import gTTS
from elevenlabs import generate, play
import os

# Load environment variables
load_dotenv()

# AI parameters
devmode = False
ai_name = "Laura" # Change this if needed
master_name = "Vincent" # Change this if needed
language = "French" # Change this if needed
api_url = os.getenv("API_URL")
sleep_time = 0.5  # Seconds to wait between requests (to avoid too much CPU usage)
elevenlabs = True # Set to True if you want to use the Eleven Labs API

# ELEVENLABS
elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
elevenlabs_model = "eleven_multilingual_v2"  # Change this if needed
elevenlabs_voice = "8NYXIvyXVhFEzg0Qgvh4"

# Load a lightweight model in dev mode for faster loading
model_name = "models/vosk-model-fr-0.22" # Download from https://alphacephei.com/vosk/models
if devmode:
    model_name = "models/vosk-model-small-fr-pguyot-0.3"
    ai_name = "Lucy"

# Load the model
model = Model(model_name)
recognizer = KaldiRecognizer(model, 16000)
print(f"{ai_name} is ready")

# Microphone stream configuration (change channels if needed)
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=16384)
stream.start_stream()

# Function to send user input to the local API
def send_request(input_text):
    headers = {"Content-Type": "application/json"}
    data = {
        "messages": [
            {
                "role": "system",
                "content": f"You are {ai_name}, an AI assistant created by {master_name} to help people. You respond ONLY in {language}. You are friendly and helpful, providing simple and quick sentences, and you never use emoji or emoticons or add a website link in response if not requested."
            },
            {"role": "user", "content": input_text}
        ],
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }
    response = requests.post(api_url, json=data, headers=headers)
    with open("response.json", "w") as file:
        file.write(response.text)
    return response.json()

# Print AI startup message
print(f"{ai_name} is listening...")
print("\033[91mSay", ai_name, "to activate\033[0m")
print("\033[91mSay Stop or Quit to stop the program\033[0m")

# Listen to the microphone in a continuous loop
while True:
    audio_data = stream.read(16384)
    if recognizer.AcceptWaveform(audio_data):
        text = json.loads(recognizer.Result())["text"]

        # Ignore empty text
        if not text:
            continue

        # Break if the user says "stop" or "quit"
        if text.lower() in ["stop", "quit"]:
            print(f"\033[91m{ai_name} stopped correctly.\033[0m")
            break

        # Show detected text
        print(f"\033[92mYou: {text}\033[0m")

        # If the text starts with the target name
        if text.split()[0].lower() == ai_name.lower():
            print(f"\033[94m{ai_name} is thinking...\033[0m")

            # Remove the target name from the text
            text = ' '.join(text.split()[1:])

            # Send text to the local API
            response_data = send_request(text)

            if 'choices' in response_data and response_data['choices']:
                local_response = response_data['choices'][0]['message']['content']
            else:
                local_response = f"\033[91m Error handling response from {ai_name} \033[0m"  # Error handling

            # Show the response from the local API
            print(f"\033[93m{ai_name} responded: {local_response}\033[0m")

            # Generate and play audio using Eleven Labs if configured
            if elevenlabs is True:
                audio = generate(local_response, voice=elevenlabs_voice, model=elevenlabs_model, api_key=elevenlabs_api_key)
                print("Eleven Labs generated audio...")
                play(audio)
            else:
                # Convert the response to TTS
                tts = gTTS(text=local_response, lang="fr", slow=False)
                print("TTS generated audio...")
                tts.save("response.mp3")

                # Play the response audio and clean up
                playsound.playsound("response.mp3")
                os.remove("response.mp3")
