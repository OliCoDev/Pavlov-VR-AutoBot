import hashlib
from math import nextafter
import random
import requests
import discord
import threading
import socket
import json
import time
import os

def tagToGameMode(tag):
    switcher = {
        "Deathmatch": "DM",
        "Team Deathmatch": "TDM",
        "Search and Destroy": "SND",
        "Gun Game": "GUN",
        "Capture the Flag": "CTF",
        "TTT": "TTT",
        "Zombie Coop": "ZWV",
        "Custom": "CUSTOM",
        "PUSH": "PUSH",
        "Hide": "HIDE",
        "Prop Hunt": "PH"
    }
    return switcher.get(tag)

def intToReaction(inInt):
    switcher = {
        0: "0️⃣",
        1: "1️⃣",
        2: "2️⃣",
        3: "3️⃣",
        4: "4️⃣",
        5: "5️⃣",
        6: "6️⃣",
        7: "7️⃣",
        8: "8️⃣",
        9: "9️⃣",
        10: "🔟"
    }
    return switcher.get(inInt)

def reactToInt(inEmote):
    switcher = {
        "0️⃣": 0,
        "1️⃣": 1,
        "2️⃣": 2,
        "3️⃣": 3,
        "4️⃣": 4,
        "5️⃣": 5,
        "6️⃣": 6,
        "7️⃣": 7,
        "8️⃣": 8,
        "9️⃣": 9,
        "🔟": 10
    }
    return switcher.get(inEmote)

class map:
    def __init__(self, mapId, tags = []) -> None:
        self.mapId = mapId
        self.tags = tags
        self.gameMode = None
        pass
    
    def selectGameMode(self, inGameMode):
        if self.gameMode != None:
            return True
        if (inGameMode in self.tags) or (len(self.tags) == 0):
            self.gameMode = tagToGameMode(inGameMode)
            return True
        return False

class mapsList:
    maps = []

    def getMap(self):
        if len(self.maps) == 0:
            return None
        return self.maps.pop(0)

    def addMap(self,addedMap):
        self.maps.append(addedMap)

    def addList(self,addedList):
        for i in addedList:
            self.maps.append(i)
    
    def randomiseOrder(self):
        for i in range(len(self.maps)):
            randomPos = random.randint(0, len(self.maps)-1)
            tempMap = self.maps[randomPos]
            self.maps[randomPos] = self.maps[i]
            self.maps[i] = tempMap

class collection:
    def __init__(self, fileIds) -> None:
        self.maps = []
        self.fileIds = fileIds
        pass

    def addMap(self, inGameMode):
        tempMap = map(self.fileIds.pop(0), [])
        tempMap.selectGameMode(inGameMode)
        self.maps.append(tempMap)

    def getFirstMapId(self):
        while len(self.fileIds) > 0:
            r = requests.post("https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/", data = {"itemcount": 1, "publishedfileids[0]": self.fileIds[0]})
            mapData = json.loads(r.content)['response']['publishedfiledetails'][0]
            if mapData["creator_app_id"] == 555160:
                return self.fileIds[0]
            self.fileIds.pop(0)
        return -1

class userRequest:
    def __init__(self, author, requestType):
        self.author = author
        self.requestType = requestType
        self.messageId = -1
        self.requestInfo = None
        pass

    def setMessage(self, newMessageId):
        self.messageId = newMessageId

    def setRequestInfo(self, newInfo):
        if self.requestInfo != None:
            return
        self.requestInfo = newInfo

def getRequestId(inputUrl):
    splitUrl = inputUrl.split("?")
    if len(splitUrl) <= 1:
        return None
    parameters = splitUrl[1]
    splitParameters = parameters.split("&")
    for i in splitParameters:
        splitData = i.split("=")
        if (len(splitData) > 1) and (splitData[0] == "id"):
            return int(splitData[1])
    return None

def getImageName():
    global imageNumber
    imageNumber += 1
    if imageNumber == 101:
        imageNumber = 0
    return imageNumber

