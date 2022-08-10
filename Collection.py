from Map import Map
import MapsList
import requests
import json


class Collection:
    def __init__(self, id) -> None:
        r = requests.post("https://api.steampowered.com/ISteamRemoteStorage/GetCollectionDetails/v1/",
                          data={"collectioncount": 1, "publishedfileids[0]": id})
        requestData = json.loads(r.content)['response']['collectiondetails'][0]
        if requestData["result"] != 1:
            raise ValueError('The url you have inputed did not correlate to a steam collection')
        requestBody = {"itemcount": len(requestData["children"])}
        for i in range(0, len(requestData["children"])):
            requestBody["publishedfileids[" + str(i) + "]"] = requestData["children"][i]["publishedfileid"]
        r = requests.post("https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/",
                          data=requestBody)
        requestData = json.loads(r.content)['response']['publishedfiledetails']
        self.id = id
        self.selectedMaps = []
        self.requestedMaps = []
        for i in requestData:
            if i["result"] != 1:
                continue
            if i["creator_app_id"] != 555160:
                continue
            tags = []
            for j in i["tags"]:
                tags.append(j["tag"])
            newMap = Map(i["publishedfileid"], i["title"], i["preview_url"], tags)
            self.requestedMaps.append(newMap)
        self.checkSingleTag()
        pass

    def checkSingleTag(self):
        while len(self.requestedMaps) > 0:
            if len(self.requestedMaps[0].tags) > 1:
                break
            self.requestedMaps[0].selectGameMode(self.requestedMaps[0].tags[0])
            self.selectedMaps.append(self.requestedMaps.pop(0))
        pass

    def getMapInfo(self) -> Map:
        if len(self.requestedMaps) == 0:
            return None
        return self.requestedMaps[0]

    def setMapGameMode(self, inGameMode):
        self.requestedMaps[0].selectGameMode(inGameMode)
        self.selectedMaps.append(self.requestedMaps.pop(0))
        self.checkSingleTag()

    def addList(self):
        for i in self.selectedMaps:
            MapsList.addMap(i)
