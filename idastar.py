import random, time, sys
from heuristic import manhattan

allmoves = 0
i = 0
allmovesstring = []
lastmoves = []

def getNextStates (width, current):
    nextStates = []
    empty = None
    for i in range(width):
        try:
            empty = current[i].index(0)
        except Exception as e:
            continue
        empty = (i, empty)
        break

    if (empty[1] < (width - 1)):
        a = [i[:] for i in current]
        a[empty[0]][empty[1]], a[empty[0]][empty[1] + 1] = a[empty[0]][empty[1] + 1], a[empty[0]][empty[1]]
        nextStates.append((a, 'RIGHT'))

    if (empty[1] > 0):
        b = [i[:] for i in current]
        b[empty[0]][empty[1]], b[empty[0]][empty[1] - 1] = b[empty[0]][empty[1] - 1], b[empty[0]][empty[1]]
        nextStates.append((b, 'LEFT'))

    if (empty[0] > 0):
        c = [i[:] for i in current]
        c[empty[0]][empty[1]], c[empty[0] - 1][empty[1]] = c[empty[0] - 1][empty[1]], c[empty[0]][empty [1]]
        nextStates.append((c, 'UP'))

    if (empty[0] < (width - 1)):
        d = [i[:] for i in current]
        d[empty[0]][empty[1]], d[empty[0] + 1][empty [1]] = d[empty[0] + 1][empty[1]], d[empty[0]][empty [1]]
        nextStates.append((d, 'DOWN'))

    return (nextStates)

def IDA_star(width, gameboard, finalboard):
    # demi_fboard = finalboard
    
    # for raw in len(finalboard)

    print "gameboard"
    print gameboard
    print "finalboard"
    print finalboard

    demi_fboard1 = []
    demi_fboard2 = []
    i = 0
    for raw in finalboard:
        if (i < 2):
            demi_fboard1.append(finalboard[i])
        else:
            demi_fboard2.append(finalboard[i])
        i += 1

    print "demi_fboard1"
    print demi_fboard1
    print "demi_fboard2"
    print demi_fboard2


    sys.exit()
    

    current = manhattan(width, gameboard, finalboard)
    while(1):
        tmp = IDA(width, gameboard, finalboard, 0, current)
        if tmp == 1:
            return allmoves, allmovesstring[::-1]
        if tmp == float("inf"):
            return 'Fail', 'Fail'
        current = tmp

j = 0
def IDA(width, gameboard, finalboard, g, current):
    global allmoves
    global allmovesstring
    global i
    global j
    
    syms = ['\\', '|', '/', '-']
    if i == 4:
        i = 0
    sys.stdout.write("\033[93m\b%s\033[0m"%syms[i])
    sys.stdout.flush()
    i += 1

    heuri = manhattan(width, gameboard, finalboard)
    f = g + heuri

    if f > current:
        return f

    if gameboard == finalboard:
        return 1

    minval = float('inf')

    for sibling in getNextStates(width, gameboard):
        tmp = IDA(width, sibling[0], finalboard, g + 1, current)
        if j == 0:
            print(sibling[1])
            print(sibling[0])
        if tmp == 1:
            allmoves += 1
            allmovesstring.append(sibling[1])
            return 1
        if tmp < minval:
            minval = tmp
    j += 1
    return minval