import MapsList
from discord import ButtonStyle
from discord.ui import Button, View
import Converter
import MessageManager

maxMapView = 5

class MapsQueue:
    def __init__(self, message, authorId):
        self.mapPos = 0
        self.message = message
        self.author = authorId
        pass

    def createList(self):
        global maxMapView
        while len(MapsList.maps) < self.mapPos:
            self.mapPos -= maxMapView
        newContent = "<@" + str(self.author) + ">\nMaps List:"
        lastMapPos = self.mapPos + maxMapView
        if len(MapsList.maps) < lastMapPos:
            lastMapPos = len(MapsList.maps)
        for i in range(self.mapPos, lastMapPos):
            mapInfo = MapsList.maps[i]
            newContent += "\n" + str(i + 1) + ": " + mapInfo.title + " with the gamemode set as " + \
                          Converter.gameModeTotag(mapInfo.gamemode)
        newView = self.getView()
        return [newContent, newView]

    def getView(self):
        global maxMapView
        newView = View()
        if maxMapView <= self.mapPos:
            previousButton = Button(emoji="◀", style=ButtonStyle.primary)

            async def previousInteraction(interaction):
                await interaction.response.defer()
                if interaction.user.id == self.author:
                    await self.previousPos()

            previousButton.callback = previousInteraction
            newView.add_item(previousButton)
        if len(MapsList.maps) >= self.mapPos + maxMapView:
            nextButton = Button(emoji="▶", style=ButtonStyle.primary)

            async def nextInteraction(interaction):
                await interaction.response.defer()
                if interaction.user.id == self.author:
                    await self.nextPos()

            nextButton.callback = nextInteraction
            newView.add_item(nextButton)
        return newView

    async def updateMessage(self):
        values = self.createList()
        await MessageManager.updateList(self.message, values)

    async def nextPos(self):
        global maxMapView
        if len(MapsList.maps) >= self.mapPos + maxMapView:
            self.mapPos += maxMapView
        await self.updateMessage()
        pass

    async def previousPos(self):
        global maxMapView
        if maxMapView <= self.mapPos:
            self.mapPos -= maxMapView
        await self.updateMessage()
        pass


