import json

in_file= open ("Fragen.txt","rt")
Quiz = json.loads(in_file.read())
in_file.close()

SL=[]
      
def players():
    AnzSp=int(input("Wie viele Spieler spielen mit?""\t"))
    for i in range(1,AnzSp+1):
        spieler = "Name von Spieler "+ str(i)+":"
        SpName=input(spieler)
        SL.append([SpName,0])
    return AnzSp

def print_question(L,r):
    print(L[r][0])

def print_answers(L,r):
    länge = len(L[r][1])
    for i in range(0,länge):
        print(L[r][1][i])

def correct_answer(L,r,RAntwort):
    Antworten=L[r][2]
    if RAntwort==L[r][2] :
        correct = True
    else:
        correct =False
    return correct

def result_answers(y,r,L,SL):
    print("Die richtige Antwort war ",L[r][2],"\n") 
    for i in range(0,y):
        print(SL[i][0], "hat momentan",SL[i][1],"Punkt(e).""\n")

y=players()        
f=len(Quiz)
for o in range (0,f):
    print_question(Quiz,o)
    print_answers(Quiz, o)
    for u in range(0,y):
        print(SL[u][0],"ist an der Reihe") 
        x=input("Antwort:")
    
        if correct_answer(Quiz,o,x):
            SL[u][1]=SL[u][1]+1
    if o != f-1:
        result_answers(y,o,Quiz,SL)
for i in range(0,y):
    print(SL[i][0],"hat",SL[i][1],"Punkt(e) von möglichen",f,"Punkten erreicht")
    
