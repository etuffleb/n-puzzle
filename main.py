import argparse
import numpy as np
import validation as V
import parse_args as P
import solver as sl
import puzzleGenerator as pG
import heurPlot as hP

class Puzzle:
    def __init__(self, current_puzzle, terminal_puzzle, field_size, heuristic_name, algo):
        self.current_state = current_puzzle
        self.terminal_state = terminal_puzzle
        self.fieldSize = field_size
        self.heuristicName = heuristic_name
        self.algo = algo

def fill_snail_state(n):
    mat = [[0]*n for i in range(n)]
    st, m = 1, 0
    for v in range(n//2):
        for i in range(n-m):
            mat[v][i + v] = st
            st += 1
        for i in range(v+1, n-v):
            mat[i][-v - 1] = st
            st += 1
        for i in range(v + 1, n - v):
            mat[-v - 1][-i - 1] =st
            st += 1
        for i in range(v + 1, n - (v + 1)):
            mat[-i-1][v]=st
            st+=1
        m+=2
    snail_state = []
    for i in range(n):
        snail_state += mat[i]
    if n ** 2 in snail_state:
        snail_state[snail_state.index(n * n)] = 0
    return snail_state

def generate_terminal_puzzle(size, puzzle_type):
    if puzzle_type == "classic":
        return list(range(1, size ** 2)) + [0]
    elif puzzle_type == "reverse":        
        return list(range(size ** 2 - 1, -1, -1))
    elif puzzle_type == "snail":
        return fill_snail_state(size)

def delete_zero(puzzle):
    new_puzzle = [int(el) if el != 0 else None for el in puzzle]
    return np.array(new_puzzle)

def main():
    parser = argparse.ArgumentParser(add_help=True, conflict_handler='resolve')
    args = P.parse_args(parser)
    if args.file_name == None and args.genPuzzleSize == None:
        print('Error! File name (using -f) or command for generating puzzle (-genPuzzle) must be given!')
        exit()
    if args.file_name != None and args.genPuzzleSize != None:
        print('Error! You can choose only one of flags: file name (-f) or generating puzzle (-genPuzzle)!')
        exit()
    if args.file_name != None:
        if args.solvable == True or args.unsolvable == True or args.solveGenPuzzle == True:
            print("Error! Flags -s, -u and -solveGenPuzzle mustn't be used with -f flag!")
            exit()
        current_puzzle, size = V.valid_map(V.read_file(args.file_name))
        V.valid_puzzle(current_puzzle, size)
        terminal_puzzle = generate_terminal_puzzle(size, args.puzzle_type)
        if V.solvable(current_puzzle, terminal_puzzle, size) == True:
            print('Puzzle is solvable!')
        else:
            print('Puzzle is unsolvable!')
            exit()
    if args.genPuzzleSize != None:
        size = args.genPuzzleSize
        if size < 3:
            print("Size < 3, enter size => 3")
            exit()
        terminal_puzzle = generate_terminal_puzzle(size, args.puzzle_type)
        if args.solvable == True and args.unsolvable == True:
            print("We can't generate the puzzle that is solvable and unsolvable the same time! Use only one of -s or -u")
            exit()
        current_puzzle, solv = pG.generatePuzzle(size, terminal_puzzle, args.solvable, args.unsolvable)
        if solv == False:
            if args.solveGenPuzzle == True:
                print("We can't solve unsolvable puzzle! Here it is, you can try yourself!")
            else:
                print('Generated unsolvable puzzle:')
            sl.printState(size, current_puzzle)
            exit()
        print('Generated solvable puzzle:')
        sl.printState(size, current_puzzle)
        if args.solveGenPuzzle == False:
            exit()
    current_puzzle, terminal_puzzle = delete_zero(current_puzzle), delete_zero(terminal_puzzle)
    str_puzzle = Puzzle(current_puzzle, terminal_puzzle, size, args.heuristic_type, args.algorithm)
    if args.compStats == True:
        heurList = ['Hamming', 'Manhattan', 'Conflict']
        stats = dict()
        for heur in heurList:
            str_puzzle.heuristicName = heur
            solver = sl.solver(str_puzzle)
            stats[heur] = sl.getStats(solver)
            del solver
        hP.showCompareHeurs(stats)
    else:
        solver = sl.solver(str_puzzle)
        answerChain = sl.printSolution(solver)
        if args.heurPlot == True:
            hP.showHeurPlot(answerChain, str_puzzle.algo)

if __name__ == '__main__':
    main()
