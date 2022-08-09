from Map import Map
from Collection import Collection
from pavlovEnums import RequestTypes
import MessageManager
import Converter


class Request:

    def __int__(self, authorId, reqType, info):
        self.author = authorId
        self.requestType = reqType
        self.requestInfo = info
        self.messageId = None
        pass

    def setMessage(self, message):
        self.messageId = message.id

    async def requestReacted(self, reaction, message):
        if self.requestType == RequestTypes.MAP:
            await self.mapReacted(reaction, message)
            return True
        return await self.collectionReacted(reaction, message)

    async def mapReacted(self, reaction, message):
        tag = self.requestInfo.tags[Converter.reactToInt(reaction.emoji)]
        self.requestInfo.selectGameMode(tag)
        self.requestInfo.addMap()
        MessageManager.sendMapConfirmation(self.requestInfo, self.author, message)
        pass

    async def collectionReacted(self, reaction, message):
        mapInfo = self.requestInfo.getMapInfo()
        tag = mapInfo.tags[Converter.reactToInt(reaction.emoji)]
        self.requestInfo.setMapGameMode(tag)
        mapInfo = self.requestInfo.getMapInfo()
        if mapInfo == None:
            await MessageManager.sendCollectionConfirmation(self.requestInfo, self.author, message)
            return True
        self.setMessage(await MessageManager.sendMapRequest(mapInfo, self.author, message))
        return False
        pass
