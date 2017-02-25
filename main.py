import random, time, sys
import pygame
from idastar import IDA_star
from astar import aStar
from heuristic import manhattan
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
	manhatanDist = manhattan(width, gameboard, finalboard)
	print("\n\033[95mprocessing : \033[0m")
	time1 = time.time()
	#if width > 3:
	seqCount, sequence = IDA_star(width, gameboard, finalboard)
	#else:
	#seqCount, sequence = aStar(width, gameboard, finalboard)
	#Time finished A star
	time2 = time.time()

	#Print time, number of move and all move to accomplite board
	print("\n\033[91mTime : \033[0m" + str(round(time2 - time1, 3)) + "scd")
	print("\033[91mManhattan distance : \033[0m" + str(manhatanDist))
	print("\033[91mNumber of move : \033[0m" + str(seqCount))
	print('\033[91mAll move : \033[0m\033[92m' + str(sequence))
	return

if __name__ == '__main__':
	width = input('\033[92mChoose size for Npuzzle: \n')
	construct(width)