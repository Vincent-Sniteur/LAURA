# Imports
import os
import json
import pyaudio
import requests
from gtts import gTTS
import playsound
from vosk import Model, KaldiRecognizer
from dotenv import load_dotenv
from elevenlabs import generate, play

# Load environment variables from .env file
load_dotenv()

# AI parameters
dev_mode = False
ai_name = "Laura"
master_name = "Vincent"
language = "French"
api_url = os.getenv("API_URL")
sleep_time = 0.5
elevenlabs = True
elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
elevenlabs_model = "eleven_multilingual_v2"
elevenlabs_voice = "8NYXIvyXVhFEzg0Qgvh4"
model_name = "models/vosk-model-fr-0.22"  # Download from https://alphacephei.com/vosk/models

# Load VOSK Model
model = Model(model_name)
recognizer = KaldiRecognizer(model, 16000)
print(f"{ai_name} is ready")

# Microphone stream configuration (change channels if needed)
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=16384)
stream.start_stream()

# Generate memory from past exchanges
def generate_exchange_memory(exchanges):
    exchange_memory = ""
    for exchange in exchanges:
        exchange_memory += f"User: {exchange['user_question']}\n"
        exchange_memory += f"{ai_name}: {exchange['assistant_response']}\n"
    return exchange_memory

# Send request to API and save response
def send_request(input_text, exchanges, include_exchange_memory=False):
    headers = {"Content-Type": "application/json"}
    exchange_memory = generate_exchange_memory(exchanges) if include_exchange_memory else ""
    data = {
        "messages": [
            {
                "role": "system",
                "content": f"You are {ai_name}, an AI assistant created by {master_name} to help people. You respond ONLY in {language}. You are friendly and helpful, providing simple and quick sentences, and you never use emoji or emoticons or add a website link in response if not requested. {'' if include_exchange_memory else 'The memory of my past exchanges is disabled.'}\n{exchange_memory}\nand allows me to learn."
            },
            {"role": "user", "content": input_text}
        ],
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }
    response = requests.post(api_url, json=data, headers=headers)
    response_text = response.json()
    exchanges.append({"user_question": input_text, "assistant_response": response_text})
    with open("response.json", "w") as file:
        json.dump(exchanges, file, ensure_ascii=False, indent=4)
    return response_text

# AI Starting message
print(f"{ai_name} is listening...")
print("\033[91mSay", ai_name, "to activate\033[0m")
print("\033[91mSay Stop to shut down the program\033[0m")

# List to store exchanges
exchanges = []

# Listen to the microphone in a continuous loop
while True:
    audio_data = stream.read(16384)
    if recognizer.AcceptWaveform(audio_data):
        text = json.loads(recognizer.Result())["text"]

        if not text:
            continue

        # Stop the program when the user says "stop"
        if text.lower() in ["stop"]:
            print(f"\033[91m{ai_name} stopped correctly.\033[0m")
            break

        print(f"\033[92mYou: {text}\033[0m")

        # Check if the user is talking to the AI
        if text.split()[0].lower() == ai_name.lower():
            print(f"\033[94m{ai_name} is thinking...\033[0m")
            text = ' '.join(text.split()[1:])
            response_data = send_request(text, exchanges)

            # Handle response from API
            if 'choices' in response_data and response_data['choices']:
                local_response = response_data['choices'][0]['message']['content']
            else:
                local_response = f"\033[91m Error handling response from {ai_name} \033[0m"
            print(f"\033[93m{ai_name} responded: {local_response}\033[0m")

            exchanges.append({"user_question": text, "assistant_response": local_response})

            # Generate audio with Eleven Labs or TTS
            if elevenlabs is True:
                audio = generate(local_response, voice=elevenlabs_voice, model=elevenlabs_model, api_key=elevenlabs_api_key)
                print("Eleven Labs generated audio...")
                play(audio)
            else:
                tts = gTTS(text=local_response, lang="fr", slow=False)
                print("TTS generated audio...")
                tts.save("response.mp3")
                playsound.playsound("response.mp3")
                os.remove("response.mp3")
