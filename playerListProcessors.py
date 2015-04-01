import json

def players():
    SL = []
    AnzSp=int(input("Wie viele Spieler spielen mit?""\t"))
    for i in range(1,AnzSp+1):
        spieler = "Name von Spieler "+ str(i)+":"
        SpName=input(spieler)
        SL.append([SpName,0])
        savePlayerList(SL)
    return AnzSp

def give_player_key():
    SL = []
    AnzSp=int(input("Wie viele Spieler spielen mit?""\t"))
    for i in range(1,AnzSp+1):
        spieler = "Name von Spieler "+ str(i)+":"
        SpName=input(spieler)
        key = "Taste von Spieler "+ str(i)+":"
        SpKey = input(key)
        SL.append([SpName,0,SpKey])
        savePlayerList(SL)

def savePlayerList(liste):
    out_file = open('playerList.txt', 'wt')
    out_file.write(json.dumps(liste))
    out_file.close()

# emptyPlayerList wird im Programm nicht genutzt
def emptyPlayerList():
    empty = "Hier gibt es derzeit nichts. Starte den Quiz, dann schon!"
    out_file = open('playerList.txt', 'wt')
    out_file.write(json.dumps(empty))
    out_file.close()
