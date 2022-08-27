import json

token = None
serverIp = None
rconPort = None
rconPassword = None
discordInfo = None


def init():
    global token
    global serverIp
    global rconPort
    global rconPassword
    global discordInfo
    f = open("data.json", "r")
    jsonData = json.loads(f.read())
    token = jsonData['Bot_Token']
    serverIp = jsonData["Server_Ip"]
    rconPort = int(jsonData["Server_Port"])
    rconPassword = jsonData["Rcon_Password"]
    f.close()
    f = open("serverInfo.json", "r")
    discordInfo = json.loads(f.read())
    f.close()


def updateServerInfo():
    global discordInfo
    f = open("serverInfo.json", "w")
    f.write(json.dumps(discordInfo))
    f.close()


def setRole():
    pass


def setChannel(channel):
    global discordInfo
    discordInfo["channelId"] = channel
    updateServerInfo()
    pass