async def requestMap(message):
    args = message.content.split(" ")
    await message.delete()
    if len(args) <= 1:
        await message.channel.send(message.author.mention + "\nPlease make a request with a steam workshop url")
        return
    mapId = getRequestId(args[1])
    if mapId == None:
        await message.channel.send(message.author.mention + "\nPlease request a valid steam workshop url")
        return
    r = requests.post("https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/", data = {"itemcount": 1, "publishedfileids[0]": mapId})
    requestData = json.loads(r.content)['response']['publishedfiledetails'][0]
    if requestData["result"] != 1:
        await message.channel.send(message.author.mention + "\nThe url you have inputed did not correlate to a steam item")
        return
    if requestData["creator_app_id"] != 555160:
        await message.channel.send(message.author.mention + "\nThe request you have made was not a valid Pavlov VR Map")
        return
    tags = []
    for i in requestData["tags"]:
        tags.append(i["tag"])
    if len(tags) == 0: 
        tags = ["Deathmatch", "Team Deathmatch", "Search and Destroy", "Gun Game", "Capture the Flag", "TTT", "Zombie Coop", "Custom", "PUSH", "Hide", "Prop Hunt"]
    newMap = map(requestData["publishedfileid"],tags)
    if len(tags) != 1:
        newRequest = userRequest(message.author.id, True)
        newRequest.setRequestInfo(newMap)
        messageResponse = message.author.mention + "\nPlease select what gamemode you would like to play on " + requestData["title"] + ":\n"
        for i in range(len(tags)):
            messageResponse += intToReaction(i) + ": " + tags[i] + "\n"
        newMessage = None
        if len(requestData["preview_url"]) == 0:
            newMessage = await message.channel.send(messageResponse)
        else:
            curImageNum = getImageName()
            imageName = "image" + str(curImageNum) + ".png"
            r = requests.get(requestData["preview_url"])
            f = open(imageName, "wb")
            f.write(r.content)
            f.close()
            newMessage = await message.channel.send(messageResponse, file = discord.File(r".\\" + imageName))
        for i in range(len(tags)):
            await newMessage.add_reaction(intToReaction(i))
        newRequest.setMessage(newMessage.id)
        global userRequests
        userRequests.append(newRequest)
        pass
    else:
        newMap.selectGameMode(tags[0])
        if len(requestData["preview_url"]) == 0:
            await message.channel.send("Map " + requestData["title"] + " has been added with the gamemode set as " + tags[0])
        else:
            curImageNum = getImageName()
            imageName = "image" + str(curImageNum) + ".png"
            r = requests.get(requestData["preview_url"])
            f = open(imageName, "wb")
            f.write(r.content)
            f.close()
            await message.channel.send("Map " + requestData["title"] + " has been added with the gamemode set as " + tags[0], file = discord.File(r".\\" + imageName))
            os.remove(r".\\" + imageName)
        global curMapList
        curMapList.addMap(newMap)

async def mapReacted(reaction, requestId):
    global curMapList
    global userRequests
    await reaction.message.delete()
    tagNumber = reactToInt(reaction.emoji)
    userRequests[requestId].requestInfo.selectGameMode(userRequests[requestId].requestInfo.tags[tagNumber])
    r = requests.post("https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/", data = {"itemcount": 1, "publishedfileids[0]": userRequests[requestId].requestInfo.mapId})
    requestData = json.loads(r.content)['response']['publishedfiledetails'][0]
    if len(requestData["preview_url"]) == 0:
        await reaction.message.channel.send("Map " + requestData["title"] + " has been added with the gamemode set as " + userRequests[requestId].requestInfo.tags[tagNumber])
    else:
        curImageNum = getImageName()
        imageName = "image" + str(curImageNum) + ".png"
        r = requests.get(requestData["preview_url"])
        f = open(imageName, "wb")
        f.write(r.content)
        f.close()
        await reaction.message.channel.send("Map " + requestData["title"] + " has been added with the gamemode set as " + userRequests[requestId].requestInfo.tags[tagNumber], file = discord.File(r".\\" + imageName))
        os.remove(r".\\" + imageName)
    curMapList.addMap(userRequests.pop(requestId).requestInfo)
    pass

async def collectionPrintList(channel, mapList):
    messageOutput = "Added:\n"
    for i in  mapList:
        r = requests.post("https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/", data = {"itemcount": 1, "publishedfileids[0]": i.mapId})
        requestData = json.loads(r.content)['response']['publishedfiledetails'][0]
        title = requestData["title"]
        messageOutput += "-" + title + " with gamemode " + i.gameMode + "\n"
    await channel.send(messageOutput)
    pass

