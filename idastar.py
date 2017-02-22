import random, time, sys
load = 0

def idaStar(get_moves, puzzle, goal):
	import itertools
	
	def dfs(route, depth):
		next_route = None
		if depth == 0:
			return
		if route[-1] == goal:
			return depth, route
		for move in get_moves(route[-1]):
			if move not in route:
				next_route = dfs(route + [move], depth - 1)
			if next_route:
				return next_route

	for depth in itertools.count():
		route = dfs([puzzle], depth)
		if route:
			return depth, route

def num_moves(rows, cols):
	def get_moves(subject):
		moves = []
		global load

		syms = ['\\', '|', '/', '-']
		if load == 4:
			load = 0
		sys.stdout.write("\033[93m\b%s\033[0m"%syms[load])
		sys.stdout.flush()
		load += 1
		zrow, zcol = next((r, c)
		for r, l in enumerate(subject)
			for c, v in enumerate(l) if v == 0)
	
		def swap(row, col):
			import copy
			s = copy.deepcopy(subject)
			s[zrow][zcol], s[row][col] = s[row][col], s[zrow][zcol]
			return s

        # north
		if zrow > 0:
			moves.append(swap(zrow - 1, zcol))
        # east
		if zcol < cols - 1:
			moves.append(swap(zrow, zcol + 1))
        # south
		if zrow < rows - 1:
			moves.append(swap(zrow + 1, zcol))
        # west
		if zcol > 0:
			moves.append(swap(zrow, zcol - 1))

		return moves
	return get_moves
