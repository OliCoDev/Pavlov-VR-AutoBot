from pavlovEnums import RequestTypes
import MessageManager
import Converter


class Request:
    def __init__(self, authorId, reqType, info):
        self.author = authorId
        self.requestType = reqType
        self.requestInfo = info
        self.messageId = None
        pass

    def setMessage(self, message):
        self.messageId = message.id

    async def requestReacted(self, gameModeTag, interaction):
        if self.requestType == RequestTypes.MAP:
            await self.mapReacted(gameModeTag, interaction)
            return True
        return await self.collectionReacted(gameModeTag, interaction)

    async def mapReacted(self, gameModeTag, interaction):
        self.requestInfo.selectGameMode(gameModeTag)
        self.requestInfo.addMap()
        await MessageManager.sendMapConfirmation(self.requestInfo, self.author, interaction)
        pass

    async def collectionReacted(self, gameModeTag, interaction):
        self.requestInfo.setMapGameMode(gameModeTag)
        mapInfo = self.requestInfo.getMapInfo()
        if mapInfo == None:
            self.requestInfo.addList()
            await MessageManager.sendCollectionConfirmation(self.requestInfo, self.author, interaction)
            return True
        await MessageManager.editMapRequest(mapInfo, self.author, interaction)
        return False
        pass
