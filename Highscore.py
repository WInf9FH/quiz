import json

def saveHighscoreList(liste):
    out_file = open('Highscores.txt', 'wt')
    out_file.write(json.dumps(liste))
    out_file.close()

def compareScore(player, score, variante):
    # Highscore importieren
    Highscore = []
    in_file = open("Highscores.txt","rt")
    Highscore = json.loads(in_file.read())
    in_file.close()

    # Highscore vergleichen
    if Highscore[variante][1] < score:
        Highscore[variante][0] = player
        Highscore[variante][1] = score
        saveHighscoreList(Highscore)
        variante = variante+1
        print("Und hat damit einen neuen Highscore fuer den Spielmodus",variante,"erzielt!")
