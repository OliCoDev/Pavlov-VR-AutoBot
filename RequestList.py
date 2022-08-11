requests = []


async def reacted(gameModeTag, message, author):
    global requests

    for i in range(0, len(requests)):
        if (requests[i].author == author.id) and (requests[i].messageId == message.id):
            result = await requests[i].requestReacted(gameModeTag, message)
            if result:
                requests.pop(i)
            return


def addRequest(newRequest):
    global requests
    requests.append(newRequest)
