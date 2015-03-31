import json

SL=[]

def players():
    AnzSp=int(input("Wie viele Spieler spielen mit?""\t"))
    for i in range(1,AnzSp+1):
        spieler = "Name von Spieler "+ str(i)+":"
        SpName=input(spieler)
        SL.append([SpName,0])
        savePlayerList()
    return AnzSp

def give_player_key():
    AnzSp=int(input("Wie viele Spieler spielen mit?""\t"))
    for i in range(1,AnzSp+1):
        spieler = "Name von Spieler "+ str(i)+":"
        SpName=input(spieler)
        key = "Taste von Spieler "+ str(i)+":"
        SpKey = input(key)
        SL.append([SpName,0,SpKey])
        savePlayerList()

def savePlayerList():
    out_file = open('playerList.txt', 'wt')
    out_file.write(json.dumps(SL))
    out_file.close()

def emptyPlayerList():
    empty = "Hier gibt es derzeit nichts. Starte den Quiz, dann schon!"
    out_file = open('playerList.txt', 'wt')
    out_file.write(json.dumps(empty))
    out_file.close()
