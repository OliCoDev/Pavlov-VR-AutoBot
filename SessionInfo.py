import json

token = None
serverIp = None
rconPort = None
rconPassword = None


def init():
    global token
    global serverIp
    global rconPort
    global rconPassword
    f = open("data.json", "r")
    jsonData = json.loads(f.read())
    token = jsonData['Bot_Token']
    serverIp = jsonData["Server_Ip"]
    rconPort = int(jsonData["Server_Port"])
    rconPassword = jsonData["Rcon_Password"]
    f.close()
