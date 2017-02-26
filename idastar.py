import random, time, sys
from heuristic import manhattan

allmoves = 0
i = 0
allmovesstring = []
lastmoves = []

def getNextStates (width, current):
	nextStates = []
	case = None
	for i in range(width):
		try:
			case = current[i].index(0)
		except Exception as e:
			continue
		case = (i, case)
		break

	# print ("case")
	# print (case)
	# sys.exit()

	if (case[1] < (width - 1)):
		a = [i[:] for i in current]
		a[case[0]][case[1]], a[case[0]][case[1] + 1] = a[case[0]][case[1] + 1], a[case[0]][case[1]]
		nextStates.append((a, 'RIGHT'))

	if (case[1] > 0):
		b = [i[:] for i in current]
		b[case[0]][case[1]], b[case[0]][case[1] - 1] = b[case[0]][case[1] - 1], b[case[0]][case[1]]
		nextStates.append((b, 'LEFT'))

	if (case[0] > 0):
		c = [i[:] for i in current]
		c[case[0]][case[1]], c[case[0] - 1][case[1]] = c[case[0] - 1][case[1]], c[case[0]][case [1]]
		nextStates.append((c, 'UP'))

	if (case[0] < (width - 1)):
		d = [i[:] for i in current]
		d[case[0]][case[1]], d[case[0] + 1][case [1]] = d[case[0] + 1][case[1]], d[case[0]][case [1]]
		nextStates.append((d, 'DOWN'))

	return (nextStates)

def negative_board(width):
	test = 0
	col = 0
	cmpt = 0
	raw = []
	tmpboard = [[None]*width for _ in range(width)]
	return tmpboard

def nbr_of_neg(tmpboard, width):
	cmpt = 0
	match = 0
	test = 0
	col = 0
	while (cmpt < (width*width)):
		if tmpboard[col][test] != None:
			match += 1
		test += 1
		if test == width:
			test = 0
			col += 1
		cmpt += 1
	return match

def IDA_star(width, gameboard, finalboard):
	match = 0
	tmpboard = negative_board(width)
	print ("tmpboard")
	print (tmpboard)
	print ("finalboard")
	print (finalboard)
	match = nbr_of_neg(tmpboard,width)
	print ("match")
	print (match)
	raw = int(match / width)
	col = int(match % width)
	print ("raw")
	print (raw)
	print ("col")
	print (col)
	tmpboard[raw][col] = finalboard[raw][col]
	
	print ("finalboard")
	print (finalboard)
	print ("tmpboard")
	print (tmpboard)
	print ("match")
	print (match)

	current = manhattan(width, gameboard, tmpboard, match)


	print ("gameboard")
	print (gameboard)
	print ("current")
	print (current)
	print ("match")
	print (match)
	# sys.exit()



	while(1):
		tmp = IDA(width, gameboard, finalboard, tmpboard, 1, current, match)
		if tmp == 1:
			print ("allmoves")
			print (allmoves)
			print ("allmovesstring[::-1]")
			print (allmovesstring[::-1])
			break
			# return allmoves, allmovesstring[::-1]
		if tmp == float("inf"):
			return 'Fail', 'Fail'
		print ("TMP")
		print (tmp)
		print ("allmoves")
		print (allmoves)
		print ("allmovesstring[::-1]")
		print (allmovesstring[::-1])
		current = tmp    

j = 0
def IDA(width, gameboard, finalboard, tmpboard, g, current, match):
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


	match = 0
	print ("tmpboard")
	print (tmpboard)
	print ("finalboard")
	print (finalboard)
	print ("gameboard")
	print (gameboard)
	match = nbr_of_neg(tmpboard,width)
	print ("match")
	print (match)
	raw = int(match / width)
	col = int(match % width)
	print ("raw")
	print (raw)
	print ("col")
	print (col)

	if j == 0:    
		tmpboard[raw][col] = finalboard[raw][col]
		j += 1
	heuri = manhattan(width, gameboard, tmpboard, match)
	f = g + heuri
	
	if f > current:
		return f
	if gameboard[0][0] == tmpboard[0][0]:
		return 1

	minval = float('inf')

	for sibling in getNextStates(width, gameboard):
		tmp = IDA(width, sibling[0], finalboard, tmpboard, g + 1, current, match)

		if tmp == 1:
			allmoves += 1
			allmovesstring.append(sibling[1])
			return 1
		if tmp < minval:
			minval = tmp
	j += 1
	return minval