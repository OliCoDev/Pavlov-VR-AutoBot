from Map import Map
from Collection import Collection
from pavlovEnums import RequestTypes
import RequestList
import MessageManager
from Request import Request


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


async def addMap(message):
    args = message.content.split(" ")
    await message.delete()
    if len(args) <= 1:
        await message.channel.send(message.author.mention + "\nPlease make a request with a steam workshop url")
        return
    mapId = getUrlId(args[1])
    if mapId == None:
        await message.channel.send(message.author.mention + "\nPlease request a valid steam workshop url")
        return
    try:
        newMap = Map(mapId)
        if len(newMap.tags) == 1:
            newMap.selectGameMode(newMap.tags[0])
            newMap.addMap()
            await MessageManager.sendMapConfirmation(newMap, message.author.id, message)
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
        await message.channel.send(message.author.mention + "\nPlease make a request with a steam workshop url")
        return
    collectionId = getUrlId(args[1])
    if collectionId == None:
        await message.channel.send(message.author.mention + "\nPlease request a valid steam workshop url")
        return
    try:
        newCollection = Collection(collectionId)
        if newCollection.getMapInfo() == None:
            newCollection.addList()
            await MessageManager.sendCollectionConfirmation(newCollection, message.author.id, message)
            return
        newRequest = Request(message.author.id, RequestTypes.COLLECTION, newCollection)
        newRequest.setMessage(await MessageManager.sendMapRequest(newCollection.getMapInfo(), message.author.id, message))
        RequestList.addRequest(newRequest)

    except ValueError as e:
        await message.channel.send(e)
