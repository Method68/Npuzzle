import random, time, sys
from math import sqrt

def manhattan(width, gameboard, finalboard, match):
	return_index = 0
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


def euclidian(width, gameboard, finalboard, match):
	return_index = 0
	result = 0
	for raw in range(width):
		for col in range(width):
			if (finalboard[raw][col] == 0):
				continue
			for l in range(width):
				for m in range(width):
					if (finalboard[raw][col] == gameboard[l][m]):
						result += sqrt((abs((m - col) * (m - col)) + abs((l - raw) * (l - raw))))
						if return_index == match:
							return result
						else:
							break
						return_index += 1
	result += 2
	return(result)

def chebyshev(width, gameboard, finalboard, match):
	return_index = 0
	result = 0
	for raw in range(width):
		for col in range(width):
			if (finalboard[raw][col] == 0):
				continue
			for l in range(width):
				for m in range(width):
					if (finalboard[raw][col] == gameboard[l][m]):
						result += max(abs(m - col), abs(l - raw))
						if return_index == match:
							return result
						else:
							break
						return_index += 1
	result += 2
	return(result)