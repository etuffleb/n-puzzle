import numpy as np

def read_file(file_name):
    try:
        with open(file_name, 'r') as f:
            map = f.readlines()
    except IOError:
        print("File not found")
        exit()
    except Exception:
        print("Cannot read from file")
        exit()
    return map

def valid_puzzle(puzzle, size):
    full_size = size * size
    possible_numbers = list(range(full_size))
    for i in range(full_size):
        if i in puzzle:
            possible_numbers.remove(i)
        else:
            print("A puzzle of size {0} must contain only numbers from 0 to {1}".format(full_size, full_size - 1))
            exit()
    if len(possible_numbers) != 0:
        print("A puzzle of size {0} must contain all numbers from 0 to {1}\n{2} is/are missing".format(full_size, full_size - 1, possible_numbers))
        exit()

def valid_map(map):
    size = 0
    sizeExist = False
    puzzle = []
    for line in map:
        if line.startswith("#"):
            continue
        line = line.split('#')[0].strip(' \t\n\r')
        numbers = get_numbers(line)
        if len(numbers) == 1 and not sizeExist:
            size = numbers[0]
            sizeExist = True
        elif len(numbers) == 1 and sizeExist:
            print("There are extra digit")
            exit()
        else:
            if len(numbers) != size and len(numbers) != 0:
                print("The number of elements in line doesn't match the declared number")
                exit()
            puzzle += numbers
    if size < 3:
        print("No size or size < 3")
        exit()
    if len(puzzle) != size * size:
        print("The number of rows must be equal to the number of columns")
        exit()
    return puzzle, size

def get_numbers(line):
    numbers = []
    split_line = line.split()
    for i in split_line:
        if i.isdigit():
            numbers.append(int(i))
        else:
            print("There are only numbers and comments can be included in line")
            exit()
    return numbers

def inversionNumber(puzzle):
    inversionNum = 0
    for i in range(len(puzzle) - 1):
        for j in range(i, len(puzzle)):
            if (puzzle[i] != 0 and puzzle[j] != 0
                and puzzle[i] > puzzle[j]):
                inversionNum += 1
    return inversionNum

def isSolvableClassic(size, invNum, emptyPositionRow):
    if size % 2 == 1:
        if invNum % 2 == 0:
            return True
    else:
        if emptyPositionRow % 2 == 0:
            if invNum % 2 == 1:
                return True
        else:
            if invNum % 2 == 0:
                return True
    return False

def solvable(current_puzzle, terminal_puzzle, size):
    invNum = inversionNumber(current_puzzle)
    termInvNum = inversionNumber(terminal_puzzle)
    emptyRow = current_puzzle.index(0) // size
    termEmptyRow = terminal_puzzle.index(0) // size
    if isSolvableClassic(size, invNum, emptyRow) == isSolvableClassic(size, termInvNum, termEmptyRow):
        return True
    else:
        return False
