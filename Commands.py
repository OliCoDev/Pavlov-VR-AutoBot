import Converter
import SessionInfo
from Map import Map
from Collection import Collection
from pavlovEnums import RequestTypes
import RequestList
import MessageManager
import MapsList
import RconManagement
from Request import Request
from MapsQueue import  MapsQueue

def isInChannel(message):
    if SessionInfo.discordInfo["channelId"] == "None" or SessionInfo.discordInfo["channelId"] == message.channel.id:
        return True
    return False

def isAdmin(message):
    if message.author.id == message.guild.owner_id:
        return True
    roles = message.author.roles
    for role in roles:
        if role.permissions.administrator:
            return True
    return False


async def commandSwitcher(message):
    args = message.content.split(" ")
    switcher = {
        "/addmap": addMap,
        "/addcollection": addCollection,
        "/shufflemaps": shuffleMaps,
        "/nextmap": nextMap,
        "/pausemap": pauseMap,
        "/playmap": playMap,
        "/maplist": mapsList,
        "/deletemap": deleteMap,
        "/setpavlovchannel": setPavlovChannel
    }
    func = switcher.get(args[0], None)
    if func:
        await func(message)
        return


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
    if not isInChannel(message):
        return
    await message.delete()
    MapsList.shuffle()
    await MessageManager.sendTempMessage(message, "The maps have been shuffled")
    await updateMapLists()


async def addMap(message):
    if not isInChannel(message):
        return
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
            await MessageManager.sendMapSingleTagConfirmation(newMap, message)
            await updateMapLists()
            return
        newRequest = Request(message.author.id, RequestTypes.MAP, newMap)
        newRequest.setMessage(await MessageManager.sendMapRequest(newMap, message.author.id, message))
        RequestList.addRequest(newRequest)

    except ValueError as e:
        await message.channel.send(e)


async def addCollection(message):
    if not isInChannel(message):
        return
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
    if not isInChannel(message):
        return
    await message.delete()
    if len(MapsList.maps) == 0:
        await MessageManager.sendTempMessage(message, "There are no maps currently in the list")
        return
    RconManagement.nextMap = True
    curMap = MapsList.maps[0]
    messageContent = "Switching over to " + curMap.title + " with the GameMode set to" + Converter.gameModeTotag(curMap.gamemode)
    await MessageManager.sendTempMapMessage(message, messageContent, curMap)
    await updateMapLists()


async def pauseMap(message):
    if not isInChannel(message):
        return
    await message.delete()
    if not RconManagement.canContinue:
        await MessageManager.sendTempMessage(message, "The bot is already paused")
        return
    RconManagement.canContinue = False
    await MessageManager.sendTempMessage(message, "The bot has been paused")


async def playMap(message):
    if not isInChannel(message):
        return
    await message.delete()
    if RconManagement.canContinue:
        await MessageManager.sendTempMessage(message, "The bot is already active")
        return
    RconManagement.canContinue = True
    await MessageManager.sendTempMessage(message, "The bot has been resumed")


async def mapsList(message):
    if not isInChannel(message):
        return
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
    if not isInChannel(message):
        return
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
    mapInfo = MapsList.maps.pop(mapInt)
    messageContent = str(message.author.mention) + "\n" + mapInfo.title + \
                     " with the GameMode set as " + Converter.gameModeTotag(mapInfo.gamemode) + \
                     " has been deleted from the list"
    await MessageManager.sendTempMapMessage(message, messageContent, mapInfo)
    await updateMapLists()


async def updateMapLists():
    for i in RequestList.requests:
        if i.requestType == RequestTypes.MAPSLIST:
            await i.requestInfo.updateMessage()


async def setPavlovChannel(message):
    await message.delete()
    if not isAdmin(message):
        await MessageManager.sendTempMessage(message, message.author.mention +
                                             "\nYou do not have permission to use this command")
    await MessageManager.sendChannelRequest(message)