async def requestCollection(message):
    args = message.content.split(" ")
    await message.delete()
    if len(args) <= 1:
        await message.channel.send(message.author.mention + "\nPlease make a request with a steam workshop url")
        return
    collectionId = getRequestId(args[1])
    if collectionId == None:
        await message.channel.send(message.author.mention + "\nPlease request a valid steam workshop url")
        return
    r = requests.post("https://api.steampowered.com/ISteamRemoteStorage/GetCollectionDetails/v1/", data = {"collectioncount": 1, "publishedfileids[0]": collectionId} )
    collectionData = json.loads(r.content)["response"]["collectiondetails"][0]
    if collectionData["result"] != 1:
        await message.channel.send(message.author.mention + "\nThe url you have inputed did not correlate to a steam collection")
        return
    collectionItemsIds = []
    for i in collectionData["children"]:
        collectionItemsIds.append(i["publishedfileid"])
    newCollection = collection(collectionItemsIds)
    newRequest = userRequest(message.author.id, False)
    newRequest.setRequestInfo(newCollection)
    mapId = newRequest.requestInfo.getFirstMapId()
    if mapId == -1:
        await message.channel.send(message.author.mention + "\nPlease request a collection with Pavlov maps")
        return
    r = requests.post("https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/", data = {"itemcount": 1, "publishedfileids[0]": mapId})
    requestData = json.loads(r.content)['response']['publishedfiledetails'][0]
    tags = []
    for i in requestData["tags"]:
        tags.append(i["tag"])
    if len(tags) == 0: 
        tags = ["Deathmatch", "Team Deathmatch", "Search and Destroy", "Gun Game", "Capture the Flag", "TTT", "Zombie Coop", "Custom", "PUSH", "Hide", "Prop Hunt"]
    if len(tags) != 1:
        messageResponse = message.author.mention + "\nPlease select what gamemode you would like to play on " + requestData["title"] + ":\n"
        for i in range(len(tags)):
            messageResponse += intToReaction(i) + ": " + tags[i] + "\n"
        newMessage = None
        if len(requestData["preview_url"]) == 0:
            newMessage = await message.channel.send(messageResponse)
        else:
            curImageNum = getImageName()
            imageName = "image" + str(curImageNum) + ".png"
            r = requests.get(requestData["preview_url"])
            f = open(imageName, "wb")
            f.write(r.content)
            f.close()
            newMessage = await message.channel.send(messageResponse, file = discord.File(r".\\" + imageName))
        for i in range(len(tags)):
            await newMessage.add_reaction(intToReaction(i))
        newRequest.setMessage(newMessage.id)
        pass
    else:
        newRequest.requestInfo.addMap(tags[0])
        while True:
            mapId = newRequest.requestInfo.getFirstMapId()
            if mapId == -1:
                global curMapList
                curMapList.addList(newRequest.requestInfo.maps)
                await collectionPrintList(message.channel ,newRequest.requestInfo.maps)
                return
            r = requests.post("https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/", data = {"itemcount": 1, "publishedfileids[0]": mapId})
            requestData = json.loads(r.content)['response']['publishedfiledetails'][0]
            tags = []
            for i in requestData["tags"]:
                tags.append(i["tag"])
            if len(tags) == 0: 
                tags = ["Deathmatch", "Team Deathmatch", "Search and Destroy", "Gun Game", "Capture the Flag", "TTT", "Zombie Coop", "Custom", "PUSH", "Hide", "Prop Hunt"]
            if len(tags) != 1:
                messageResponse = message.author.mention + "\nPlease select what gamemode you would like to play on " + requestData["title"] + ":\n"
                for i in range(len(tags)):
                    messageResponse += intToReaction(i) + ": " + tags[i] + "\n"
                newMessage = None
                if len(requestData["preview_url"]) == 0:
                    newMessage = await message.channel.send(messageResponse)
                else:
                    curImageNum = getImageName()
                    imageName = "image" + str(curImageNum) + ".png"
                    r = requests.get(requestData["preview_url"])
                    f = open(imageName, "wb")
                    f.write(r.content)
                    f.close()
                    newMessage = await message.channel.send(messageResponse, file = discord.File(r".\\" + imageName))
                for i in range(len(tags)):
                    await newMessage.add_reaction(intToReaction(i))
                newRequest.setMessage(newMessage.id)
                break
            else:
                newRequest.requestInfo.addMap(tags[0])
    global userRequests
    userRequests.append(newRequest)

def getMapTags(id):
    r = requests.post("https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/", data = {"itemcount": 1, "publishedfileids[0]": id})
    requestData = json.loads(r.content)['response']['publishedfiledetails'][0]
    tags = []
    for i in requestData["tags"]:
        tags.append(i["tag"])
    if len(tags) == 0: 
        tags = ["Deathmatch", "Team Deathmatch", "Search and Destroy", "Gun Game", "Capture the Flag", "TTT", "Zombie Coop", "Custom", "PUSH", "Hide", "Prop Hunt"]
    return tags

