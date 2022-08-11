requests = []


def isInEmojiList(emoji):
    emojiList = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    for i in emojiList:
        if i == emoji:
            return True
    return False


async def reacted(reaction, author):
    global requests
    if reaction.custom_emoji:
        return
    if not isInEmojiList(reaction.emoji):
        return

    for i in range(0, len(requests)):
        if (requests[i].author == author.id) and (requests[i].messageId == reaction.message.id):
            result = await requests[i].requestReacted(reaction)
            if result:
                requests.pop(i)
            return


def addRequest(newRequest):
    global requests
    requests.append(newRequest)
