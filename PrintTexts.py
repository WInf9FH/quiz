def print_question(L,r):
    print(L[r][0])

def print_answers(L,r):
    laenge = len(L[r][1])
    for i in range(0,laenge):
        print(L[r][1][i])
