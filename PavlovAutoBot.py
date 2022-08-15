import discord
import Commands
import SessionInfo
import RconManagement

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('We have logged in as {0}'.format(client.user.name))


@client.event
async def on_message(message):
    args = message.content.split(" ")
    if len(message.content) == 0:
        return
    if args[0] == "/addmap":
        await Commands.addMap(message)
        return
    if args[0] == "/addcollection":
        await Commands.addCollection(message)
        return
    if args[0] == "/shufflemaps":
        await Commands.shuffleMaps(message)
        return
    if args[0] == "/nextmap":
        await Commands.nextMap(message)
        return
    if args[0] == "/pausemap":
        await Commands.pauseMap(message)
        return
    if args[0] == "/playmap":
        await Commands.playMap(message)
        return
    if args[0] == "/maplist":
        await Commands.mapsList(message)
        return
    return

if __name__ == "__main__":
    SessionInfo.init()
    RconManagement.init()
    client.run(SessionInfo.token)
