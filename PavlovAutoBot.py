import discord
import Commands
import RequestList

token = "OTM1ODkyMDQyMDM3NDY1MTk4.Gj-avo.UvW0JG062cDOh0PsRs7Usum-Wjs-Z3ZyRBorlo"
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