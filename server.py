from RyhBotPythonSDK import Message, Server
import Config
import GConfig
import env

Message.Token = env.Token
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
    chatId = data['chat']['chatId']
    if data['sender']['senderUserLevel'] != 'member':
        chatType = data['chat']['chatType']
        CmdName = data['message']['instructionName']

        if chatId == env.GroupId:
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

        if CmdName == '在容器中继续':
            GConfig.CheckExists(chatId)
            GConfig.StartListen(chatId)
            Send.Markdown(chatId, chatType, '容器已启动')

        if CmdName == '删除容器':
            GConfig.CheckExists(chatId)
            TargetMode = data['message']['content']['formJson']['uattua']['selectValue']
            if TargetMode == '删除容器':
                GConfig.StopListen(chatId)
                Send.Markdown(chatId, chatType, '删除成功, 消息保留')
            if TargetMode == '删除消息':
                MsgList = GConfig.ReadMsgList(chatId)
                for MsgId in MsgList:
                    Delete(MsgId, chatId, chatType)
                GConfig.StopListen(chatId)
                Send.Markdown(chatId, chatType, '删除成功, 消息撤回')

        if CmdName == '容器状态':
            GConfig.CheckExists(chatId)
            MsgList = GConfig.ReadMsgList(chatId)
            ContainerState = GConfig.ReadContainerState(chatId)
            rep_str = ''
            if ContainerState == True:
                rep_str+='容器正在运行, '
            if ContainerState == False:
                rep_str+='容器未在运行, '
            rep_str+=f'已容纳{len(MsgList)}条消息'
            Send.Markdown(chatId, chatType, rep_str)

    if data['sender']['senderUserLevel'] == 'member':
        if Config.BotState() == True:
            DelMessage(data)
        ContainerState = GConfig.ReadContainerState(chatId)
        if ContainerState == True:
            msgId = data['message']['msgId']
            GConfig.AddMessage(chatId, msgId)

@Server.Message.Normal
def DelMsg(data):
    chatId = data['chat']['chatId']
    GConfig.CheckExists(chatId)
    if Config.BotState() == True:
        DelMessage(data)
    ContainerState = GConfig.ReadContainerState(chatId)
    if ContainerState == True:
        msgId = data['message']['msgId']
        GConfig.AddMessage(chatId, msgId)

Server.Start(
    env.Host, env.Port, env.EnableDebug
)
