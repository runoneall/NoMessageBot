from RyhBotPythonSDK import Message, Server
import Config

Message.Token = ''
Send = Message.Send()
Delete = Message.Delete

def DelMessage(data:dict):
    chatId = data['chat']['chatId']
    chatType = data['chat']['chatType']
    senderId = data['sender']['senderId']
    msgId = data['message']['msgId']
    Mode = Config.BotMode()
    if Mode == 'Global':
        Delete(msgId, chatId, chatType)
    if Mode == 'BlackList':
        BlackLists = Config.ReadBlackList()
        if senderId in BlackLists:
            Delete(msgId, chatId, chatType)
    if Mode == 'WhiteList':
        WhiteLists = Config.ReadWhiteList()
        if senderId not in WhiteLists:
            Delete(msgId, chatId, chatType)

@Server.Message.Command
def CommandHandle(data):
    if data['sender']['senderUserLevel'] != 'member':
        chatId = data['chat']['chatId']
        chatType = data['chat']['chatType']
        CmdName = data['message']['instructionName']

        if CmdName == 'Ping':
            Send.Text(chatId, chatType, 'Pong')

        if CmdName == '启动':
            Config.RunBot()
            Send.Text(chatId, chatType, '已启动')

        if CmdName == '停止':
            Config.StopBot()
            Send.Text(chatId, chatType, '已停止')

        if CmdName == '状态':
            if Config.BotState() == True:
                Send.Text(chatId, chatType, '正在运行')
            else: Send.Text(chatId, chatType, '未运行')

        if CmdName == '模式':
            Mode = Config.BotMode()
            if Mode == 'Global':
                Send.Text(chatId, chatType, '全局模式')
            if Mode == 'BlackList':
                Send.Text(chatId, chatType, '黑名单模式')
            if Mode == 'WhiteList':
                Send.Text(chatId, chatType, '白名单模式')

        if CmdName == '模式切换':
            TargetMode = data['message']['content']['formJson']['pqefdg']['selectValue']
            if TargetMode == '全局':
                TargetMode = 'Global'
            if TargetMode == '黑名单':
                TargetMode = 'BlackList'
            if TargetMode == '白名单':
                TargetMode = 'WhiteList'
            Config.ChangeBotMode(TargetMode)
            Send.Text(chatId, chatType, '切换成功')

        if CmdName == '白名单':
            WhiteLists = Config.ReadWhiteList()
            if WhiteLists != []:
                rep = str()
                for WhiteList in WhiteLists:
                    rep += f"- {WhiteList} \n"
                Send.Markdown(chatId, chatType, rep)
            else: Send.Text(chatId, chatType, '没有条目')

        if CmdName == '黑名单':
            BlackLists = Config.ReadBlackList()
            if BlackLists != []:
                rep = str()
                for BlackList in BlackLists:
                    rep += f"- {BlackList} \n"
                Send.Markdown(chatId, chatType, rep)
            else: Send.Text(chatId, chatType, '没有条目')

        if CmdName == '白名单加':
            UserId = data['message']['content']['text']
            Config.WhiteListAdd(UserId)
            Send.Text(chatId, chatType, '加入成功')

        if CmdName == '白名单减':
            UserId = data['message']['content']['text']
            Config.WhiteListDelete(UserId)
            Send.Text(chatId, chatType, '删除成功')

        if CmdName == '黑名单加':
            UserId = data['message']['content']['text']
            Config.BlackListAdd(UserId)
            Send.Text(chatId, chatType, '加入成功')

        if CmdName == '黑名单减':
            UserId = data['message']['content']['text']
            Config.BlackListDelete(UserId)
            Send.Text(chatId, chatType, '删除成功')

    if data['sender']['senderUserLevel'] == 'member':
        if Config.BotState() == True:
            DelMessage(data)

@Server.Message.Normal
def DelMsg(data):
    if Config.BotState() == True:
        DelMessage(data)

Server.Start(
    'localhost', 8501, True
)