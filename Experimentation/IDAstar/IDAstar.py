SOLVED = False
pTour = []
bound = h(pTour)

while not SOLVED:
	bound = DFS(root, depth=1, bound)


DFS(node, depth, bound):
	if h(node/pTour) = 0:
		SOLVED = True
		return bound

	









h(distances, pTour)  # MST Heueristic
