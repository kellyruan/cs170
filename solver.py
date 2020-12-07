import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness
import sys
import itertools

def solve(G, s):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """

    # TODO: your code here!
    rooms = {}
    numRooms = 1
    maxHap = 0
    maxRooms = {}
    maxNumRooms = 0
    # print(G.edges(data=True))
    for perm in itertools.permutations([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]):
        while numRooms <= 10:
            studentsPerRoom = 10 // numRooms
            studentCountPerRoom = 0
            currRoom = 0
            for student in perm:
                rooms[student] = currRoom
                studentCountPerRoom += 1
                if studentCountPerRoom >= studentsPerRoom:
                    studentCountPerRoom = 0
                    currRoom += 1
            if is_valid_solution(rooms, G, s, numRooms):
                temp = calculate_happiness(rooms, G)
                if temp > maxHap:
                    maxHap = temp
                    maxRooms = rooms
                    maxNumRooms = numRooms
            rooms = {}
            numRooms += 1
        print(perm, maxHap)
        numRooms = 1
    print(maxRooms, maxNumRooms)
    return (maxRooms, maxNumRooms)


# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    G, s = read_input_file(path)
    D, k = solve(G, s)
    assert is_valid_solution(D, G, s, k)
    print("Total Happiness: {}".format(calculate_happiness(D, G)))
    write_output_file(D, 'test.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('file_path/inputs/*')
#     for input_path in inputs:
#         output_path = 'file_path/outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G, s = read_input_file(input_path, 100)
#         D, k = solve(G, s)
#         assert is_valid_solution(D, G, s, k)
#         cost_t = calculate_happiness(T)
#         write_output_file(D, output_path)
