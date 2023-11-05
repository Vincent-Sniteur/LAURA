# LAURA - Your Local AI Voice Dialog Assistant 🗣️🤖📢

![LAURA Logo](https://i.imgur.com/WYEdMmE.jpeg)

## Introduction

LAURA is a local AI voice dialog assistant designed to help you with various tasks using natural language processing. 
This README provides an overview of the software and instructions on how to get it up and running.

## Features

- **ElevenLab Voice:** LAURA can use the powerful ElevenLab API to generate natural-sounding voices for a more interactive experience.
- **Store Exchange:** LAURA saves every exchange with the user. ( Not recommended, creates latency )

## Getting Started

Follow these steps to set up and run LAURA on your system:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Vincent-Sniteur/LAURA.git
    ```
2. **Move to the Project Folder:**

   ```bash
   cd LAURA
   ```
3. **Download VOSK Models:**

   - Download the necessary models from [alphacephei.com/vosk/models](https://alphacephei.com/vosk/models).
   - Add the downloaded models to the "Models" folder in the project.
   - Make sure to update the model name in the 'model_name' function in the code. For example, if you downloaded "vosk-model-fr-0.22," set the 'model_name' accordingly.

4. **Install the Requirements:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Config .Env**
   - Edit `exemple.env` to `.env`
   - Add your API URL
   - ***Optional:*** Add API Key for Elevenlabs (https://elevenlabs.io)

6. **Launch LAURA:**
   ```bash
   python laura.py
   ```

7. **Local API Server & Models:**

   - To enhance LAURA's capabilities, you can use a local API server. We recommend [lmstudio.ai](https://lmstudio.ai/) for this purpose. It provides additional features and better interaction.
   - For the model to use, look for the one that will be best for your needs. The one I use: Yarn-Mistral-7B-128k

## Development To-Do ( before 2023 )
- Character File
- Telegram Bot API
- Twitch Chat Read
- Monologue Mode

## License

This software is released under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributions

Contributions and feedback are welcome! If you have ideas, improvements, or bug reports, please open an issue or submit a pull request.
[Issue](https://github.com/Vincent-Sniteur/LAURA/issues).

## Author

- [Vincent Sniteur](https://github.com/Vincent-Sniteur)


Happy chatting with LAURA 🚀
