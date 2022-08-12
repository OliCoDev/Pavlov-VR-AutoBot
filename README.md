# Pavlov VR AutoBot

The Pavlov VR AutoBot is an easy way for you and your friends to create sessions where you play together on a Dedicated server whilst not needing to contact the owner of the server to change the map and gamemode constantly

## Key Features

-Add maps and select which gamemode you would like to play on it
-Add a steam collection and select the gamemodes you would like to play on each individual map of the collection
-Randomise the order of already selected maps

## Setup

**Python 3.8 or higher is required**

To setup the Bot, you'll first need to install [Pycord](https://docs.pycord.dev/en/master/index.html)
To install it, you can run the following commands:
```
# Linux/macOS
python3 -m pip install -U py-cord

# Windows
py -3 -m pip install -U py-cord
```

Once [Pycord](https://docs.pycord.dev/en/master/index.html) has been installed, you can now create your Discord bot at the [Discord Developer Portal](https://discord.com/developers/applications) and get it's token(Don't forget to turn on MESSAGE CONTENT INTENT under the Bot category). Using that token, you'll need to replace the ```[Token Here]``` that's inside of [data.json](data.json) with the token you have recieved from the [Discord Developer Portal](https://discord.com/developers/applications)

Finally, in [data.json](data.json) you will need to replace the ```[Pavlov VR Server IP Here]``` with the IP of the Pavlov Dedicated Server you would like the bot to be connected to, replace the ```[Rcon Port Here]``` with the port of the Rcon port you have selected and replace the ```[Rcon Password Here]``` with the Rcon password that you have set for the server

Once all of that is done, you can simply launch it using the following command:
```
# Linux/macOS
python3 PavlovAutoBot.py

# Windows
py -3 PavlovAutoBot.py
```

## Usage

Currently you can use the bot using the following commands:

-```/addmap [Map Url Here]```
You can request a map using the aforementioned command and replacing the ```[Map Url Here]``` with the URL of a Pavlov VR Map that you can find on it's [Steam Workshop](https://steamcommunity.com/app/555160/workshop/) page. After that, you may follow the instruction that the bot gives you

-```/addcollection [Collection Url Here]```
You can request a collection of maps using the aforementioned command and replacing the ```[Collection Url Here]``` with the URL of a Pavlov VR Collection that you can find on it's [Steam Workshop Collections](https://steamcommunity.com/workshop/browse/?appid=555160&browsesort=trend&section=collections) page. After that, you may follow the instruction that the bot gives you

-```/shufflemaps```
This command will shuffle the order of the maps that are present inside the waiting list

-```/pausemap```
This command will pause the bot's ability to switch maps, so you may add maps and shuffle them without the bot switching maps on the Pavlov VR Server

-```/playmap```
This command will resume the bot's ability to switch maps

-```/nextmap```
This command will make the bot skip the current active map to the next map in the list. If there's no other map in the list

### License

MIT
