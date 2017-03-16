import random, time, sys
from heuristic import manhattan, euclidian, chebyshev
from heapq import heapify, heappush, heappop

test = 0
def getNextStates (width, current, laststate):
	nextStates = []
	empty = None
	global test
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
		nextStates.append(('RIGHT', a, (empty[0], empty[1] + 1)))

	if (empty[1] > 0 and laststate != 'RIGHT'):
		b = [i[:] for i in current]
		b[empty[0]][empty[1]], b[empty[0]][empty[1] - 1] = b[empty[0]][empty[1] - 1], b[empty[0]][empty[1]]
		nextStates.append(('LEFT', b, (empty[0], empty[1] - 1)))

	if (empty[0] > 0 and laststate != 'DOWN'):
		c = [i[:] for i in current]
		c[empty[0]][empty[1]], c[empty[0] - 1][empty[1]] = c[empty[0] - 1][empty[1]], c[empty[0]][empty [1]]
		nextStates.append(('UP', c, (empty[0] - 1, empty[1])))

	if (empty[0] < (width - 1) and laststate != 'UP'):
		d = [i[:] for i in current]
		d[empty[0]][empty[1]], d[empty[0] + 1][empty [1]] = d[empty[0] + 1][empty[1]], d[empty[0]][empty [1]]
		nextStates.append(('DOWN', d, (empty[0] + 1, empty[1])))
	return (nextStates)
 
def aStar (width, gameboard, finalboard, answers, allstatesselected):
	allstatesselected = 0
	if answers == "Manhattan":
		current = (manhattan(width, gameboard, finalboard, 1000), 0, [], gameboard)
	elif answers == "Euclidian":
		current = (euclidian(width, gameboard, finalboard, 1000), 0, [], gameboard)
	else:
		current = (chebyshev(width, gameboard, finalboard, 1000), 0, [], gameboard)
	stateTree = [current]

	# print ("first state of tree")
	# print (stateTree)
	heapify(stateTree)
	Sizecomplexity = 0
	Timecomplexity = 0
	i = 0
	while (not current[-1] == finalboard):
		####################
		#load view in terminal
		syms = ['\\', '|', '/', '-']
		if i == 4:
			i = 0
		sys.stdout.write("\033[93m\b%s\033[0m"%syms[i])
		sys.stdout.flush()
		i += 1
		####################
		current = heappop(stateTree)
		# print ("First heappop")
		# print (current)
		state = None
		for elem in current[2]:
			state = elem
		for state in getNextStates(width, current[-1], state):
			Timecomplexity += 1
			if answers == "Manhattan":
				heappush(stateTree,  (manhattan(width, state[1], finalboard, 1000) + current[1] + 1, current[1] + 1, current[2] + [state[0]], state[1]))
			elif answers == "Euclidian":
				heappush(stateTree,  (euclidian(width, state[1], finalboard, 1000) + current[1] + 1, current[1] + 1, current[2] + [state[0]], state[1]))
			else:
				heappush(stateTree,  (chebyshev(width, state[1], finalboard, 1000) + current[1] + 1, current[1] + 1, current[2] + [state[0]], state[1]))
			if (len(stateTree) > Sizecomplexity):
				Sizecomplexity = len(stateTree)
			# print (stateTree)
			# if test == 4:
			# 	sys.exit()
			allstatesselected += 1
	print ("\033[91mComplexity in Size : \033[0m" + str(Sizecomplexity))
	print ("\033[91mComplexity in Time : \033[0m" + str(Timecomplexity))
	# Total of all state selected in each open state from the beggining
	for groupes in stateTree:
		for listmoves in groupes[2]:
			allstatesselected += len(listmoves) 
	return current[1], current[2] , allstatesselected
