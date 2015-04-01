import json
import json
from playerListProcessors import *
from PrintTexts import *
from AnswerProcessors import *
from getPlayerByKey import *

# Fragen importieren
in_file= open ("Fragen.txt","rt")
Quiz = json.loads(in_file.read())
in_file.close()

# Spielerliste importieren
SL=[]
in_file = open ("playerList.txt","rt")
SL = json.loads(in_file.read())
in_file.close()

def refreshPlayerList():
    in_file = open ("playerList.txt","rt")
    SL = json.loads(in_file.read())
    in_file.close()

# Gewünschte Spielvariante abfragen
print("Verfügbare Spielvarianten:")
print("1 - Jeder Spieler gibt eine Antwort ab.")
print("2 - Jeder Spieler bekommt eine Taste zugewiesen, drückt er diese,\nist er der einzige der die Frage beantworten darf.")
Spielart = input("Welche möchtest du nutzen?")


# Spielvariante 1
if int(Spielart) == 1:
      y=players()        
      f=len(Quiz)
      for o in range (0,f):
          print_question(Quiz,o)
          print_answers(Quiz, o)
          richtig = True
          for u in range(0,y):
              print(SL[u][0],"ist an der Reihe") 
              x=input("Antwort:")
              if correct_answer(Quiz,o,x):
                  SL[u][1]=SL[u][1]+1
                  richtig = True
          if richtig == True:
              result_answers(o,Quiz,SL)
      refreshPlayerList()
      for i in range(0,y):
          print(SL[i][0],"hat",SL[i][1],"Punkt(e) von",f,"möglichen Punkten erreicht")
      emptyPlayerList()
else:        
    # Spielvariante 2
    give_player_key()
    f=len(Quiz)
    for o in range (0,f):
        print_question(Quiz,o)
        print_answers(Quiz, o)
        PressedKey = input("Wenn du die Antwort weißt, drücke deine Taste!")
        getPlayer = getPlayerByKey(PressedKey)
        print(SL[getPlayer][0],"ist an der Reihe.")
        x = input("Welche Antwort ist richtig?")
        punkte_rechnen(Quiz,o,x, PressedKey)
        result_answers(o,Quiz,SL)
    refreshPlayerList()
    for i in range(0,len(SL)):
        print(SL[i][0],"hat",SL[i][1],"Punkt(e) von",f," möglichen Punkten erreicht.")
    emptyPlayerList()
