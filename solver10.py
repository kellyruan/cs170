import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness
import sys
import itertools
import glob
import os
import numpy as np

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
    used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
    edgeCount = 0
    maxHap = 0
    maxRooms = {}
    maxNumRooms = 1
    # for i in G.edges(data=True):
    #     print (i[2])
    # edges = list(G.edges(data=True))
    # edges.sort(key=lambda x: x[2]["happiness"], reverse=True)
    # while used < G.number_of_nodes():
    #     edges[edgeCount]
    # # print(len(list(G.edges)))
    # print(temp)
    # for perm in itertools.permutations([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]):
    # for i in range(500):
    #     perm = np.random.permutation(50)
    #     currRoom = 0
    #     for student in perm:
    #
    #     # while numRooms <= 50:
    #         # studentsPerRoom = 50 // numRooms
    #         # studentCountPerRoom = 0
    #         # currRoom = 0
    #         # for student in perm:
            #     rooms[student] = currRoom
            #     studentCountPerRoom += 1
            #     if studentCountPerRoom >= studentsPerRoom:
            #         studentCountPerRoom = 0
            #         currRoom += 1
        #     if is_valid_solution(rooms, G, s, numRooms):
        #         temp = calculate_happiness(rooms, G)
        #         if temp > maxHap:
        #             maxHap = temp
        #             maxRooms = rooms
        #             maxNumRooms = numRooms
        #         print(perm, temp)
        #     rooms = {}
        #     numRooms += 1
        # # print(perm, maxHap)
        # rooms = {}
        # numRooms = 1
    numRooms = 1
    for student in range(10):
        rooms[student] = 0
    if is_valid_solution(rooms, G, s, numRooms):
            temp = calculate_happiness(rooms, G)
            if temp > maxHap:
                maxHap = temp
                maxRooms = rooms
                maxNumRooms = numRooms
    rooms = {}
    used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
    numRooms = 2
    for i in range(1, 10):
        for comb in itertools.combinations(used, i):
            for student in comb:
                rooms[student] = 0
                used.remove(student)
            for student in used:
                rooms[student] = 1
            if is_valid_solution(rooms, G, s, numRooms):
                    temp = calculate_happiness(rooms, G)
                    if temp > maxHap:
                        maxHap = temp
                        maxRooms = rooms
                        maxNumRooms = numRooms
            rooms = {}
            used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
    numRooms = 3
    for i in range(1, 10):
        for comb1 in itertools.combinations(used, i):
            for student in comb1:
                rooms[student] = 0
                used.remove(student)
            rooms1 = dict(rooms)
            used1 = set(used)
            for j in range(1, 10-i):
                for comb2 in itertools.combinations(used, j):
                    for student in comb2:
                        rooms[student] = 1
                        used.remove(student)
                    for student in used:
                        rooms[student] = 2
                    if is_valid_solution(rooms, G, s, numRooms):
                            temp = calculate_happiness(rooms, G)
                            if temp > maxHap:
                                maxHap = temp
                                maxRooms = rooms
                                maxNumRooms = numRooms
                    rooms = dict(rooms1)
                    used = set(used1)
            rooms = {}
            used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
    numRooms = 4
    for i in range(1, 10):
        for comb1 in itertools.combinations(used, i):
            for student in comb1:
                rooms[student] = 0
                used.remove(student)
            rooms1 = dict(rooms)
            used1 = set(used)
            for j in range(1, 10-i):
                for comb2 in itertools.combinations(used, j):
                    for student in comb2:
                        rooms[student] = 1
                        used.remove(student)
                    rooms2 = dict(rooms)
                    used2 = set(used)
                    for k in range(1, 10-i-j):
                        for comb3 in itertools.combinations(used, k):
                            for student in comb3:
                                rooms[student] = 2
                                used.remove(student)
                            for student in used:
                                rooms[student] = 3
                            if is_valid_solution(rooms, G, s, numRooms):
                                    temp = calculate_happiness(rooms, G)
                                    if temp > maxHap:
                                        maxHap = temp
                                        maxRooms = rooms
                                        maxNumRooms = numRooms
                            rooms = dict(rooms2)
                            used = set(used2)
                    rooms = dict(rooms1)
                    used = set(used1)
            rooms = {}
            used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}


    # for dict in dicts:
    #     if is_valid_solution(dict[0], G, s, dict[1]):
    #             temp = calculate_happiness(dict[0], G)
    #             if temp > maxHap:
    #                 maxHap = temp
    #                 maxRooms = dict[0]
    #                 maxNumRooms = dict[1]
    # print(maxRooms, maxNumRooms)
    return (maxRooms, maxNumRooms)
    # return (rooms, numRooms)


# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G, s = read_input_file(path)
#     D, k = solve(G, s)
#     assert is_valid_solution(D, G, s, k)
#     print("Total Happiness: {}".format(calculate_happiness(D, G)))
#     write_output_file(D, 'test.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
if __name__ == '__main__':
    inputs = glob.glob('inputs/small/*')
    for input_path in inputs:
        output_path = 'outputs/small/' + os.path.basename(os.path.normpath(input_path))[:-3] + '.out'
        G, s = read_input_file(input_path, 100)
        D, k = solve(G, s)
        assert is_valid_solution(D, G, s, k)
        cost_t = calculate_happiness(D, G)
        print(cost_t)
        write_output_file(D, output_path)
