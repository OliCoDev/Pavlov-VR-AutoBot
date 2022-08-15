import Converter
from Map import Map
from discord import File
from Collection import Collection
from pavlovEnums import RequestTypes
import ImageManager
import RequestList
import MessageManager
import MapsList
import RconManagement
from Request import Request
from MapsQueue import  MapsQueue


def getUrlId(url):
    splitUrl = url.split("?")
    if len(splitUrl) <= 1:
        return None
    parameters = splitUrl[1]
    splitParameters = parameters.split("&")
    for i in splitParameters:
        splitData = i.split("=")
        if (len(splitData) > 1) and (splitData[0] == "id"):
            return int(splitData[1])
    return None


async def shuffleMaps(message):
    await message.delete()
    MapsList.shuffle()
    await MessageManager.sendTempMessage(message, "The maps have been shuffled")


async def addMap(message):
    args = message.content.split(" ")
    await message.delete()
    if len(args) <= 1:
        await MessageManager.sendTempMessage(message, message.author.mention +
                                             "\nPlease make a request with a steam workshop url")
        return
    mapId = getUrlId(args[1])
    if mapId == None:
        await MessageManager.sendTempMessage(message, message.author.mention +
                                             "\nPlease request a valid steam workshop url")
        return
    try:
        newMap = Map(mapId)
        if len(newMap.tags) == 1:
            newMap.selectGameMode(newMap.tags[0])
            newMap.addMap()
            await MessageManager.sendMapSingleTagConfirmation(newMap, message.author.id, message)
            return
        newRequest = Request(message.author.id, RequestTypes.MAP, newMap)
        newRequest.setMessage(await MessageManager.sendMapRequest(newMap, message.author.id, message))
        RequestList.addRequest(newRequest)

    except ValueError as e:
        await message.channel.send(e)


async def addCollection(message):
    args = message.content.split(" ")
    await message.delete()
    if len(args) <= 1:
        await MessageManager.sendTempMessage(message, message.author.mention +
                                             "\nPlease make a request with a steam workshop url")
        return
    collectionId = getUrlId(args[1])
    if collectionId == None:
        await MessageManager.sendTempMessage(message, message.author.mention +
                                             "\nPlease request a valid steam workshop url")
        return
    try:
        newCollection = Collection(collectionId)
        if newCollection.getMapInfo() == None:
            newCollection.addList()
            await MessageManager.sendCollectionConfirmation(newCollection, message.author.id, message)
            return
        newRequest = Request(message.author.id, RequestTypes.COLLECTION, newCollection)
        newRequest.setMessage(await MessageManager.sendMapRequest(newCollection.getMapInfo(),
                                                                  message.author.id, message))
        RequestList.addRequest(newRequest)

    except ValueError as e:
        await message.channel.send(e)


async def nextMap(message):
    await message.delete()
    if len(MapsList.maps) == 0:
        await MessageManager.sendTempMessage(message, "There are no maps currently in the list")
        return
    RconManagement.nextMap = True
    curMap = MapsList.maps[0]
    messageContent = "Switching over to " + curMap.title + " with the GameMode set to" + Converter.gameModeTotag(curMap.gamemode)
    await MessageManager.sendTempMapMessage(message, messageContent, curMap)


async def pauseMap(message):
    await message.delete()
    if not RconManagement.canContinue:
        await MessageManager.sendTempMessage(message, "The bot is already paused")
        return
    RconManagement.canContinue = False
    await MessageManager.sendTempMessage(message, "The bot has been paused")


async def playMap(message):
    await message.delete()
    if RconManagement.canContinue:
        await MessageManager.sendTempMessage(message, "The bot is already active")
        return
    RconManagement.canContinue = False
    await MessageManager.sendTempMessage(message, "The bot has been resumed")


async def mapsList(message):
    await message.delete()
    newMessage = await MessageManager.sendListMessage(message)
    newMapsList = MapsQueue(newMessage, message.author.id)
    await newMapsList.updateMessage()
    newRequest = Request(message.author.id, RequestTypes.MAPSLIST, newMapsList)
    for i in range(0, len(RequestList.requests)):
        requestInfo = RequestList.requests[i]
        if (requestInfo.author == message.author.id) and (requestInfo.requestType == RequestTypes.MAPSLIST):
            await requestInfo.requestInfo.message.delete()
            RequestList.requests.pop(i)
    RequestList.addRequest(newRequest)


async def deleteMap(message):
    args = message.content.split(" ")
    await message.delete()
    if len(args) <= 1:
        await MessageManager.sendTempMessage(message, message.author.mention +
                                             "\nPlease make a request with the number of the map you want to delete")
        return
    if not args[1].isnumeric():
        await MessageManager.sendTempMessage(message, message.author.mention +
                                             "\nPlease make a request with the number of the map you want to delete")
        return
    mapInt = int(args[1]) - 1
    if mapInt >= len(MapsList.maps):
        await MessageManager.sendTempMessage(message, message.author.mention +
                                             "\nThe inputed number was greater than the length of the current map list")
        return
    mapInfo = MapsList.pop(mapInt)

