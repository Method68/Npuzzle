import random, time, sys
import pygame
from heuristic import manhattan, euclidian, chebyshev
from idastar import IDA_star
from astar import aStar
from heapq import heapify, heappush, heappop

def set_board(liste, width):
	board = []
	k = 0
	for i in range(width):
		new = []
		for j in range(width):
			new.append(liste[k])
			k += 1
		board.append(new)
	return board

def set_finalboard(n):
	m = [[0] * n for i in range(n)]
	dx, dy = [0, 1, 0, -1], [1, 0, -1, 0]
	x, y, c = 0, -1, 1
	for i in range(n + n - 1):
		for j in range((n + n - i) // 2):
			x += dx[i % 4]
			y += dy[i % 4]
			if c == n*n:
				m[x][y] = 0
			else:
				m[x][y] = c
			c += 1
	return m

def loopOnBoardInversion(gameboardsimplearray, size):
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
	return inversion

def checkIfSolvable(gameboard, finalboard):
	gameboardsimplearray = []
	numberElem = -1
	for elem in gameboard:
		for value in elem:
			gameboardsimplearray.append(value)
		numberElem += 1
	positionZero = 0
	while(0 <= numberElem):
		for elem in gameboard[numberElem]:
			if elem == 0:
				positionZero = numberElem
		numberElem -= 1

	inversion = 0
	size = len(gameboardsimplearray)
	if size % 2 == 1:
		inversion = loopOnBoardInversion(gameboardsimplearray, size)
		print("\n\033[91mTotal inversion : \033[0m" + str(inversion))
		if(inversion % 2 == 0):
			return False
		else:
			return True
	else:
		if positionZero % 2 == 0:
			inversion = loopOnBoardInversion(gameboardsimplearray, size)
			print("\n\033[91mTotal inversion : \033[0m" + str(inversion))
			if (inversion % 2 == 1):
				return False
			else:
				return True
		else:
			inversion = loopOnBoardInversion(gameboardsimplearray, size)
			print("\n\033[91mTotal inversion : \033[0m" + str(inversion))
			if (inversion % 2 == 0):
				return False
			else:
				return True

def call_core(squareside, heuristic, algo, gamemode, filegameboard):
	solvable = None	
	dont_replay = 0
	if len(filegameboard):
		dont_replay = 1
	while (solvable == None):
		allvalue = squareside * squareside
		allcase_order = [x for x in range(0, allvalue)]
		allcase_order.pop(0)
		allcase_order.append(0)
		allcase = random.sample(range(allvalue),allvalue)
		finalboard = set_finalboard(squareside)
		if not len(filegameboard):
			gameboard = set_board(allcase, squareside)
		else:
			gameboard = filegameboard
		solvable = construct(squareside, gameboard, finalboard, heuristic, algo, gamemode)
		if (solvable != None):
			print ("\n\033[92mBoard Builded\033[0m\n")
			break
		else:
			print ("\n\033[91mBoard Not Builded\033[0m\n")
			if dont_replay == 1:
				print ("\033[92mNot solvable\033[0m")
				exit()
	return solvable, allcase


def construct(width, gameboard, finalboard, answers, algo, gamemode):
	
	allstatesselected = 0
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
	if gameboard == finalboard:
		print("\n\033[91mThis game board is Allready solve !\033[90m")
		return None
	checkifsolvable = checkIfSolvable(gameboard, finalboard)
	if (checkifsolvable == False):
		print("\n\033[91mThis game board is unsolvable !\033[90m")
		return None
	#Call A star, time instentiation
	if gamemode == 'ia':
		if answers == "Manhattan":
			print("\033[91mManhattan distance : \033[0m" + str(manhattan(width,gameboard,finalboard,1000)))
		elif answers == "Euclidian":
			print("\033[91mEuclidian distance : \033[0m" + str(euclidian(width,gameboard,finalboard,1000)))
		else:
			print("\033[91mChebyshev distance : \033[0m" + str(chebyshev(width,gameboard,finalboard,1000)))
		print("\n\033[95mprocessing : \033[0m")
		time1 = time.time()
		if algo == "Astar":
			print('\033[91mAlgorythm selected : \033[0m' + str(algo))
			seqCount, sequence, allstatesselected = aStar(width, gameboard, finalboard, answers, allstatesselected)
		else:
			print('\033[91mAlgorythm selected : \033[0m' + str(algo))
			seqCount, sequence, allstatesselected = IDA_star(width, gameboard, finalboard, answers, allstatesselected)
		#Time finished A star
		time2 = time.time()
		#Print time, number of move and all move to accomplite board
		print("\n\033[91mTime : \033[0m" + str(round(time2 - time1, 3)) + "scd")
		print("\033[91mNumber of move : \033[0m" + str(seqCount))
		print('\033[91mAll move : \033[0m\033[92m' + str(sequence))
		return sequence
	return ''