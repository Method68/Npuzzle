import random, time, sys
from heuristic import manhattan, euclidian, chebyshev
import core_solver

allmoves = 0
i = 0
allmovesstring = []
lastmoves = []
final_list_moves = []

def getNextStates (width, current, state):
	nextStates = []
	case = None

	for i in range(width):
		try:
			case = current[i].index(0)
		except Exception as e:
			continue
		case = (i, case)
		break

	if (case[1] < (width - 1) and state != 'LEFT'):
		a = [i[:] for i in current]
		a[case[0]][case[1]], a[case[0]][case[1] + 1] = a[case[0]][case[1] + 1], a[case[0]][case[1]]
		nextStates.append((a, 'RIGHT'))

	if (case[1] > 0 and state != 'RIGHT'):
		b = [i[:] for i in current]
		b[case[0]][case[1]], b[case[0]][case[1] - 1] = b[case[0]][case[1] - 1], b[case[0]][case[1]]
		nextStates.append((b, 'LEFT'))

	if (case[0] > 0 and state != 'DOWN'):
		c = [i[:] for i in current]
		c[case[0]][case[1]], c[case[0] - 1][case[1]] = c[case[0] - 1][case[1]], c[case[0]][case [1]]
		nextStates.append((c, 'UP'))

	if (case[0] < (width - 1) and state != 'UP'):
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

def update_gameboard(gameboard, allmovesstring, width):
	len_upt = len(allmovesstring) + 1
	cmpt = 0
	while (cmpt < len_upt):
		for i in range(width):
			try:
				case = gameboard[i].index(0)
			except Exception as e:
				continue
			case= (i, case)
			raw = i
			col = case[1]
			break
		if cmpt == allmoves:
			return gameboard
		move = allmovesstring[0]
		if (move == 'RIGHT'):
			gameboard[raw][col + 1] , gameboard[raw][col] = gameboard[raw][col], gameboard[raw][col + 1]
		elif (move == 'LEFT'):
			gameboard[raw][col - 1] , gameboard[raw][col] = gameboard[raw][col], gameboard[raw][col - 1]
		elif (move == 'UP'):
			gameboard[raw - 1][col] , gameboard[raw][col] = gameboard[raw][col], gameboard[raw - 1][col]
		elif (move == 'DOWN'):
			gameboard[raw + 1][col] , gameboard[raw][col] = gameboard[raw][col], gameboard[raw + 1][col]
		final_list_moves.append(allmovesstring[0])
		allmovesstring.pop(0)		
		cmpt += 1

def IDA_star(width, gameboard, finalboard, answers, allstatesselected):
	global final_list_moves
	match = 0
	final_list_moves = []
	final_all_moves = 0
	tmpboard = negative_board(width)
	match = nbr_of_neg(tmpboard,width)
	raw = int(match / width)
	col = int(match % width)
	tmpboard[raw][col] = finalboard[raw][col]
	if answers == "Manhattan":
		current = manhattan(width, gameboard, tmpboard, match)
	elif answers == "Euclidian":
		current = euclidian(width, gameboard, tmpboard, match)
	else:
		current = chebyshev(width, gameboard, tmpboard, match)
	laststate = None
	while(1):
		tmp, allstatesselected = IDA(width, gameboard, finalboard, tmpboard, 1, current, match, laststate, answers, allstatesselected)
		if tmp == 1:
			gameboard = update_gameboard(gameboard, allmovesstring[::-1], width)
			print(gameboard)
			match += 1
			if gameboard == finalboard:
				for elem in final_list_moves:
					final_all_moves += 1
				print ("Total all states selected = " + str(allstatesselected))
				return final_all_moves, final_list_moves, allstatesselected
		elif tmp == float("inf"):
			return 'Fail', 'Fail'
		current = tmp

def are_all_tildes_valid_untill_match_value(match, gameboard, tmpboard, width):
	cmpt = 0
	can_exit = 0
	while (cmpt <= match):
		raw = int(cmpt / width)
		col = int(cmpt % width)
		if gameboard[raw][col] == tmpboard[raw][col]:
			can_exit += 1
		cmpt += 1
	if can_exit == match + 1:
		return 1

allstatesselected = 0
def IDA(width, gameboard, finalboard, tmpboard, g, current, match, laststate, answers, allstatesselected):
	global allmoves
	global allmovesstring
	global i


	####################
	#load view in terminal
	syms = ['\\', '|', '/', '-']
	if i == 4:
		i = 0
	sys.stdout.write("\033[93m\b%s\033[0m"%syms[i])
	sys.stdout.flush()
	i += 1
	####################

	raw = int(match / width)
	col = int(match % width)
	tmpboard[raw][col] = finalboard[raw][col]
	if answers == "Manhattan":
		heuri = manhattan(width, gameboard, tmpboard, match)
	elif answers == "Euclidian":
		heuri = euclidian(width, gameboard, tmpboard, match)
	else:
		heuri = chebyshev(width, gameboard, tmpboard, match)

	f = g + heuri

	if f > current:
		return f, allstatesselected

	#this function check if all the tildes in tmpblock are matched by gameboard
	mathc_all_block = are_all_tildes_valid_untill_match_value(match, gameboard, tmpboard, width)
	if mathc_all_block == 1:
		allmoves = 0
		return 1, allstatesselected

	minval = float('inf')
	for sibling in getNextStates(width, gameboard, laststate):
		###############
		#save last move for don't get inversion in getnextstates
		laststate = sibling[1]
		allstatesselected += 1
		###############
		tmp, allstatesselected = IDA(width, sibling[0], finalboard, tmpboard, g + 1, current, match, laststate, answers, allstatesselected)
		if tmp == 1:
			allmoves += 1
			allmovesstring.append(sibling[1])
			return 1, allstatesselected
		if tmp < minval:
			minval = tmp
	return minval, allstatesselected