import random, time, sys

def manhattan(width, gameboard, finalboard):
	result = 0
	for i in range(width):
		for j in range(width):
			if (finalboard[i][j] == 0):
				continue
			for l in range(width):
				for m in range(width):
					if (finalboard[i][j] == gameboard[l][m]):
						result += (abs (m - j) + abs (l - i))
						break
	return(result + 2)

# def manhattan(width, gameboard, finalboard):
# 	result = 0
# 	for i in range(width):
# 		for j in range(width):
# 			current = gameboard[i][j]
# 			if current is not 0:
# 				x_dist = abs(i - current / width)
# 				y_dist = abs(j - current % width)
# 				result += x_dist + y_dist
# 	return(result + 2)

def hamming_distance(width, gameboard, finalboard):
	gameboardsimplearray = ''
	for elem in gameboard:
		for value in elem:
			gameboardsimplearray += str(value)
	
	finalboardsimplearray = ''
	for elem in finalboard:
		for value in elem:
			finalboardsimplearray += str(value)

	return sum(el1 != el2 for el1, el2 in zip(gameboardsimplearray, finalboardsimplearray))