async def collectionReacted(reaction, requestId):
    global curMapList
    global userRequests
    await reaction.message.delete()
    tagNumber = reactToInt(reaction.emoji)
    tags = getMapTags(userRequests[requestId].requestInfo.getFirstMapId())
    userRequests[requestId].requestInfo.addMap(tags[tagNumber]) 
    while True:
        mapId = userRequests[requestId].requestInfo.getFirstMapId()
        if mapId == -1:
            global curMapList
            curMapList.addList(userRequests[requestId].requestInfo.maps)
            await collectionPrintList(reaction.message.channel ,userRequests[requestId].requestInfo.maps)
            userRequests.pop(requestId)
            return
        r = requests.post("https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/", data = {"itemcount": 1, "publishedfileids[0]": mapId})
        requestData = json.loads(r.content)['response']['publishedfiledetails'][0]
        tags = []
        for i in requestData["tags"]:
            tags.append(i["tag"])
        if len(tags) == 0: 
            tags = ["Deathmatch", "Team Deathmatch", "Search and Destroy", "Gun Game", "Capture the Flag", "TTT", "Zombie Coop", "Custom", "PUSH", "Hide", "Prop Hunt"]
        if len(tags) != 1:
            messageResponse = "<@" + str(userRequests[requestId].author) + ">\nPlease select what gamemode you would like to play on " + requestData["title"] + ":\n"
            for i in range(len(tags)):
                messageResponse += intToReaction(i) + ": " + tags[i] + "\n"
            newMessage = None
            if len(requestData["preview_url"]) == 0:
                newMessage = await reaction.message.channel.send(messageResponse)
            else:
                curImageNum = getImageName()
                imageName = "image" + str(curImageNum) + ".png"
                r = requests.get(requestData["preview_url"])
                f = open(imageName, "wb")
                f.write(r.content)
                f.close()
                newMessage = await reaction.message.channel.send(messageResponse, file = discord.File(r".\\" + imageName))
            for i in range(len(tags)):
                await newMessage.add_reaction(intToReaction(i))
            userRequests[requestId].setMessage(newMessage.id)
            break
        else:
            userRequests[requestId].requestInfo.addMap(tags[0])

curMapList = mapsList()
userRequests = []
imageNumber = 0
mapSwitched = False

f = open("data.json", "r")
jsonData = json.loads(f.read())
token = jsonData['Bot_Token']
serverIp = jsonData["Server_Ip"]
serverPort = int(jsonData["Server_Port"])
rconPassword = jsonData["Rcon_Password"]
f.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((serverIp,serverPort))
data = s.recv(1024)
s.sendall(hashlib.md5(rconPassword.encode('utf-8')).hexdigest().encode('utf-8'))
data = s.recv(1024)

def switchMap():
    global curMapList
    global s
    nextMap = curMapList.getMap()
    if nextMap:
        print("Switching map to:", nextMap.mapId)
        message = "SwitchMap UGC" + str(nextMap.mapId) + " " + nextMap.gameMode
        s.sendall(message.encode('utf-8'))

def socketReception():
    global s
    lastMessage = None
    while True:
        continueReception = True
        message = ""
        while continueReception:
            data = s.recv(1024)
            message += data.decode('utf-8')
            if len(data) < 1024:
                continueReception = False
        if len(message) > 20:
            messageJson = json.loads(message)
            if lastMessage != messageJson:
                print(messageJson)
                lastMessage = messageJson
            if messageJson['Command'] == "ServerInfo":
                if ((messageJson['ServerInfo']['MapLabel'] == 'datacenter') or (messageJson['ServerInfo']['MapLabel'] == 'sand')) and messageJson['ServerInfo']['GameMode'] == 'DM':
                    switchMap()

def checkMapInfo():
    global s
    global mapSwitched
    while True:
        if mapSwitched:
            mapSwitched = False
            time.sleep(180)
        s.sendall("ServerInfo".encode('utf-8'))
        time.sleep(1)

t1 = threading.Thread(target=socketReception, args=())
t1.start()
t2 = threading.Thread(target=checkMapInfo, args=())
t2.start()

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0}'.format(client.user.name))

@client.event
async def on_message(message):
    global curMapList
    args = message.content.split(" ")
    if len(message.content) == 0:
        return
    if args[0] == "/addmap":
        await requestMap(message)
        pass
    if args[0] == "/addcollection":
        await requestCollection(message)
        pass
    if args[0] == "/shufflemaps":
        curMapList.randomiseOrder()
        pass
    return

@client.event
async def on_reaction_add(reaction, user):
    global curMapList
    global userRequests
    
    for i in range(len(userRequests)):
        if userRequests[i].messageId == reaction.message.id:
            if userRequests[i].author == user.id:
                if userRequests[i].requestType:
                    await mapReacted(reaction, i)
                    return
                await collectionReacted(reaction, i)
            return
    return

client.run(token)