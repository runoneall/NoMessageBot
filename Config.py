import json

def Read() -> dict:
    with open('./Config.json', 'r', encoding='utf-8') as ConfigFile:
        return json.load(ConfigFile)
    
def Write(Content:dict):
    with open('./Config.json', 'w', encoding='utf-8') as ConfigFile:
        json.dump(Content, ConfigFile, ensure_ascii=False, indent=4)

def BotState() -> bool:
    State = Read()['State']
    if State == 'RUN':
        return True
    return False

def RunBot():
    Configs = Read()
    if BotState() == False:
        Configs['State'] = 'RUN'
        Write(Configs)

def StopBot():
    Configs = Read()
    if BotState() == True:
        Configs['State'] = 'STOP'
        Write(Configs)

def BotMode() -> str:
    return Read()['Mode']

def ChangeBotMode(TargetMode:str):
    Configs = Read()
    if Configs['Mode'] != TargetMode:
        Configs['Mode'] = TargetMode
        Write(Configs)

def ReadWhiteList() -> list:
    Configs = Read()
    return Configs['WhiteList']

def ReadBlackList() -> list:
    Configs = Read()
    return Configs['BlackList']

def WriteWhiteList(Content:list):
    Configs = Read()
    Configs['WhiteList'] = Content
    Write(Configs)

def WriteBlackList(Content:list):
    Configs = Read()
    Configs['BlackList'] = Content
    Write(Configs)

def WhiteListAdd(UserId:str):
    OldList = ReadWhiteList()
    merged_list = OldList + [UserId]
    unique_list = list(set(merged_list))
    WriteWhiteList(unique_list)

def WhiteListDelete(UserId:str):
    WhiteList = ReadWhiteList()
    if UserId in WhiteList:
        del WhiteList[WhiteList.index(UserId)]
        WriteWhiteList(WhiteList)

def BlackListAdd(UserId:str):
    OldList = ReadBlackList()
    merged_list = OldList + [UserId]
    unique_list = list(set(merged_list))
    WriteBlackList(unique_list)

def BlackListDelete(UserId:str):
    BlackList = ReadBlackList()
    if UserId in BlackList:
        del BlackList[BlackList.index(UserId)]
        WriteBlackList(BlackList)