import random, time, sys
from heuristic import manhattan

allmoves = 0
i = 0
allmovesstring = []

def getNextStates (width, current, laststate):
    nextStates = []
    empty = None
    for i in range(width):
        try:
            empty = current[i].index(0)
        except Exception as e:
            continue
        empty = (i, empty)
        break

    if (empty[1] < (width - 1) and laststate != 'LEFT'):
        a = [i[:] for i in current]
        a[empty[0]][empty[1]], a[empty[0]][empty[1] + 1] = a[empty[0]][empty[1] + 1], a[empty[0]][empty[1]]
        nextStates.append((a, 'RIGHT'))

    if (empty[1] > 0 and laststate != 'RIGHT'):
        b = [i[:] for i in current]
        b[empty[0]][empty[1]], b[empty[0]][empty[1] - 1] = b[empty[0]][empty[1] - 1], b[empty[0]][empty[1]]
        nextStates.append((b, 'LEFT'))

    if (empty[0] > 0 and laststate != 'DOWN'):
        c = [i[:] for i in current]
        c[empty[0]][empty[1]], c[empty[0] - 1][empty[1]] = c[empty[0] - 1][empty[1]], c[empty[0]][empty [1]]
        nextStates.append((c, 'UP'))

    if (empty[0] < (width - 1) and laststate != 'UP'):
        d = [i[:] for i in current]
        d[empty[0]][empty[1]], d[empty[0] + 1][empty [1]] = d[empty[0] + 1][empty[1]], d[empty[0]][empty [1]]
        nextStates.append((d, 'DOWN'))

    return (nextStates)

def IDA_star(width, gameboard, finalboard):
    current = manhattan(width, gameboard, finalboard)
    print (current)
    while(1):
        tmp = IDA(width, gameboard, finalboard, 0, current)
        if tmp == 1:
            return allmoves, allmovesstring[::-1]
        if tmp == float("inf"):
            return 'Fail', 'Fail'
        current = tmp
    return result

def IDA(width, gameboard, finalboard, g, current):
    global allmoves
    global allmovesstring
    global i
    
    syms = ['\\', '|', '/', '-']
    if i == 4:
        i = 0
    sys.stdout.write("\033[93m\b%s\033[0m"%syms[i])
    sys.stdout.flush()
    i += 1

    state = None
    heuri = manhattan(width, gameboard, finalboard)
    print ("HEURI" + str(heuri))
    f = g + heuri

    if f > current:
        return f

    if gameboard == finalboard:
        return 1

    minval = float('inf')

    for elem in allmovesstring:
        state = elem

    for sibling in getNextStates(width, gameboard, state):
        tmp = IDA(width, sibling[0], finalboard, g + 1, current)
        if tmp == 1:
            allmoves += 1
            allmovesstring.append(sibling[1])
            return 1
        if tmp < minval:
            minval = tmp
    return minval