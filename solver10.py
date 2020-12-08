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
                maxRooms = dict(rooms)
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
                        maxRooms = dict(rooms)
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
                                maxRooms = dict(rooms)
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
                                        maxRooms = dict(rooms)
                                        maxNumRooms = numRooms
                            rooms = dict(rooms2)
                            used = set(used2)
                    rooms = dict(rooms1)
                    used = set(used1)
            rooms = {}
            used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
    if maxHap == 0:
        numRooms = 5
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
                                rooms3 = dict(rooms)
                                used3 = set(used)
                                for l in range(1, 10-i-j-k):
                                    for comb4 in itertools.combinations(used, l):
                                        for student in comb4:
                                            rooms[student] = 3
                                            used.remove(student)
                                        for student in used:
                                            rooms[student] = 4
                                        if is_valid_solution(rooms, G, s, numRooms):
                                                temp = calculate_happiness(rooms, G)
                                                if temp > maxHap:
                                                    maxHap = temp
                                                    maxRooms = dict(rooms)
                                                    maxNumRooms = numRooms
                                        rooms = dict(rooms3)
                                        used = set(used3)
                                rooms = dict(rooms2)
                                used = set(used2)
                        rooms = dict(rooms1)
                        used = set(used1)
                rooms = {}
                used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
    if maxHap == 0:
        numRooms = 6
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
                                rooms3 = dict(rooms)
                                used3 = set(used)
                                for l in range(1, 10-i-j-k):
                                    for comb4 in itertools.combinations(used, l):
                                        for student in comb4:
                                            rooms[student] = 3
                                            used.remove(student)
                                        rooms4 = dict(rooms)
                                        used4 = set(used)
                                        for m in range(1, 10-i-j-k-l):
                                            for comb5 in itertools.combinations(used, m):
                                                for student in comb5:
                                                    rooms[student] = 4
                                                    used.remove(student)
                                                for student in used:
                                                    rooms[student] = 5
                                                if is_valid_solution(rooms, G, s, numRooms):
                                                        temp = calculate_happiness(rooms, G)
                                                        if temp > maxHap:
                                                            maxHap = temp
                                                            maxRooms = dict(rooms)
                                                            maxNumRooms = numRooms
                                                rooms = dict(rooms4)
                                                used = set(used4)
                                        rooms = dict(rooms3)
                                        used = set(used3)
                                rooms = dict(rooms2)
                                used = set(used2)
                        rooms = dict(rooms1)
                        used = set(used1)
                rooms = {}
                used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
    # if maxHap == 0:
    #     numRooms = 7
    #     for i in range(1, 10):
    #         for comb1 in itertools.combinations(used, i):
    #             for student in comb1:
    #                 rooms[student] = 0
    #                 used.remove(student)
    #             rooms1 = dict(rooms)
    #             used1 = set(used)
    #             for j in range(1, 10-i):
    #                 for comb2 in itertools.combinations(used, j):
    #                     for student in comb2:
    #                         rooms[student] = 1
    #                         used.remove(student)
    #                     rooms2 = dict(rooms)
    #                     used2 = set(used)
    #                     for k in range(1, 10-i-j):
    #                         for comb3 in itertools.combinations(used, k):
    #                             for student in comb3:
    #                                 rooms[student] = 2
    #                                 used.remove(student)
    #                             rooms3 = dict(rooms)
    #                             used3 = set(used)
    #                             for l in range(1, 10-i-j-k):
    #                                 for comb4 in itertools.combinations(used, l):
    #                                     for student in comb4:
    #                                         rooms[student] = 3
    #                                         used.remove(student)
    #                                     rooms4 = dict(rooms)
    #                                     used4 = set(used)
    #                                     for m in range(1, 10-i-j-k-l):
    #                                         for comb5 in itertools.combinations(used, m):
    #                                             for student in comb5:
    #                                                 rooms[student] = 4
    #                                                 used.remove(student)
    #                                             rooms5 = dict(rooms)
    #                                             used5 = set(used)
    #                                             for n in range(1, 10-i-j-k-l-m):
    #                                                 for comb6 in itertools.combinations(used, n):
    #                                                     for student in comb6:
    #                                                         rooms[student] = 5
    #                                                         used.remove(student)
    #                                                     for student in used:
    #                                                         rooms[student] = 6
    #                                                     if is_valid_solution(rooms, G, s, numRooms):
    #                                                             temp = calculate_happiness(rooms, G)
    #                                                             if temp > maxHap:
    #                                                                 maxHap = temp
    #                                                                 maxRooms = dict(rooms)
    #                                                                 maxNumRooms = numRooms
    #                                                     rooms = dict(rooms5)
    #                                                     used = set(used5)
    #                                             rooms = dict(rooms4)
    #                                             used = set(used4)
    #                                     rooms = dict(rooms3)
    #                                     used = set(used3)
    #                             rooms = dict(rooms2)
    #                             used = set(used2)
    #                     rooms = dict(rooms1)
    #                     used = set(used1)
    #             rooms = {}
    #             used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}


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

if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    G, s = read_input_file(path)
    D, k = solve(G, s)
    assert is_valid_solution(D, G, s, k)
    print("Total Happiness: {}".format(calculate_happiness(D, G)))
    output_path = 'outputs/small/new/' + os.path.basename(os.path.normpath(path))[:-3] + '.out'
    write_output_file(D, output_path)


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('inputs/small/new/*')
#     for input_path in inputs:
#         if input_path != 'inputs/small/new':
#             output_path = 'outputs/small/' + os.path.basename(os.path.normpath(input_path))[:-3] + '.out'
#             G, s = read_input_file(input_path, 100)
#             D, k = solve(G, s)
#             assert is_valid_solution(D, G, s, k)
#             cost_t = calculate_happiness(D, G)
#             print(input_path, cost_t)
#             write_output_file(D, output_path)
