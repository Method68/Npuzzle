import random, time, sys
import pygame
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
		if positionZero % 2 == 1:
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

def construct(width, gameboard, finalboard):
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
	print("\n\033[95mprocessing : \033[0m")
	time1 = time.time()
	#if width > 3:
	seqCount, sequence = IDA_star(width, gameboard, finalboard)
	#else:
	#	seqCount, sequence = aStar(width, gameboard, finalboard)
	#Time finished A star
	time2 = time.time()

	#Print time, number of move and all move to accomplite board
	print("\n\033[91mTime : \033[0m" + str(round(time2 - time1, 3)) + "scd")
	print("\033[91mNumber of move : \033[0m" + str(seqCount))
	print('\033[91mAll move : \033[0m\033[92m' + str(sequence))
	return sequence