import random

def calculateManhattanDistance(matrix, goal):
	size  = len(matrix)
	for i in range(size):
		for j in range(size):
			value = matrix[i][j]
			valuegoal = goal[i][j]
			if(value != 0):
				resX = abs(value % size - valuegoal % size)
				resY = abs(value / size - valuegoal / size)
				manhattanDistanceSum = resX + resY
	return manhattanDistanceSum

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

	#Find start position, 0 is start position
	print("\nGAME BOARD")
	posrow = 0
	for row in gameboard:
		posZero = 0
		for elem in row:
			if elem == 0:
				startrow = posrow
				startPos = posZero
			posZero += 1
		posrow += 1
		print(str(row))

	print("\nFINAL BOARD")
	for row in finalboard:
		print(str(row))

	print("\nRow to start : " + str(startrow))
	print("Position in row to start : " + str(startPos))
	print("Value to start : " + str(gameboard[startrow][startPos]))

	toto = calculateManhattanDistance(gameboard, finalboard)
	print(toto)
	return

if __name__ == '__main__':
	width = input('\033[92mChoose width for Npuzzle: \n')
	construct(width)