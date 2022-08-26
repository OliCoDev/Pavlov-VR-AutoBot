def tagToGameMode(tag):
    switcher = {
        "Deathmatch": "DM",
        "Team Deathmatch": "TDM",
        "Search and Destroy": "SND",
        "Gun Game": "GUN",
        "Capture the Flag": "CTF",
        "TTT": "TTT",
        "Zombie Coop": "ZWV",
        "Custom": "CUSTOM",
        "Push": "PUSH",
        "Hide": "HIDE",
        "Prop Hunt": "PH"
    }
    return switcher.get(tag)


def gameModeTotag(gameMode):
    switcher = {
        "DM": "Deathmatch",
        "TDM": "Team Deathmatch",
        "SND": "Search and Destroy",
        "GUN": "Gun Game",
        "CTF": "Capture the Flag",
        "TTT": "TTT",
        "ZWV": "Zombie Coop",
        "CUSTOM": "Custom",
        "PUSH": "Push",
        "HIDE": "Hide",
        "PH": "Prop Hunt"
    }
    return switcher.get(gameMode)


def intToReaction(inInt):
    switcher = {
        0: "0️⃣",
        1: "1️⃣",
        2: "2️⃣",
        3: "3️⃣",
        4: "4️⃣",
        5: "5️⃣",
        6: "6️⃣",
        7: "7️⃣",
        8: "8️⃣",
        9: "9️⃣",
        10: "🔟"
    }
    return switcher.get(inInt)


def reactToInt(inEmote):
    switcher = {
        "0️⃣": 0,
        "1️⃣": 1,
        "2️⃣": 2,
        "3️⃣": 3,
        "4️⃣": 4,
        "5️⃣": 5,
        "6️⃣": 6,
        "7️⃣": 7,
        "8️⃣": 8,
        "9️⃣": 9,
        "🔟": 10
    }
    return switcher.get(inEmote)
