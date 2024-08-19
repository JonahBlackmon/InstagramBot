import assemblyai as aai
from dotenv import load_dotenv
import os
from pathConfig import get_default


def srtGen(filepath):
    default_path = get_default()
    load_dotenv()
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
    config = aai.TranscriptionConfig(disfluencies=True)
    file = filepath

    transcriber = aai.Transcriber(config=config)
    transcript = transcriber.transcribe(file)

    srt = transcript.export_subtitles_srt(chars_per_caption=25)

    with open(f"{default_path}/AIChatbot/textFiles/subtitle.srt", "w") as f:
        f.write(srt)
    print("Success")
