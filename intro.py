import time
import sys
from obswebsocket import obsws, requests
import os
from pathConfig import get_default
host = 'localhost'
port = 4455
password = 'secret'
default_path = get_default()
class OBSWebsocketsManager:
    def __init__(self):
        self.ws = obsws(host, port, password)
        try:
            self.ws.connect()
        except:
            print("error")
            time.sleep(3)
            sys.exit()
        print("Connected to OBS Websockets!\n")

    def disconnect(self):
        self.ws.disconnect()
    
    def switch_scene(self, scene_name):
        self.ws.call(requests.SetCurrentProgramScene(sceneName=scene_name))
    def get_text(self, source_name):
        response = self.ws.call(requests.GetInputSettings(inputName=source_name))
        return response.datain["inputSettings"]["text"]
    def set_text(self, source_name, new_text):
        self.ws.call(requests.SetInputSettings(inputName=source_name, inputSettings = {'text': new_text}))
    def applyFilter(self, scene_name, filter_name, filter_enabled=True):
        self.ws.call(requests.SetSourceFilterEnabled(sourceName=scene_name, filterName=filter_name, filterEnabled=filter_enabled))
    def create_source(self, source_name, source_kind, scene_name, file):
        source_settings = {
            "file": file
        }
        self.ws.call(requests.CreateInput(inputName=source_name, inputKind = source_kind, sceneName = scene_name, inputSettings = source_settings))
    def remove_source(self, source_name):
        self.ws.call(requests.RemoveInput(inputName=source_name))
    def setTransform(self, scene_name, source_name, new_transform):
        response = self.ws.call(requests.GetSceneItemId(sceneName=scene_name, sourceName=source_name))
        myItemID = response.datain['sceneItemId']
        self.ws.call(requests.SetSceneItemTransform(sceneName=scene_name, sceneItemId=myItemID, sceneItemTransform=new_transform))
    def setFilter(self, source_name, scene_name, filter_name):
        filter_settings = {
            "source": 'Test'
        }
        self.ws.call(requests.SetSourceFilterSettings(sourceName=scene_name, filterName=filter_name, filterSettings=filter_settings))
    def startRecord(self):
        self.ws.call(requests.StartRecord())
    def stopRecord(self):
        self.ws.call(requests.StopRecord())
    def introSequence(self):
        self.applyFilter("Intro", "FlyIn", True )
        time.sleep(1)
        with open(f"{default_path}/AIChatbot/textFiles/commentFile.txt", "r") as f:
            file = f.read()
        self.create_source("Test", "image_source", "Intro", file)
        self.setTransform("Intro", "Test", {"positionX": -1220, "positionY": 558, "scaleX": 1.413, "scaleY": 1.413})
        self.setFilter("Test", "Intro", "MoveTest")
        self.applyFilter("Intro", "MoveTest")
        with open(f'{default_path}/AIChatbot/textFiles/delay.txt', 'r') as f:
            delay = float(f.read())
        time.sleep(delay)
        self.setFilter("Test", "Intro", "MoveTest 2")
        self.applyFilter("Intro", "MoveTest 2")
        time.sleep(1)
        self.applyFilter("Intro", "Reset", True )
        time.sleep(1)
        self.remove_source("Test")