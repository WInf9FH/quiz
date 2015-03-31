import json

def importPlayerList():
    in_file = open ("playerList.txt","rt")
    playerList = json.loads(in_file.read())
    in_file.close()
    return playerList

def getPlayerByKey(pressedKey):
    SL = []
    SL = importPlayerList()
    for i in range(0,len(SL)):
        if SL[i][2] == pressedKey:
            return i
