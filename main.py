import random, time, sys
from heapq import heapify, heappush, heappop

def checkIfSolvable(gameboard):
	gameboardsimplearray = []
	for elem in gameboard:
		for value in elem:
			gameboardsimplearray.append(value)
	
	size = len(gameboardsimplearray)
	i = 0
	inversion = 0
	while(i < size):
		j = i + 1
		while(j < size):
			if(gameboardsimplearray[j] != 0 and gameboardsimplearray[i] != 0):
				if(gameboardsimplearray[j] > gameboardsimplearray[i]):
					inversion += 1
			j += 1
		i += 1

	print("\nTotal inversion : " + str(inversion))
	if(inversion % 2 == 1):
		return False
	else:
		return True

def manhattan(width, gameboard, finalboard):
	result = 0
	for i in range(width):
		for j in range(width):
			if (finalboard[i][j] == 0):
				continue
			for l in range(width):
				for m in range(width):
					if (finalboard[i][j] == gameboard[l][m]):
						result += (abs (m - j) + abs (l - i))
						break
	return (result)

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
		a = [i.copy () for i in current]
		a [empty[0]] [empty[1]], a[empty[0]][empty[1] + 1] = a[empty[0]][empty[1] + 1], a[empty[0]][empty[1]]
		nextStates.append(('RIGHT', a, (empty[0], empty[1] + 1)))

	if (empty[1] > 0):
		b = [i.copy () for i in current]
		b [empty[0]][empty[1]], b[empty[0]][empty[1] - 1] = b[empty[0]][empty[1] - 1], b[empty[0]][empty[1]]
		nextStates.append(('LEFT', b, (empty[0], empty[1] - 1)))

	if (empty[0] > 0):
		c = [i.copy () for i in current]
		c [empty[0]][empty[1]], c[empty[0] - 1][empty[1]] = c[empty[0] - 1][empty[1]], c[empty[0]][empty [1]]
		nextStates.append(('UP', c, (empty[0] - 1, empty[1])))

	if (empty[0] < (width - 1)):
		d = [i.copy () for i in current]
		d [empty[0]][empty[1]], d[empty[0] + 1][empty [1]] = d[empty[0] + 1][empty[1]], d[empty[0]][empty [1]]
		nextStates.append(('DOWN', d, (empty[0] + 1, empty[1])))
	return (nextStates)

def getSequenceInfo (width, gameboard, finalboard):
	current = (manhattan(width, gameboard, finalboard), 0, [], gameboard)
	stateTree = [current]
	heapify(stateTree)
	i = 0
	while (not current[-1] == finalboard):
		syms = ['\\', '|', '/', '-']
		if i == 4:
			i = 0
		sys.stdout.write("\033[93m\b%s\033[0m"%syms[i])
		sys.stdout.flush()
		i += 1
		current = heappop(stateTree)
		for state in getNextStates(width, current[-1]):
			heappush(stateTree,  (manhattan(width, state[1], finalboard) + current[1] + 1, current[1] + 1, current[2] + [state[0]], state[1]))
	return (current[1], current[2])

def construct(width):
	if (width.isdigit() == False):
		return print('\033[91mThis is not integer !')
	elif (int(width) < 2):
		return print('\033[91mThis is not a good value !')
	width = int(width)
	allvalue = width * width
	#list trier pour le tableau de fin
	allcase_order = [x for x in range(0, allvalue)]
	#list random pour le tableau de jeu
	allcase = random.sample(range(allvalue),allvalue)

	#Cree un tableau a 2 dimension pour le tableau a atteindre fin du jeu
	finalboard = []
	k = 0
	for i in range(width):
		new = []
		for j in range(width):
			new.append(allcase_order[k])
			k += 1
		finalboard.append(new)

	#Cree un tableau a 2 dimension pour le plateau de jeu
	gameboard = []
	k = 0
	for i in range(width):
		new = []
		for j in range(width):
			new.append(allcase[k])
			k += 1
		gameboard.append(new)

	#Board with random value
	print("\n\033[95mGAME BOARD\033[0m")
	posrow = 0
	for row in gameboard:
		print(str(row))

	#Goal board
	print("\n\033[95mFINAL BOARD\033[0m")
	for row in finalboard:
		print(str(row))

	#If total inversion % 2 == 1, puzzle is unsolvable
	checkifsolvable = checkIfSolvable(gameboard)
	if (checkifsolvable == False):
		return(print("\n\033[91mThis game board is unsolvable !\033[90m"))
	#Call A star, time instentiation 
	print("\n\033[95mprocessing : \033[0m")
	time1 = time.time()
	seqCount, sequence = getSequenceInfo (width, gameboard, finalboard)
	#Time finished A star
	time2 = time.time()

	#Print time, number of move and all move to accomplite board
	print("\n\033[91mTime : \033[0m" + str(round(time2 - time1, 3)) + "scd")
	print("\033[91mNumber of move : \033[0m" + str(seqCount))
	print('\033[91mAll move : \033[0m\033[92m')
	print('\n'.join (sequence))
	return

if __name__ == '__main__':
	width = input('\033[92mChoose size for Npuzzle: \n')
	construct(width)