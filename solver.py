import numpy as np
from heapq import heappush as insert, heappop as extract
import time

def distHamming(tmp, term, fieldSize):
	dist = 0
	for i in range(fieldSize ** 2):
		if tmp[i] != term[i] and term[i] != None:
			dist += 1
	return dist

def distOutRowCol(tmp, term, fieldSize):
	dist = 0
	for i in range(fieldSize ** 2):
		j = np.where(term == tmp[i])[0][0]
		if term[j] != None:
			if i // fieldSize != j // fieldSize:
				dist += 1
			if i % fieldSize != j % fieldSize:
				dist += 1
	return dist

def distManhattan(tmp, term, fieldSize):
	dist = 0
	for i in range(fieldSize ** 2):
		if tmp[i] != None:
			j = np.where(term == tmp[i])[0][0]
			dist += abs(j // fieldSize - i // fieldSize) + abs(j % fieldSize - i % fieldSize)
	return dist

def distLinConflict(tmp, term, fieldSize):
	dist = distManhattan(tmp, term, fieldSize)
	for rowNum in range(fieldSize):
		for i1 in range(fieldSize - 1):
			for i2 in range(i1 + 1, fieldSize):
				ind1 = np.where(term == tmp[rowNum * fieldSize + i1])[0][0]
				ind2 = np.where(term == tmp[rowNum * fieldSize + i2])[0][0]
				if (term[ind1] is not None and term[ind2] is not None
					and ind1 // fieldSize == rowNum
					and ind2 // fieldSize == rowNum
					and ind1 % fieldSize > ind2 % fieldSize):
					dist += 2
	for colNum in range(fieldSize):
		for i1 in range(fieldSize - 1):
			for i2 in range(i1 + 1, fieldSize):
				ind1 = np.where(term == tmp[colNum + fieldSize * i1])[0][0]
				ind2 = np.where(term == tmp[colNum + fieldSize * i2])[0][0]
				if (term[ind1] is not None and term[ind2] is not None
					and ind1 % fieldSize == colNum
					and ind2 % fieldSize == colNum
					and ind1 // fieldSize > ind2 // fieldSize):
					dist += 2
	return dist

def distAngleConflict(tmp, term, fieldSize):
	dist = distLinConflict(tmp, term, fieldSize)
	if (tmp[0] != term[0] and 
		tmp[0] is not None and term[0] is not None and
		tmp[1] == term[1] and tmp[1] is not None and
		tmp[fieldSize] == term[fieldSize] and tmp[fieldSize] is not None):
		dist += 2
	if (tmp[fieldSize - 1] != term[fieldSize - 1] and 
		tmp[fieldSize - 1] is not None and term[fieldSize - 1] is not None and
		tmp[fieldSize - 2] == term[fieldSize - 2] and tmp[fieldSize - 2] is not None and
		tmp[2 * fieldSize - 1] == term[2 * fieldSize - 1] and tmp[2 * fieldSize - 1] is not None):
		dist += 2
	if (tmp[fieldSize * (fieldSize - 1)] != term[fieldSize * (fieldSize - 1)] and
		tmp[fieldSize * (fieldSize - 1)] is not None and term[fieldSize * (fieldSize - 1)] is not None and
		tmp[fieldSize * (fieldSize - 1) + 1] == term[fieldSize * (fieldSize - 1) + 1]
		and tmp[fieldSize * (fieldSize - 1) + 1] is not None and
		tmp[fieldSize * (fieldSize - 2)] == term[fieldSize * (fieldSize - 2)] 
		and tmp[fieldSize * (fieldSize - 2)] is not None):
		dist += 2
	if (tmp[fieldSize ** 2 - 1] != term[fieldSize ** 2 - 1] and
		tmp[fieldSize ** 2 - 1] is not None and term[fieldSize ** 2 - 1] is not None and
		tmp[fieldSize ** 2 - 2] == term[fieldSize ** 2 - 2] and tmp[fieldSize ** 2 - 2] is not None and
		tmp[fieldSize * (fieldSize - 1) - 1] == term[fieldSize * (fieldSize - 1) - 1] and 
		tmp[fieldSize * (fieldSize - 1) - 1] is not None):
		dist += 2
	return dist

nameToFunc = {
	'Hamming': distHamming,
	'OutRowCol': distOutRowCol,
	'Manhattan': distManhattan,
	'Conflict': distLinConflict,
	'AngleConflict': distAngleConflict
}

class node(object):
	def __init__(self, state, valG, parent, solver):
		self.state = state
		self.parent = parent
		self.G = 0 if solver.algo == 'greedy' else valG
		self.H = 0 if solver.algo == 'uniformCost' else nameToFunc[solver.heuristicName](state, solver.terminalState, solver.fieldSize)
		self.F = valG + self.H

	def __eq__(self, other):
		return np.array_equal(self.state, other.state)

	def __lt__(self, other):
		if self.F < other.F:
			return self.F < other.F
		if self.H < other.H:
			return self.H < other.H
		return self.G < other.G

class solver(object):
	def __init__(self, puzzle):
		self.initialState = puzzle.current_state
		self.terminalState = puzzle.terminal_state
		self.fieldSize = puzzle.fieldSize
		self.heuristicName = puzzle.heuristicName
		self.algo = puzzle.algo
		initialNode = node(self.initialState, 0, None, self)
		self.openNodes = []
		insert(self.openNodes, (initialNode.F, initialNode))
		self.closedNodes = []
		self.closedStates = set()
		print('Solving with heuristic ' + self.heuristicName + ' and algorithm ' + self.algo + '...')
		start_time = time.time()
		self.finalNode = self.solve()
		self.timeDiff = time.time() - start_time
		print('Done!')
	
	def moveNone(self, state, indNone, directions):
		generatedStates = []
		for direction in directions:
			newState = state.copy()
			if direction == 'up':
				newState[indNone - self.fieldSize], newState[indNone] = newState[indNone], newState[indNone - self.fieldSize]
			if direction == 'down':
				newState[indNone + self.fieldSize], newState[indNone] = newState[indNone], newState[indNone + self.fieldSize]
			if direction == 'left':
				newState[indNone - 1], newState[indNone] = newState[indNone], newState[indNone - 1]
			if direction == 'right':
				newState[indNone + 1], newState[indNone] = newState[indNone], newState[indNone + 1]
			if not ''.join([str(num) for num in newState]) in self.closedStates:
				generatedStates.append(newState)
		return generatedStates

	def generateStates(self, tmpNode):
		i = np.where(tmpNode.state == None)[0][0]
		directions = ['up', 'left', 'down', 'right']
		if i // self.fieldSize == 0:
			directions.remove('up')
		if i // self.fieldSize == self.fieldSize - 1:
			directions.remove('down')
		if i % self.fieldSize == 0:
			directions.remove('left')
		if i % self.fieldSize == self.fieldSize - 1:
			directions.remove('right')
		generatedStates = self.moveNone(tmpNode.state, i, directions)
		for state in generatedStates:
			stateNode = node(state, tmpNode.G + 1, tmpNode, self)
			insert(self.openNodes, (stateNode.F, stateNode))

	def findMinH(self, lst):
		minH = min([el.H for el in lst])
		for el in lst:
			if el.H == minH:
				break
		lst.remove(el)
		return el

	def solve(self):
		while True:
			tmpNode = extract(self.openNodes)[1]
			if np.array_equal(tmpNode.state, self.terminalState):
				return tmpNode
			self.generateStates(tmpNode)
			self.closedNodes.append(tmpNode)
			self.closedStates.add(''.join([str(num) for num in tmpNode.state]))
	
def printState(fieldSize, state):
	maxNumLen = len(str(fieldSize ** 2 - 1)) + 1
	for i in range(fieldSize):
		for j in range(fieldSize):
			tmpNum = str(state[i * fieldSize + j]) if state[i * fieldSize + j] != None and state[i * fieldSize + j] != 0 else ''
			print(tmpNum + ' ' * (maxNumLen - len(tmpNum)), end='')
		print('\n', end='')

def printSolution(solver):
	print('Time spent:', round(solver.timeDiff, 3), 'seconds')
	print('Number of states ever selected from opened set:', len(solver.closedStates))
	print('Number of states ever represented in memory:', len(solver.closedStates) + len(solver.openNodes))
	tmpNode = solver.finalNode
	chain = list()
	while tmpNode.parent is not None:
		chain.append(tmpNode)
		tmpNode = tmpNode.parent
	chain.append(tmpNode)
	print('Number of moves needed:', len(chain) - 1)
	print('The sequence of states tending to the answer:')
	chain.reverse()
	for nod in chain:
		print('')
		printState(solver.fieldSize, nod.state)
	print('')
	return chain

def getStats(solver):
	tmpNode = solver.finalNode
	chain = list()
	while tmpNode.parent is not None:
		chain.append(tmpNode)
		tmpNode = tmpNode.parent
	chain.append(tmpNode)
	return (round(solver.timeDiff, 3), len(solver.closedStates), len(solver.closedStates) + len(solver.openNodes), len(chain) - 1)
