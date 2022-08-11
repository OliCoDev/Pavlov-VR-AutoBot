import SessionInfo
import threading
import hashlib
import socket
import json
import MapsList
import time

thread1 = None
thread2 = None
connectionSocket = None
mapSwitched = False


def switchMap():
    global connectionSocket
    global mapSwitched
    nextMap = MapsList.getMap()
    if nextMap:
        print("Switching map to:", nextMap.id)
        message = "SwitchMap UGC" + str(nextMap.id) + " " + nextMap.gamemode
        connectionSocket.sendall(message.encode('utf-8'))
        mapSwitched = True


def socketReception():
    global connectionSocket
    lastMessage = None
    while True:
        continueReception = True
        message = ""
        while continueReception:
            data = connectionSocket.recv(1024)
            message += data.decode('utf-8')
            if len(data) < 1024:
                continueReception = False
        if len(message) > 20:
            try:
                messageJson = json.loads(message)
                if lastMessage != messageJson:
                    print(messageJson)
                    lastMessage = messageJson
                if messageJson['Command'] == "ServerInfo":
                    if ((messageJson['ServerInfo']['MapLabel'] == 'datacenter') or (messageJson['ServerInfo']['MapLabel'] == 'sand')) and messageJson['ServerInfo']['GameMode'] == 'DM':
                        switchMap()
            finally:
                pass


def checkMapInfo():
    global connectionSocket
    global mapSwitched
    while True:
        if mapSwitched:
            mapSwitched = False
            time.sleep(180)
        connectionSocket.sendall("ServerInfo".encode('utf-8'))
        time.sleep(1)


def init():
    global thread1
    global thread2
    global connectionSocket
    serverIp = SessionInfo.serverIp
    port = SessionInfo.rconPort
    password = SessionInfo.rconPassword

    connectionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connectionSocket.connect((serverIp, port))
    data = connectionSocket.recv(1024)
    connectionSocket.sendall(hashlib.md5(password.encode('utf-8')).hexdigest().encode('utf-8'))
    data = connectionSocket.recv(1024)

    thread1 = threading.Thread(target=socketReception, args=())
    thread1.start()
    thread2 = threading.Thread(target=checkMapInfo, args=())
    thread2.start()

