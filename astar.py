import random, time, sys
import queue as Q
from heuristic import manhattan
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
		a = [i.copy() for i in current]
		a[empty[0]][empty[1]], a[empty[0]][empty[1] + 1] = a[empty[0]][empty[1] + 1], a[empty[0]][empty[1]]
		nextStates.append(('RIGHT', a, (empty[0], empty[1] + 1)))

	if (empty[1] > 0 and laststate != 'RIGHT'):
		b = [i.copy() for i in current]
		b[empty[0]][empty[1]], b[empty[0]][empty[1] - 1] = b[empty[0]][empty[1] - 1], b[empty[0]][empty[1]]
		nextStates.append(('LEFT', b, (empty[0], empty[1] - 1)))

	if (empty[0] > 0 and laststate != 'DOWN'):
		c = [i.copy() for i in current]
		c[empty[0]][empty[1]], c[empty[0] - 1][empty[1]] = c[empty[0] - 1][empty[1]], c[empty[0]][empty [1]]
		nextStates.append(('UP', c, (empty[0] - 1, empty[1])))

	if (empty[0] < (width - 1) and laststate != 'UP'):
		d = [i.copy() for i in current]
		d[empty[0]][empty[1]], d[empty[0] + 1][empty [1]] = d[empty[0] + 1][empty[1]], d[empty[0]][empty [1]]
		nextStates.append(('DOWN', d, (empty[0] + 1, empty[1])))
	return (nextStates)

def aStar (width, gameboard, finalboard):
	current = (manhattan(width, gameboard, finalboard), 0, [], gameboard)
	stateTree = [current]
	print("Estimate manhatan distance : " + str(current[0]))
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
		state = None
		for elem in current[2]:
			state = elem
		for state in getNextStates(width, current[-1], state):
			heappush(stateTree,  (manhattan(width, state[1], finalboard) + current[1] + 1, current[1] + 1, current[2] + [state[0]], state[1]))
	return (current[1], current[2])
