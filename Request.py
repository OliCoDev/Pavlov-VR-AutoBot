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

    async def requestReacted(self, gameModeTag, message):
        if self.requestType == RequestTypes.MAP:
            await self.mapReacted(gameModeTag, message)
            return True
        return await self.collectionReacted(gameModeTag, message)

    async def mapReacted(self, gameModeTag, message):
        self.requestInfo.selectGameMode(gameModeTag)
        self.requestInfo.addMap()
        await message.delete()
        await MessageManager.sendMapConfirmation(self.requestInfo, self.author, message)
        pass

    async def collectionReacted(self, gameModeTag, message):
        self.requestInfo.setMapGameMode(gameModeTag)
        mapInfo = self.requestInfo.getMapInfo()
        await message.delete()
        if mapInfo == None:
            await MessageManager.sendCollectionConfirmation(self.requestInfo, self.author, message)
            return True
        self.setMessage(await MessageManager.sendMapRequest(mapInfo, self.author, message))
        return False
        pass
