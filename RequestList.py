requests = []


async def reacted(gameModeTag, interaction):
    global requests

    for i in range(0, len(requests)):
        if (requests[i].author == interaction.user.id) and (requests[i].messageId == interaction.message.id):
            result = await requests[i].requestReacted(gameModeTag, interaction)
            if result:
                requests.pop(i)
            return


def addRequest(newRequest):
    global requests
    requests.append(newRequest)
