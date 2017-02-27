import random, time, sys
import pygame
from heuristic import manhattan, euclidian, chebyshev
from idastar import IDA_star
from astar import aStar
from heapq import heapify, heappush, heappop

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

def checkIfSolvable(gameboard):
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
		if(inversion % 2 == 1):
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

def construct(width, gameboard, finalboard, answers, algo):
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
		print("\n\033[91mThis game board is unsolvable !\033[90m")
		return None
	#Call A star, time instentiation
	if answers == "\033[91mManhattan":
		print("\033[91mManhattan distance : \033[0m" + str(manhattan(width,gameboard,finalboard,1000)))
	elif answers == "\033[91mEuclidian":
		print("\033[91mEuclidian distance : \033[0m" + str(euclidian(width,gameboard,finalboard,1000)))
	else:
		print("\033[91mChebyshev distance : \033[0m" + str(chebyshev(width,gameboard,finalboard,1000)))
	print("\n\033[95mprocessing : \033[0m")
	time1 = time.time()
	if algo == "\033[91mAstar":
		seqCount, sequence = aStar(width, gameboard, finalboard, answers)
	else:
		seqCount, sequence, allstatesselected = IDA_star(width, gameboard, finalboard, answers)
	#Time finished A star
	time2 = time.time()

	#Print time, number of move and all move to accomplite board
	print("\n\033[91mTime : \033[0m" + str(round(time2 - time1, 3)) + "scd")
	print("\033[91mAll states selected : \033[0m" + str(allstatesselected))
	print("\033[91mNumber of move : \033[0m" + str(seqCount))
	print('\033[91mAll move : \033[0m\033[92m' + str(sequence))
	return sequence