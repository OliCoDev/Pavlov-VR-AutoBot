import ImageManager
import Converter
from Map import Map
from Collection import Collection
from discord import File


async def sendMapConfirmation(mapInfo: Map, author, message):
    messageContent = "<@" + str(author) + ">\n" + mapInfo.title + \
                     " has been added with the GameMode set as " + Converter.gameModeTotag(mapInfo.gamemode)
    img = ImageManager.getImage(mapInfo.image)
    if img:
        await message.channel.send(messageContent, file=File(r".\\" + img))
        ImageManager.deleteImage(img)
    else:
        await message.channel.send(messageContent)


async def sendCollectionConfirmation(collectionInfo: Collection, author, message):
    messageContent = "<@" + str(author) + ">\nSuccessfully added:"
    for i in collectionInfo.selectedMaps:
        messageContent += "\n" + i.title + " with the GameMode set to " + Converter.gameModeTotag(i.gamemode)
    await message.channel.send(messageContent)


async def sendMapRequest(mapInfo: Map, author, message):
    messageContent = "<@" + str(author) + ">\nPlease select what gamemode you would like to play on " + mapInfo.title
    for i in range(len(mapInfo.tags)):
        messageContent += "\n" + Converter.intToReaction(i) + ": " + mapInfo.tags[i]
    newMessage = None
    img = ImageManager.getImage(mapInfo.image)
    if img:
        newMessage = await message.channel.send(messageContent, file=File(r".\\" + img))
        ImageManager.deleteImage(img)
    else:
        newMessage = await message.channel.send(messageContent)
    for i in range(len(mapInfo.tags)):
        await newMessage.add_reaction(Converter.intToReaction(i))
    return newMessage
