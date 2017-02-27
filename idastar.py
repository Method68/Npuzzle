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

def update_gameboard(gameboard, allmovesstring, width):
	
	print ("INSIDE UPDATE_GAMEBOARD")
	print ("len of allmovesstring")
	print (len(allmovesstring))
	print ("First gameboard")
	print (gameboard)
	print ("allmovesstring")
	print (allmovesstring)

	len_upt = len(allmovesstring) + 1
	cmpt = 0
	while (cmpt < len_upt):

		# Get the cell which contain 0
		for i in range(width):
			try:
				case = gameboard[i].index(0)
			except Exception as e:
				continue
			case= (i, case)
	
			# Store block0 position
			raw = i
			col = case[1]
			break
		# if all moves are done we exit
		if cmpt == allmoves:
			return gameboard

		# check next move	
		move = allmovesstring[0]

		#SWAP
		if (move == 'RIGHT'):
			gameboard[raw][col + 1] , gameboard[raw][col] = gameboard[raw][col], gameboard[raw][col + 1]
		elif (move == 'LEFT'):
			gameboard[raw][col - 1] , gameboard[raw][col] = gameboard[raw][col], gameboard[raw][col - 1]
		elif (move == 'UP'):
			gameboard[raw - 1][col] , gameboard[raw][col] = gameboard[raw][col], gameboard[raw - 1][col]
		elif (move == 'DOWN'):
			gameboard[raw + 1][col] , gameboard[raw][col] = gameboard[raw][col], gameboard[raw + 1][col]
		
		print ("AFTER MOVE gameboard")
		print (gameboard)

		#Remove actual MOVES for the next block to solve the next block
		allmovesstring.pop(0)		
		cmpt += 1

def IDA_star(width, gameboard, finalboard):
	match = 0
	final_list_moves = []
	final_all_moves = 0
	tmpboard = negative_board(width)
	match = nbr_of_neg(tmpboard,width)
	raw = int(match / width)
	col = int(match % width)
	tmpboard[raw][col] = finalboard[raw][col]
	current = manhattan(width, gameboard, tmpboard, match)



	while(1):
		tmp = IDA(width, gameboard, finalboard, tmpboard, 1, current, match)
		if tmp == 1:
			# # TEST THIS
			# # we need to find a way to solve the final list for the graphical interface
			# #

			# for stri in allmovesstring[::-1]:
			# 	final_list_moves.append(stri)
			# final_all_moves += allmoves
			# print ("final_list_moves")
			# print (final_list_moves)

			# # 
			# sys.exit()


			# Update gameboard before the next move otherwhise we always restart from 0
			gameboard = update_gameboard(gameboard, allmovesstring[::-1], width)
			match += 1
			print ("Final One more block gameboard !!!!")
			print (gameboard)

			if gameboard == finalboard:
				print ("Win win winwin !!!!")
				# The actual value of allmoves and allmovesstring are actually wrong
				# print ("final_list_moves")
				# print (final_list_moves)
				# return final_all_moves, final_list_moves
				return allmoves , allmovesstring
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


	raw = int(match / width)
	col = int(match % width)
	tmpboard[raw][col] = finalboard[raw][col]
	heuri = manhattan(width, gameboard, tmpboard, match)
	f = g + heuri	

	# Debug
	# We need to check if the the value sent by manhattan make sense
	# #
	# print ("IDA heuri")
	# print (heuri)
	# print ("IDA g")
	# print (g)
	# print ("IDA f")
	# print (f)
	# print ("IDA current")
	# print (current)

	if f > current:
		return f

	# Debug
	print ("IDA tmpboard")
	print (tmpboard)
	print ("IDA finalboard")
	print (finalboard)
	print ("IDA gameboard")
	print (gameboard)
	print ("IDA match")
	print (match)
	print ("IDA raw")
	print (raw)
	print ("IDA col")
	print (col)


	#this function check if all the tildes in tmpblock are matched by gameboard
	mathc_all_block = are_all_tildes_valid_untill_match_value(match, gameboard, tmpboard, width)
	if mathc_all_block == 1:
		print ("match all the actual tmpboard blocks")
		allmoves = 0
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