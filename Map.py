import requests
import json

import converter
import MapsList

class Map:
    def __init__(self, id) -> None:
        r = requests.post("https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/", data = {"itemcount": 1, "publishedfileids[0]": id})
        requestData = json.loads(r.content)['response']['publishedfiledetails'][0]
        if requestData["result"] != 1:
            raise ValueError('The url you have inputed did not correlate to a steam item')
        if requestData["creator_app_id"] != 555160:
            raise ValueError('The request you have made was not a Pavlov VR Map')
        tags = []
        for i in requestData["tags"]:
            tags.append(i["tag"])
        if len(tags) == 0: 
            tags = ["Deathmatch", "Team Deathmatch", "Search and Destroy", "Gun Game", "Capture the Flag", "TTT", "Zombie Coop", "Custom", "PUSH", "Hide", "Prop Hunt"]
        self.id = id
        self.title = requestData["title"]
        self.image = requestData["preview_url"]
        self.tags = tags
        self.gamemode = None
        pass

    def selectGameMode(self, inGameMode):
        if self.gameMode != None:
            return
        if (inGameMode in self.tags) or (len(self.tags) == 0):
            self.gameMode = converter.tagToGameMode(inGameMode)
            return
        return

    def addMap(self):
        MapsList.addMap(self)