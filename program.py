from TTS_Azure import azureTTS
from TTS_Eleven import elevenTTS
from GPT_Question import GPTQuestion
from caption import autoCaption
from srtgen import srtGen
from intro import OBSWebsocketsManager
from moviepy.editor import *
from pathConfig import get_default
import os
import uuid
import vlc
import time
import threading


default_path = get_default()
captioned_video = f'{default_path}/AIChatbot/mediaOutput/captionedVideo/{uuid.uuid4()}.mp3'
with open(f'{default_path}/AIChatbot/textFiles/question.txt', 'r') as f:
     question = f.read()
print(question)
with open(f"{default_path}/AIChatbot/textFiles/subtitle.srt", "w") as f:
        f.write(question)
#Sets base paths for files

#Runs all files that create the final output
audioQuestionPath = f"{azureTTS(question)}"
AIresponse = GPTQuestion(question)
audioResponsePath = f"{elevenTTS(AIresponse)}"

def audioThreading():
    player = vlc.MediaPlayer(f'{audioQuestionPath}')
    player.play()
    time.sleep(1)
    media_length = player.get_length() / 1000
    with open(f'{default_path}/AIChatbot/textFiles/delay.txt', 'w') as f:
            f.write(str(media_length))
    time.sleep(media_length)
    player.stop()
def get_most_recent_file(folder_path):
    # List all files in the directory with full path
    files = [os.path.join(folder_path, file) for file in os.listdir(folder_path)]
    
    # Filter out directories
    files = [file for file in files if os.path.isfile(file)]
    
    # Sort files by modification time in descending order
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    
    # Return the most recent file
    if files:
        return files[0]
    else:
        return None
def wipeFiles(file_path):
     for file in os.listdir(file_path):
          print(f"Removed File: {file}")
          os.remove(f"{file_path}/{file}")

# Example usage

import time
import sys
from obswebsocket import obsws, requests  # noqa: E402

host = 'localhost'
port = 4455
password = 'secret'

print("Connecting to OBS Websockets")
obswebsockets_manager = OBSWebsocketsManager()
time.sleep(10)
obswebsockets_manager.switch_scene("Intro")
obswebsockets_manager.applyFilter("Intro", "FratReset")
obswebsockets_manager.applyFilter("Intro", "Reset", True )
time.sleep(7)
obswebsockets_manager.startRecord()
print("record started")
time.sleep(1)
audioThread = threading.Thread(target=audioThreading)
videoThread = threading.Thread(target=obswebsockets_manager.introSequence)
audioThread.start()
videoThread.start()
audioThread.join()
videoThread.join()
obswebsockets_manager.stopRecord()
time.sleep(1)
obswebsockets_manager.startRecord()
obswebsockets_manager.applyFilter("Intro", "FratIntro")
time.sleep(1)
obswebsockets_manager.switch_scene("Scene")

player = vlc.MediaPlayer(f'{audioResponsePath}')
player.play()
time.sleep(1)
media_length = player.get_length() / 1000
time.sleep(media_length)
player.stop()
obswebsockets_manager.stopRecord()
obswebsockets_manager.disconnect()
time.sleep(3)
folder_path = f'{default_path}/AIChatbot/mediaOutput/preCaptionVid'
most_recent_file = get_most_recent_file(folder_path)
print(f"File to be captioned: {most_recent_file}")
time.sleep(5)
print("Captioning Started...")

srtGen(most_recent_file)
autoCaption(most_recent_file, f'{default_path}/AIChatbot/textFiles/subtitle.srt') 
os.remove(most_recent_file)
print("Captioning Success!")

most_recent_file = get_most_recent_file(folder_path)
clip1 = VideoFileClip(most_recent_file)
folder_path = f'{default_path}/AIChatbot/mediaOutput/captionedVideo'
most_recent_file = get_most_recent_file(folder_path)
clip2 = VideoFileClip(most_recent_file)
clips = [clip1, clip2]
final = concatenate_videoclips(clips, method="compose")
final.write_videofile(f'{default_path}/AIChatbot/mediaOutput/finalVideo/{uuid.uuid4()}.mp4')


os.remove(audioQuestionPath)
os.remove(audioResponsePath)
os.remove(most_recent_file)

wipeFiles(f"{default_path}/AIChatbot/mediaOutput/azureOutput")
wipeFiles(f"{default_path}/AIChatbot/mediaOutput/elevenOutput")
wipeFiles(f"{default_path}/AIChatbot/mediaOutput/captionedVideo")
wipeFiles(f"{default_path}/AIChatbot/mediaOutput/preCaptionVid")
