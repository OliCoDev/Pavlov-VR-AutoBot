import ImageManager
import Converter
import RequestList
import SessionInfo
from Map import Map
from Collection import Collection
from discord import File, SelectOption, ChannelType
from discord.ui import Select, View


async def sendMapConfirmation(mapInfo: Map, author, interaction):
    messageContent = "<@" + str(author) + ">\n" + mapInfo.title + \
                     " has been added with the GameMode set as " + Converter.gameModeTotag(mapInfo.gamemode)
    img = ImageManager.getImage(mapInfo.image)
    if img:
        await interaction.response.edit_message(content=messageContent, files=[File(r".\\" + img)], attachments=[], view=None)
        ImageManager.deleteImage(img)
    else:
        await interaction.response.edit_message(content=messageContent, files=[], attachments=[], view=None)


async def sendMapSingleTagConfirmation(mapInfo: Map, author, message):
    messageContent = "<@" + str(author) + ">\n" + mapInfo.title + \
                     " has been added with the GameMode set as " + Converter.gameModeTotag(mapInfo.gamemode)
    img = ImageManager.getImage(mapInfo.image)
    if img:
        await message.channel.send(content=messageContent, file=File(r".\\" + img), view=None)
        ImageManager.deleteImage(img)
    else:
        await message.channel.send(content=messageContent, view=None)


async def sendCollectionConfirmation(collectionInfo: Collection, author, interaction):
    messageContent = "<@" + str(author) + ">\nSuccessfully added:"
    for i in collectionInfo.selectedMaps:
        messageContent += "\n" + i.title + " with the GameMode set to " + Converter.gameModeTotag(i.gamemode)
    await interaction.response.edit_message(content=messageContent, files=[], attachments=[], view=None)


async def editMapRequest(mapInfo: Map, author, interaction):
    messageContent = "<@" + str(author) + ">\nPlease select what gamemode you would like to play on " + mapInfo.title
    options = []
    for i in mapInfo.tags:
        options.append(SelectOption(label=i))
    newSelect = Select(placeholder="Select a GameMode", options=options)
    newView = View(newSelect)

    async def selectionMenuInteracted(newInteraction):
        await RequestList.reacted(newSelect.values[0], newInteraction)
        pass

    newSelect.callback = selectionMenuInteracted
    img = ImageManager.getImage(mapInfo.image)
    if img:
        await interaction.response.edit_message(content=messageContent, files=[File(r".\\" + img)], attachments=[], view=newView)
        ImageManager.deleteImage(img)
    else:
        await interaction.response.edit_message(content=messageContent, files=[], attachments=[], view=newView)


async def sendMapRequest(mapInfo: Map, author, message):
    messageContent = "<@" + str(author) + ">\nPlease select what gamemode you would like to play on " + mapInfo.title
    options = []
    for i in mapInfo.tags:
        options.append(SelectOption(label=i))
    newSelect = Select(placeholder="Select a GameMode", options=options)
    newView = View(newSelect)

    async def selectionMenuInteracted(interaction):
        # await interaction.response.defer()
        await RequestList.reacted(newSelect.values[0], interaction)
        pass

    newSelect.callback = selectionMenuInteracted
    newMessage = None
    img = ImageManager.getImage(mapInfo.image)
    if img:
        newMessage = await message.channel.send(messageContent, files=[File(r".\\" + img)], view=newView)
        ImageManager.deleteImage(img)
    else:
        newMessage = await message.channel.send(messageContent, view=newView)
    return newMessage


async def sendTempMessage(message, content):
    await message.channel.send(content=content,
                               delete_after=30)


async def sendTempMapMessage(message, content, mapInfo):
    img = ImageManager.getImage(mapInfo.image)
    if img:
        await message.channel.send(content=content,
                                   file=File(r".\\" + img),
                                   delete_after=30)
        ImageManager.deleteImage(img)
    else:
        await message.channel.send(content=content,
                                   delete_after=30)


async def sendListMessage(message):
    return await message.channel.send(content="Please Wait")


async def updateList(message, values):
    await message.edit(content=values[0], view=values[1])


async def sendChannelRequest(message):
    channels = [SelectOption(label="None")]
    for i in message.guild.channels:
        if i.type == ChannelType.text:
            channels.append(SelectOption(label=i.name))
    newSelect = Select(placeholder="Select a Text Channel", options=channels)

    async def channelSelected(interaction):
        if interaction.user.id != message.author.id:
            return
        selectedValue = newSelect.values[0]
        if selectedValue == "None":
            SessionInfo.setChannel("None")
            await interaction.response.edit_message(content="Commands can now be requested anywhere",
                                                    view=None)
        else:
            for i in message.guild.channels:
                if i.type == ChannelType.text:
                    if i.name == selectedValue:
                        SessionInfo.setChannel(i.id)
            await interaction.response.edit_message(content="The commands channel has been set to " + selectedValue,
                                                    view=None)
    newSelect.callback = channelSelected
    newView = View(newSelect)
    await message.channel.send(content="Please select which channel you want the commands to be in", view=newView)

