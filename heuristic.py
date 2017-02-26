import random, time, sys

# def coords_of_tile(state, tile_to_find):
# 	for x, column in enumerate(state):
# 		for y, tile in enumerate(column):
# 			if tile == tile_to_find:
# 				return x, y

# def manhattan(width, gameboard, finalboard):
# 	total_distance = 0
# 	for column in gameboard:
# 		for tile in column:
# 			current_coords, desired_coords = coords_of_tile(gameboard, tile), coords_of_tile(finalboard, tile)
# 			total_distance += abs(current_coords[0] - desired_coords[0]) + abs(current_coords[1] - desired_coords[1])
# 	total_distance += 2
# 	return total_distance

def manhattan(width, gameboard, finalboard, match):
	return_index = 1
	result = 0
	for raw in range(width):
		for col in range(width):
			if (finalboard[raw][col] == 0):
				continue
			for l in range(width):
				for m in range(width):
					if (finalboard[raw][col] == gameboard[l][m]):
						result += (abs (m - col) + abs (l - raw))
						if return_index == match:
							return result
						else:
							break
						return_index += 1
	result += 2
	return(result)

# def manhattan(width, gameboard, finalboard):
# 	result = 0
# 	for raw in range(width):
# 		for col in range(width):
# 			current = gameboard[raw][col]
# 			if current is not 0:
# 				x_dist = abs(raw - current / width)
# 				y_dist = abs(col - current % width)
# 				result += x_dist + y_dist
# 	result += 2
# 	return(result)

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
