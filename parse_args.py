import argparse

def parse_args(parser):
    parser.add_argument('-f', dest="file_name", help='file name')
    parser.add_argument('-puzzle', dest="puzzle_type", help='puzzle type', choices=["snail", "classic", "reverse"], default="snail")
    parser.add_argument('-heuristic', dest="heuristic_type", help='heuristic type', choices=["Hamming", "OutRowCol", "Manhattan", "Conflict", "AngleConflict"], default="Manhattan")
    parser.add_argument('-algo', dest="algorithm", help='algorithm type', choices=["aStar", "greedy", "uniformCost"], default="aStar")
    parser.add_argument('-genPuzzle', dest="genPuzzleSize",type=int ,help='generate random puzzle (-genPuzzle SIZE)')
    parser.add_argument('-s', dest="solvable", help='generate random solvable puzzle', action='store_true')
    parser.add_argument('-u', dest="unsolvable", help='generate random unsolvable puzzle', action='store_true')
    parser.add_argument('-solveGenPuzzle', dest="solveGenPuzzle", help='generated puzzle will be solved (if solvable)', action='store_true')
    parser.add_argument('-heurPlot', dest="heurPlot", help='shows the plot of heuristic decreasing', action='store_true')
    parser.add_argument('-compStats', dest="compStats", help='comparing stats for 3 different heuristics', action='store_true')
    return parser.parse_args()
