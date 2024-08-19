import azure.cognitiveservices.speech as speechsdk
import random
import uuid
import os
from pathConfig import get_default
from dotenv import load_dotenv
def azureTTS(userQuestion):
    
    default_path = get_default()
    load_dotenv()
    azure_key = os.getenv("AZURE_KEY")
    azure_region = os.getenv("AZURE_REGION")
    question = userQuestion
    styles = ['angry', 'cheerful', 'excited', 'friendly', 'hopeful', 'sad', 'shouting', 'terrified', 'unfriendly', 'whispering']

    # Creates an instance of a speech config with specified subscription key and service region.
    speech_key, service_region = azure_key, azure_region
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)


    
    voices = ['en-US-DavisNeural','en-US-JaneNeural']
    voice = voices[random.randint(0, len(voices) - 1)]

    file_path = f"{default_path}/AIChatbot/mediaOutput/azureOutput/{uuid.uuid4()}.mp3"

    if voice == 'en-US-DavisNeural':
        style = 'cheerful'
    else:
        style = 'hopeful'

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    ssml_string = f"""
    <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
            <voice name='{voice}' style='{style}'>
                <prosody rate='0%' pitch='0%'>
                    <s> Today's question: {question} </s>
                </prosody>
            </voice>
        </speak>
        """
    result = speech_synthesizer.speak_ssml_async(ssml_string).get()

    stream = speechsdk.AudioDataStream(result)
    stream.save_to_wav_file(file_path)
    print(f"Voice: {voice} Style: {style}")
    return file_path
    
