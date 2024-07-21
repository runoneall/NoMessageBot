import json
import os

def CheckExists(chatId:str):
    ConfigFilePath = f'./GroupConfig/{chatId}.json'
    if not os.path.exists(ConfigFilePath):
        with open(ConfigFilePath, 'w', encoding='utf-8') as ConfigFile:
            ConfigFile.write('''{
    "in_container": false,
    "Messages": []
}''')
            
def Read(chatId:str) -> dict:
    ConfigFilePath = f'./GroupConfig/{chatId}.json'
    with open(ConfigFilePath, 'r', encoding='utf-8') as ConfigFile:
        return json.load(ConfigFile)
            
def Write(chatId:str, Content:dict):
    ConfigFilePath = f'./GroupConfig/{chatId}.json'
    with open(ConfigFilePath, 'w', encoding='utf-8') as ConfigFile:
        json.dump(Content, ConfigFile, ensure_ascii=False, indent=4)

def ReadMsgList(chatId:str) -> list:
    return Read(chatId)['Messages']

def ReadContainerState(chatId:str) -> bool:
    return Read(chatId)['in_container']

def StartListen(chatId:str):
    ConfigContent = Read(chatId)
    if ConfigContent['in_container'] == False:
        ConfigContent['in_container'] = True
        ConfigContent['Messages'] = []
        Write(chatId, ConfigContent)

def StopListen(chatId:str):
    ConfigContent = Read(chatId)
    if ConfigContent['in_container'] == True:
        ConfigContent['in_container'] = False
        ConfigContent['Messages'] = []
        Write(chatId, ConfigContent)

def AddMessage(chatId:str, msgId:str):
    ConfigContent = Read(chatId)
    MsgList = ConfigContent['Messages']
    MsgList.append(msgId)
    ConfigContent['Messages'] = MsgList
    Write(chatId, ConfigContent)