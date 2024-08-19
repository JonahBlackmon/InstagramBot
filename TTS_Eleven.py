from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
import os
import uuid
from pathConfig import get_default
#Loads and sets ElevenLabs API Key from Environment variable

def elevenTTS(str):
    default_path = get_default()
    load_dotenv()

    client = ElevenLabs(
        api_key = os.getenv('ELEVEN_KEY'),
    )

    response = client.text_to_speech.convert(
        voice_id="TX3LPaxmHKxFdv7VOQHJ",
        output_format="mp3_22050_32",
        text=str,
        voice_settings=VoiceSettings(
            stability=0.1,
            similarity_boost=0.3,
            style=0.7,
        ),
    )

    save_file_path = f"{default_path}/AIChatbot/mediaOutput/elevenOutput/{uuid.uuid4()}.mp3"

    with open(save_file_path, 'wb') as f:
        for chunk in response:
            if chunk:
                f.write(chunk)
    print(f"{save_file_path}: A new audio file was saved successfully!")
    return save_file_path
    


def callum(str):
    load_dotenv()

    client = ElevenLabs(
        api_key = os.getenv('ELEVEN_KEY'),
    )

    response = client.text_to_speech.convert(
        voice_id="N2lVS1w4EtoT3dr4eOWO",
        output_format="mp3_22050_32",
        text=str,
        voice_settings=VoiceSettings(
            stability=0.3,
            similarity_boost=0.75,
            style=0.5,
        ),
    )

    save_file_path = f"{uuid.uuid4()}.mp3"

    with open(save_file_path, 'wb') as f:
        for chunk in response:
            if chunk:
                f.write(chunk)
    print(f"{save_file_path}: A new audio file was saved successfully!")
    return save_file_path
