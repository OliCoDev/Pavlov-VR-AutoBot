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

    async def requestReacted(self, reaction):
        if self.requestType == RequestTypes.MAP:
            await self.mapReacted(reaction)
            return True
        return await self.collectionReacted(reaction)

    async def mapReacted(self, reaction):
        tag = self.requestInfo.tags[Converter.reactToInt(reaction.emoji)]
        self.requestInfo.selectGameMode(tag)
        self.requestInfo.addMap()
        await reaction.message.delete()
        await MessageManager.sendMapConfirmation(self.requestInfo, self.author, reaction.message)
        pass

    async def collectionReacted(self, reaction):
        mapInfo = self.requestInfo.getMapInfo()
        tag = mapInfo.tags[Converter.reactToInt(reaction.emoji)]
        self.requestInfo.setMapGameMode(tag)
        mapInfo = self.requestInfo.getMapInfo()
        await reaction.message.delete()
        if mapInfo == None:
            await MessageManager.sendCollectionConfirmation(self.requestInfo, self.author, reaction.message)
            return True
        self.setMessage(await MessageManager.sendMapRequest(mapInfo, self.author, reaction.message))
        return False
        pass
