import SessionInfo
import threading
import hashlib
import asyncio
import socket
import json
import RequestList
from pavlovEnums import RequestTypes
import MapsList
import time

thread1 = None
thread2 = None
connectionSocket = None
mapSwitched = False
nextMap = False
canContinue = True


def getPlayerCount(inString):
    countString = inString.split("/")[0]
    return int(countString)


async def updateMapLists():
    for i in RequestList.requests:
        if i.requestType == RequestTypes.MAPSLIST:
            await i.requestInfo.updateMessage()

def updateListsAsyncThread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(updateMapLists())
    loop.close()

def switchMap():
    global connectionSocket
    global mapSwitched
    nextMap = MapsList.getMap()
    if nextMap:
        print("Switching map to:", nextMap.id)
        message = "SwitchMap UGC" + str(nextMap.id) + " " + nextMap.gamemode
        connectionSocket.sendall(message.encode('utf-8'))
        mapSwitched = True
        tempThread = threading.Thread(target=updateListsAsyncThread, args=())
        tempThread.start()


def socketReception():
    global connectionSocket
    global nextMap
    global canContinue
    while True:
        continueReception = True
        message = ""
        while continueReception:
            data = connectionSocket.recv(1024)
            message += data.decode('utf-8')
            if len(data) < 1024:
                continueReception = False
        if len(message) > 20:
            if not canContinue:
                continue
            try:
                messageJson = json.loads(message)
                if nextMap:
                    nextMap = False
                    switchMap()
                    continue
                if (messageJson['Command'] == "ServerInfo") and messageJson['Successful']:
                    if ((messageJson['ServerInfo']['MapLabel'] == 'datacenter') or
                            (messageJson['ServerInfo']['MapLabel'] == 'sand')) and \
                            messageJson['ServerInfo']['GameMode'] == 'DM' and \
                            (getPlayerCount(messageJson['ServerInfo']['PlayerCount']) > 0):
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

