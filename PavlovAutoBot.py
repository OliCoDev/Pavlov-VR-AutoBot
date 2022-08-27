import discord
from Commands import commandSwitcher
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
    if len(message.content) == 0:
        return
    await commandSwitcher(message)
    return

if __name__ == "__main__":
    SessionInfo.init()
    RconManagement.init()
    client.run(SessionInfo.token)
