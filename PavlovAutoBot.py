import discord
import Commands
import RequestList

client = discord.Client()


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
        pass
    if args[0] == "/addcollection":
        await Commands.addCollection(message)
        pass
    return


@client.event
async def on_reaction_add(reaction, user):
    await RequestList.reacted(reaction, user)
    return

client.run(token)