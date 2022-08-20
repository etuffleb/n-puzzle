import random
import validation as val

def generatePuzzle(fieldSize, terminal_state, solvable, unsolvable):
	genPuzzle = [i for i in range(fieldSize ** 2)]
	random.shuffle(genPuzzle)
	if (solvable == False and unsolvable == False) or solvable == True:
		while val.solvable(genPuzzle, terminal_state, fieldSize) == False:
			random.shuffle(genPuzzle)
		solv = True
	else:
		while val.solvable(genPuzzle, terminal_state, fieldSize) == True:
			random.shuffle(genPuzzle)
		solv = False
	return genPuzzle, solv
