import requests
import os

imageNumber = 0


def getImage(url):
    global imageNumber
    if url == "":
        return None
    imageName = "thumbnail" + str(imageNumber) + ".png"
    r = requests.get(url)
    f = open(imageName, "wb")
    f.write(r.content)
    f.close()
    return imageName


def deleteImage(imageName):
    if imageName == None:
        return
    os.remove(r".\\" + imageName)
