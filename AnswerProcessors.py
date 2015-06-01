import json
from getPlayerByKey import *

def savePlayerList(liste):
    out_file = open('playerList.txt', 'wt')
    out_file.write(json.dumps(liste))
    out_file.close()

def importPlayerList():
    SL=[]
    in_file = open ("playerList.txt","rt")
    playerList = json.loads(in_file.read())
    in_file.close()
    return playerList

def correct_answer(L,r,RAntwort):
    Antworten=L[r][2]
    if RAntwort==L[r][2] :
        correct = True
    else:
        correct =False
    return correct

def result_answers(r,L,SL):
    SL = importPlayerList()
    print("Die richtige Antwort war "+L[r][2]+"\n") 
    for i in range(0,len(SL)):
        print(SL[i][0]+ " hat momentan "+SL[i][1]+" Punkt(e).""\n")

def punkte_rechnen(Quiz,o,x, pressedKey):
    SL = importPlayerList()
    if correct_answer(Quiz,o,x):
                getPlayer = getPlayerByKey(pressedKey)
                SL[getPlayer][1]=SL[getPlayer][1]+1
                savePlayerList(SL)
