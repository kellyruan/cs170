import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness, calculate_stress_for_room, calculate_happiness_for_room
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
    used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}
    edgeCount = 0
    maxHap = 0
    maxRooms = {0:0, 1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, 11:11, 12:12, 13:13, 14:14, 15:15, 16:16, 17:17, 18:18, 19:19}
    maxNumRooms = 20
    # for i in G.edges(data=True):
    #     print (i[2])
    edges = list(G.edges(data=True))
    edges.sort(key=lambda x: x[2]["happiness"], reverse=True)
    numRooms = 1
    for student in range(20):
        rooms[student] = 0
    if is_valid_solution(rooms, G, s, numRooms):
            temp = calculate_happiness(rooms, G)
            if temp > maxHap:
                maxHap = temp
                maxRooms = rooms
                maxNumRooms = numRooms
    numRooms = 2
    stresses = s / numRooms
    roomsReverse = {0:[],1:[]}
    while len(used) > 0 and edgeCount < len(edges):
        student1 = edges[edgeCount][0]
        student2 = edges[edgeCount][1]
        if student1 in used and student2 in used:
            temp1 = calculate_happiness_for_room(roomsReverse[0] + [student1, student2], G)
            temp2 = calculate_happiness_for_room(roomsReverse[1] + [student1, student2], G)
            if temp1 > temp2 and calculate_stress_for_room(roomsReverse[0] + [student1, student2], G) <= stresses:
                rooms[student1] = 0
                rooms[student2] = 0
                roomsReverse[0].append(student1)
                roomsReverse[0].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calculate_stress_for_room(roomsReverse[1] + [student1, student2], G) <= stresses:
                rooms[student1] = 1
                rooms[student2] = 1
                roomsReverse[1].append(student1)
                roomsReverse[1].append(student2)
                used.remove(student1)
                used.remove(student2)
        elif student1 in used and student2 not in used:
            if calculate_stress_for_room(roomsReverse[rooms[student2]] + [student1], G) <= stresses:
                rooms[student1] = rooms[student2]
                roomsReverse[rooms[student2]].append(student1)
                used.remove(student1)
        elif student1 not in used and student2 in used:
            if calculate_stress_for_room(roomsReverse[rooms[student1]] + [student2], G) <= stresses:
                rooms[student2] = rooms[student1]
                roomsReverse[rooms[student1]].append(student2)
                used.remove(student2)
        edgeCount += 1
    if is_valid_solution(rooms, G, s, numRooms) and len(used) == 0:
        temp = calculate_happiness(rooms, G)
        if temp > maxHap:
            maxHap = temp
            maxRooms = dict(rooms)
            maxNumRooms = numRooms
    rooms = {}
    used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}
    edgeCount = 0
    numRooms = 3
    stresses = s / numRooms
    roomsReverse = {0:[],1:[],2:[]}
    while len(used) > 0 and edgeCount < len(edges):
        student1 = edges[edgeCount][0]
        student2 = edges[edgeCount][1]
        if student1 in used and student2 in used:
            temp1 = calculate_happiness_for_room(roomsReverse[0] + [student1, student2], G)
            temp2 = calculate_happiness_for_room(roomsReverse[1] + [student1, student2], G)
            temp3 = calculate_happiness_for_room(roomsReverse[2] + [student1, student2], G)
            calcStresses = [temp1, temp2, temp3]
            argCalc = np.argsort(calcStresses)
            if calculate_happiness_for_room(roomsReverse[argCalc[len(argCalc)-1]] + [student1, student2], G) <= stresses:
                rooms[student1] = argCalc[0]
                rooms[student2] = argCalc[0]
                roomsReverse[argCalc[0]].append(student1)
                roomsReverse[argCalc[0]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calculate_happiness_for_room(roomsReverse[argCalc[len(argCalc)-2]] + [student1, student2], G) <= stresses:
                rooms[student1] = argCalc[1]
                rooms[student2] = argCalc[1]
                roomsReverse[argCalc[1]].append(student1)
                roomsReverse[argCalc[1]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calculate_happiness_for_room(roomsReverse[argCalc[len(argCalc)-3]] + [student1, student2], G) <= stresses:
                rooms[student1] = argCalc[2]
                rooms[student2] = argCalc[2]
                roomsReverse[argCalc[2]].append(student1)
                roomsReverse[argCalc[2]].append(student2)
                used.remove(student1)
                used.remove(student2)
        elif student1 in used and student2 not in used:
            if calculate_stress_for_room(roomsReverse[rooms[student2]] + [student1], G) <= stresses:
                rooms[student1] = int(rooms[student2])
                roomsReverse[rooms[student2]].append(student1)
                used.remove(student1)
        elif student1 not in used and student2 in used:
            if calculate_stress_for_room(roomsReverse[rooms[student1]] + [student2], G) <= stresses:
                rooms[student2] = int(rooms[student1])
                roomsReverse[rooms[student1]].append(student2)
                used.remove(student2)
        edgeCount += 1
    if is_valid_solution(rooms, G, s, numRooms) and len(used) == 0:
        temp = calculate_happiness(rooms, G)
        if temp > maxHap:
            maxHap = temp
            maxRooms = dict(rooms)
            maxNumRooms = numRooms
    rooms = {}
    used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}
    edgeCount = 0
    numRooms = 4
    stresses = s / numRooms
    roomsReverse = {0:[],1:[],2:[],3:[]}
    while len(used) > 0 and edgeCount < len(edges):
        student1 = edges[edgeCount][0]
        student2 = edges[edgeCount][1]
        if student1 in used and student2 in used:
            temp1 = calculate_stress_for_room(roomsReverse[0] + [student1, student2], G)
            temp2 = calculate_stress_for_room(roomsReverse[1] + [student1, student2], G)
            temp3 = calculate_stress_for_room(roomsReverse[2] + [student1, student2], G)
            temp4 = calculate_stress_for_room(roomsReverse[3] + [student1, student2], G)
            calcStresses = [temp1, temp2, temp3, temp4]
            argCalc = np.argsort(calcStresses)
            if calcStresses[argCalc[0]] <= stresses:
                rooms[student1] = argCalc[0]
                rooms[student2] = argCalc[0]
                roomsReverse[argCalc[0]].append(student1)
                roomsReverse[argCalc[0]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[1]] <= stresses:
                rooms[student1] = argCalc[1]
                rooms[student2] = argCalc[1]
                roomsReverse[argCalc[1]].append(student1)
                roomsReverse[argCalc[1]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[2]] <= stresses:
                rooms[student1] = argCalc[2]
                rooms[student2] = argCalc[2]
                roomsReverse[argCalc[2]].append(student1)
                roomsReverse[argCalc[2]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[3]] <= stresses:
                rooms[student1] = argCalc[3]
                rooms[student2] = argCalc[3]
                roomsReverse[argCalc[3]].append(student1)
                roomsReverse[argCalc[3]].append(student2)
                used.remove(student1)
                used.remove(student2)
        elif student1 in used and student2 not in used:
            if calculate_stress_for_room(roomsReverse[rooms[student2]] + [student1], G) <= stresses:
                rooms[student1] = int(rooms[student2])
                roomsReverse[rooms[student2]].append(student1)
                used.remove(student1)
        elif student1 not in used and student2 in used:
            if calculate_stress_for_room(roomsReverse[rooms[student1]] + [student2], G) <= stresses:
                rooms[student2] = int(rooms[student1])
                roomsReverse[rooms[student1]].append(student2)
                used.remove(student2)
        edgeCount += 1
    if is_valid_solution(rooms, G, s, numRooms) and len(used) == 0:
        temp = calculate_happiness(rooms, G)
        if temp > maxHap:
            maxHap = temp
            maxRooms = dict(rooms)
            maxNumRooms = numRooms
    rooms = {}
    used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}
    edgeCount = 0
    numRooms = 5
    stresses = s / numRooms
    roomsReverse = {0:[],1:[],2:[],3:[],4:[]}
    while len(used) > 0 and edgeCount < len(edges):
        student1 = edges[edgeCount][0]
        student2 = edges[edgeCount][1]
        if student1 in used and student2 in used:
            temp1 = calculate_stress_for_room(roomsReverse[0] + [student1, student2], G)
            temp2 = calculate_stress_for_room(roomsReverse[1] + [student1, student2], G)
            temp3 = calculate_stress_for_room(roomsReverse[2] + [student1, student2], G)
            temp4 = calculate_stress_for_room(roomsReverse[3] + [student1, student2], G)
            temp5 = calculate_stress_for_room(roomsReverse[4] + [student1, student2], G)
            calcStresses = [temp1, temp2, temp3, temp4, temp5]
            argCalc = np.argsort(calcStresses)
            if calcStresses[argCalc[0]] <= stresses:
                rooms[student1] = argCalc[0]
                rooms[student2] = argCalc[0]
                roomsReverse[argCalc[0]].append(student1)
                roomsReverse[argCalc[0]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[1]] <= stresses:
                rooms[student1] = argCalc[1]
                rooms[student2] = argCalc[1]
                roomsReverse[argCalc[1]].append(student1)
                roomsReverse[argCalc[1]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[2]] <= stresses:
                rooms[student1] = argCalc[2]
                rooms[student2] = argCalc[2]
                roomsReverse[argCalc[2]].append(student1)
                roomsReverse[argCalc[2]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[3]] <= stresses:
                rooms[student1] = argCalc[3]
                rooms[student2] = argCalc[3]
                roomsReverse[argCalc[3]].append(student1)
                roomsReverse[argCalc[3]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[4]] <= stresses:
                rooms[student1] = argCalc[4]
                rooms[student2] = argCalc[4]
                roomsReverse[argCalc[4]].append(student1)
                roomsReverse[argCalc[4]].append(student2)
                used.remove(student1)
                used.remove(student2)
        elif student1 in used and student2 not in used:
            if calculate_stress_for_room(roomsReverse[rooms[student2]] + [student1], G) <= stresses:
                rooms[student1] = int(rooms[student2])
                roomsReverse[rooms[student2]].append(student1)
                used.remove(student1)
        elif student1 not in used and student2 in used:
            if calculate_stress_for_room(roomsReverse[rooms[student1]] + [student2], G) <= stresses:
                rooms[student2] = int(rooms[student1])
                roomsReverse[rooms[student1]].append(student2)
                used.remove(student2)
        edgeCount += 1
    if is_valid_solution(rooms, G, s, numRooms) and len(used) == 0:
        temp = calculate_happiness(rooms, G)
        if temp > maxHap:
            maxHap = temp
            maxRooms = dict(rooms)
            maxNumRooms = numRooms
    rooms = {}
    used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}
    edgeCount = 0
    numRooms = 6
    stresses = s / numRooms
    roomsReverse = {0:[],1:[],2:[],3:[],4:[],5:[]}
    while len(used) > 0 and edgeCount < len(edges):
        student1 = edges[edgeCount][0]
        student2 = edges[edgeCount][1]
        if student1 in used and student2 in used:
            temp1 = calculate_stress_for_room(roomsReverse[0] + [student1, student2], G)
            temp2 = calculate_stress_for_room(roomsReverse[1] + [student1, student2], G)
            temp3 = calculate_stress_for_room(roomsReverse[2] + [student1, student2], G)
            temp4 = calculate_stress_for_room(roomsReverse[3] + [student1, student2], G)
            temp5 = calculate_stress_for_room(roomsReverse[4] + [student1, student2], G)
            temp6 = calculate_stress_for_room(roomsReverse[5] + [student1, student2], G)
            calcStresses = [temp1, temp2, temp3, temp4, temp5, temp6]
            argCalc = np.argsort(calcStresses)
            if calcStresses[argCalc[0]] <= stresses:
                rooms[student1] = argCalc[0]
                rooms[student2] = argCalc[0]
                roomsReverse[argCalc[0]].append(student1)
                roomsReverse[argCalc[0]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[1]] <= stresses:
                rooms[student1] = argCalc[1]
                rooms[student2] = argCalc[1]
                roomsReverse[argCalc[1]].append(student1)
                roomsReverse[argCalc[1]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[2]] <= stresses:
                rooms[student1] = argCalc[2]
                rooms[student2] = argCalc[2]
                roomsReverse[argCalc[2]].append(student1)
                roomsReverse[argCalc[2]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[3]] <= stresses:
                rooms[student1] = argCalc[3]
                rooms[student2] = argCalc[3]
                roomsReverse[argCalc[3]].append(student1)
                roomsReverse[argCalc[3]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[4]] <= stresses:
                rooms[student1] = argCalc[4]
                rooms[student2] = argCalc[4]
                roomsReverse[argCalc[4]].append(student1)
                roomsReverse[argCalc[4]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[5]] <= stresses:
                rooms[student1] = argCalc[5]
                rooms[student2] = argCalc[5]
                roomsReverse[argCalc[5]].append(student1)
                roomsReverse[argCalc[5]].append(student2)
                used.remove(student1)
                used.remove(student2)
        elif student1 in used and student2 not in used:
            if calculate_stress_for_room(roomsReverse[rooms[student2]] + [student1], G) <= stresses:
                rooms[student1] = int(rooms[student2])
                roomsReverse[rooms[student2]].append(student1)
                used.remove(student1)
        elif student1 not in used and student2 in used:
            if calculate_stress_for_room(roomsReverse[rooms[student1]] + [student2], G) <= stresses:
                rooms[student2] = int(rooms[student1])
                roomsReverse[rooms[student1]].append(student2)
                used.remove(student2)
        edgeCount += 1
    if is_valid_solution(rooms, G, s, numRooms) and len(used) == 0:
        temp = calculate_happiness(rooms, G)
        if temp > maxHap:
            maxHap = temp
            maxRooms = dict(rooms)
            maxNumRooms = numRooms
    rooms = {}
    used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}
    edgeCount = 0
    numRooms = 7
    stresses = s / numRooms
    roomsReverse = {0:[],1:[],2:[],3:[],4:[],5:[],6:[]}
    while len(used) > 0 and edgeCount < len(edges):
        student1 = edges[edgeCount][0]
        student2 = edges[edgeCount][1]
        if student1 in used and student2 in used:
            temp1 = calculate_stress_for_room(roomsReverse[0] + [student1, student2], G)
            temp2 = calculate_stress_for_room(roomsReverse[1] + [student1, student2], G)
            temp3 = calculate_stress_for_room(roomsReverse[2] + [student1, student2], G)
            temp4 = calculate_stress_for_room(roomsReverse[3] + [student1, student2], G)
            temp5 = calculate_stress_for_room(roomsReverse[4] + [student1, student2], G)
            temp6 = calculate_stress_for_room(roomsReverse[5] + [student1, student2], G)
            temp7 = calculate_stress_for_room(roomsReverse[6] + [student1, student2], G)
            calcStresses = [temp1, temp2, temp3, temp4, temp5, temp6, temp7]
            argCalc = np.argsort(calcStresses)
            if calcStresses[argCalc[0]] <= stresses:
                rooms[student1] = argCalc[0]
                rooms[student2] = argCalc[0]
                roomsReverse[argCalc[0]].append(student1)
                roomsReverse[argCalc[0]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[1]] <= stresses:
                rooms[student1] = argCalc[1]
                rooms[student2] = argCalc[1]
                roomsReverse[argCalc[1]].append(student1)
                roomsReverse[argCalc[1]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[2]] <= stresses:
                rooms[student1] = argCalc[2]
                rooms[student2] = argCalc[2]
                roomsReverse[argCalc[2]].append(student1)
                roomsReverse[argCalc[2]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[3]] <= stresses:
                rooms[student1] = argCalc[3]
                rooms[student2] = argCalc[3]
                roomsReverse[argCalc[3]].append(student1)
                roomsReverse[argCalc[3]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[4]] <= stresses:
                rooms[student1] = argCalc[4]
                rooms[student2] = argCalc[4]
                roomsReverse[argCalc[4]].append(student1)
                roomsReverse[argCalc[4]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[5]] <= stresses:
                rooms[student1] = argCalc[5]
                rooms[student2] = argCalc[5]
                roomsReverse[argCalc[5]].append(student1)
                roomsReverse[argCalc[5]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[6]] <= stresses:
                rooms[student1] = argCalc[6]
                rooms[student2] = argCalc[6]
                roomsReverse[argCalc[6]].append(student1)
                roomsReverse[argCalc[6]].append(student2)
                used.remove(student1)
                used.remove(student2)
        elif student1 in used and student2 not in used:
            if calculate_stress_for_room(roomsReverse[rooms[student2]] + [student1], G) <= stresses:
                rooms[student1] = int(rooms[student2])
                roomsReverse[rooms[student2]].append(student1)
                used.remove(student1)
        elif student1 not in used and student2 in used:
            if calculate_stress_for_room(roomsReverse[rooms[student1]] + [student2], G) <= stresses:
                rooms[student2] = int(rooms[student1])
                roomsReverse[rooms[student1]].append(student2)
                used.remove(student2)
        edgeCount += 1
    if is_valid_solution(rooms, G, s, numRooms) and len(used) == 0:
        temp = calculate_happiness(rooms, G)
        if temp > maxHap:
            maxHap = temp
            maxRooms = dict(rooms)
            maxNumRooms = numRooms
    rooms = {}
    used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}
    edgeCount = 0
    numRooms = 8
    stresses = s / numRooms
    roomsReverse = {0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[]}
    while len(used) > 0 and edgeCount < len(edges):
        student1 = edges[edgeCount][0]
        student2 = edges[edgeCount][1]
        if student1 in used and student2 in used:
            temp1 = calculate_stress_for_room(roomsReverse[0] + [student1, student2], G)
            temp2 = calculate_stress_for_room(roomsReverse[1] + [student1, student2], G)
            temp3 = calculate_stress_for_room(roomsReverse[2] + [student1, student2], G)
            temp4 = calculate_stress_for_room(roomsReverse[3] + [student1, student2], G)
            temp5 = calculate_stress_for_room(roomsReverse[4] + [student1, student2], G)
            temp6 = calculate_stress_for_room(roomsReverse[5] + [student1, student2], G)
            temp7 = calculate_stress_for_room(roomsReverse[6] + [student1, student2], G)
            temp8 = calculate_stress_for_room(roomsReverse[7] + [student1, student2], G)
            calcStresses = [temp1, temp2, temp3, temp4, temp5, temp6, temp7, temp8]
            argCalc = np.argsort(calcStresses)
            if calcStresses[argCalc[0]] <= stresses:
                rooms[student1] = argCalc[0]
                rooms[student2] = argCalc[0]
                roomsReverse[argCalc[0]].append(student1)
                roomsReverse[argCalc[0]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[1]] <= stresses:
                rooms[student1] = argCalc[1]
                rooms[student2] = argCalc[1]
                roomsReverse[argCalc[1]].append(student1)
                roomsReverse[argCalc[1]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[2]] <= stresses:
                rooms[student1] = argCalc[2]
                rooms[student2] = argCalc[2]
                roomsReverse[argCalc[2]].append(student1)
                roomsReverse[argCalc[2]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[3]] <= stresses:
                rooms[student1] = argCalc[3]
                rooms[student2] = argCalc[3]
                roomsReverse[argCalc[3]].append(student1)
                roomsReverse[argCalc[3]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[4]] <= stresses:
                rooms[student1] = argCalc[4]
                rooms[student2] = argCalc[4]
                roomsReverse[argCalc[4]].append(student1)
                roomsReverse[argCalc[4]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[5]] <= stresses:
                rooms[student1] = argCalc[5]
                rooms[student2] = argCalc[5]
                roomsReverse[argCalc[5]].append(student1)
                roomsReverse[argCalc[5]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[6]] <= stresses:
                rooms[student1] = argCalc[6]
                rooms[student2] = argCalc[6]
                roomsReverse[argCalc[6]].append(student1)
                roomsReverse[argCalc[6]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[7]] <= stresses:
                rooms[student1] = argCalc[7]
                rooms[student2] = argCalc[7]
                roomsReverse[argCalc[7]].append(student1)
                roomsReverse[argCalc[7]].append(student2)
                used.remove(student1)
                used.remove(student2)
        elif student1 in used and student2 not in used:
            if calculate_stress_for_room(roomsReverse[rooms[student2]] + [student1], G) <= stresses:
                rooms[student1] = int(rooms[student2])
                roomsReverse[rooms[student2]].append(student1)
                used.remove(student1)
        elif student1 not in used and student2 in used:
            if calculate_stress_for_room(roomsReverse[rooms[student1]] + [student2], G) <= stresses:
                rooms[student2] = int(rooms[student1])
                roomsReverse[rooms[student1]].append(student2)
                used.remove(student2)
        edgeCount += 1
    if is_valid_solution(rooms, G, s, numRooms) and len(used) == 0:
        temp = calculate_happiness(rooms, G)
        if temp > maxHap:
            maxHap = temp
            maxRooms = dict(rooms)
            maxNumRooms = numRooms
    rooms = {}
    used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}
    edgeCount = 0
    numRooms = 9
    stresses = s / numRooms
    roomsReverse = {0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[]}
    while len(used) > 0 and edgeCount < len(edges):
        student1 = edges[edgeCount][0]
        student2 = edges[edgeCount][1]
        if student1 in used and student2 in used:
            temp1 = calculate_stress_for_room(roomsReverse[0] + [student1, student2], G)
            temp2 = calculate_stress_for_room(roomsReverse[1] + [student1, student2], G)
            temp3 = calculate_stress_for_room(roomsReverse[2] + [student1, student2], G)
            temp4 = calculate_stress_for_room(roomsReverse[3] + [student1, student2], G)
            temp5 = calculate_stress_for_room(roomsReverse[4] + [student1, student2], G)
            temp6 = calculate_stress_for_room(roomsReverse[5] + [student1, student2], G)
            temp7 = calculate_stress_for_room(roomsReverse[6] + [student1, student2], G)
            temp8 = calculate_stress_for_room(roomsReverse[7] + [student1, student2], G)
            temp9 = calculate_stress_for_room(roomsReverse[8] + [student1, student2], G)
            calcStresses = [temp1, temp2, temp3, temp4, temp5, temp6, temp7, temp8, temp9]
            argCalc = np.argsort(calcStresses)
            if calcStresses[argCalc[0]] <= stresses:
                rooms[student1] = argCalc[0]
                rooms[student2] = argCalc[0]
                roomsReverse[argCalc[0]].append(student1)
                roomsReverse[argCalc[0]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[1]] <= stresses:
                rooms[student1] = argCalc[1]
                rooms[student2] = argCalc[1]
                roomsReverse[argCalc[1]].append(student1)
                roomsReverse[argCalc[1]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[2]] <= stresses:
                rooms[student1] = argCalc[2]
                rooms[student2] = argCalc[2]
                roomsReverse[argCalc[2]].append(student1)
                roomsReverse[argCalc[2]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[3]] <= stresses:
                rooms[student1] = argCalc[3]
                rooms[student2] = argCalc[3]
                roomsReverse[argCalc[3]].append(student1)
                roomsReverse[argCalc[3]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[4]] <= stresses:
                rooms[student1] = argCalc[4]
                rooms[student2] = argCalc[4]
                roomsReverse[argCalc[4]].append(student1)
                roomsReverse[argCalc[4]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[5]] <= stresses:
                rooms[student1] = argCalc[5]
                rooms[student2] = argCalc[5]
                roomsReverse[argCalc[5]].append(student1)
                roomsReverse[argCalc[5]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[6]] <= stresses:
                rooms[student1] = argCalc[6]
                rooms[student2] = argCalc[6]
                roomsReverse[argCalc[6]].append(student1)
                roomsReverse[argCalc[6]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[7]] <= stresses:
                rooms[student1] = argCalc[7]
                rooms[student2] = argCalc[7]
                roomsReverse[argCalc[7]].append(student1)
                roomsReverse[argCalc[7]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[8]] <= stresses:
                rooms[student1] = argCalc[8]
                rooms[student2] = argCalc[8]
                roomsReverse[argCalc[8]].append(student1)
                roomsReverse[argCalc[8]].append(student2)
                used.remove(student1)
                used.remove(student2)
        elif student1 in used and student2 not in used:
            if calculate_stress_for_room(roomsReverse[rooms[student2]] + [student1], G) <= stresses:
                rooms[student1] = int(rooms[student2])
                roomsReverse[rooms[student2]].append(student1)
                used.remove(student1)
        elif student1 not in used and student2 in used:
            if calculate_stress_for_room(roomsReverse[rooms[student1]] + [student2], G) <= stresses:
                rooms[student2] = int(rooms[student1])
                roomsReverse[rooms[student1]].append(student2)
                used.remove(student2)
        edgeCount += 1
    if is_valid_solution(rooms, G, s, numRooms) and len(used) == 0:
        temp = calculate_happiness(rooms, G)
        if temp > maxHap:
            maxHap = temp
            maxRooms = dict(rooms)
            maxNumRooms = numRooms
    rooms = {}
    used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}
    edgeCount = 0
    numRooms = 10
    stresses = s / numRooms
    roomsReverse = {0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[]}
    while len(used) > 0 and edgeCount < len(edges):
        student1 = edges[edgeCount][0]
        student2 = edges[edgeCount][1]
        if student1 in used and student2 in used:
            temp1 = calculate_stress_for_room(roomsReverse[0] + [student1, student2], G)
            temp2 = calculate_stress_for_room(roomsReverse[1] + [student1, student2], G)
            temp3 = calculate_stress_for_room(roomsReverse[2] + [student1, student2], G)
            temp4 = calculate_stress_for_room(roomsReverse[3] + [student1, student2], G)
            temp5 = calculate_stress_for_room(roomsReverse[4] + [student1, student2], G)
            temp6 = calculate_stress_for_room(roomsReverse[5] + [student1, student2], G)
            temp7 = calculate_stress_for_room(roomsReverse[6] + [student1, student2], G)
            temp8 = calculate_stress_for_room(roomsReverse[7] + [student1, student2], G)
            temp9 = calculate_stress_for_room(roomsReverse[8] + [student1, student2], G)
            temp10 = calculate_stress_for_room(roomsReverse[9] + [student1, student2], G)
            calcStresses = [temp1, temp2, temp3, temp4, temp5, temp6, temp7, temp8, temp9, temp10]
            argCalc = np.argsort(calcStresses)
            if calcStresses[argCalc[0]] <= stresses:
                rooms[student1] = argCalc[0]
                rooms[student2] = argCalc[0]
                roomsReverse[argCalc[0]].append(student1)
                roomsReverse[argCalc[0]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[1]] <= stresses:
                rooms[student1] = argCalc[1]
                rooms[student2] = argCalc[1]
                roomsReverse[argCalc[1]].append(student1)
                roomsReverse[argCalc[1]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[2]] <= stresses:
                rooms[student1] = argCalc[2]
                rooms[student2] = argCalc[2]
                roomsReverse[argCalc[2]].append(student1)
                roomsReverse[argCalc[2]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[3]] <= stresses:
                rooms[student1] = argCalc[3]
                rooms[student2] = argCalc[3]
                roomsReverse[argCalc[3]].append(student1)
                roomsReverse[argCalc[3]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[4]] <= stresses:
                rooms[student1] = argCalc[4]
                rooms[student2] = argCalc[4]
                roomsReverse[argCalc[4]].append(student1)
                roomsReverse[argCalc[4]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[5]] <= stresses:
                rooms[student1] = argCalc[5]
                rooms[student2] = argCalc[5]
                roomsReverse[argCalc[5]].append(student1)
                roomsReverse[argCalc[5]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[6]] <= stresses:
                rooms[student1] = argCalc[6]
                rooms[student2] = argCalc[6]
                roomsReverse[argCalc[6]].append(student1)
                roomsReverse[argCalc[6]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[7]] <= stresses:
                rooms[student1] = argCalc[7]
                rooms[student2] = argCalc[7]
                roomsReverse[argCalc[7]].append(student1)
                roomsReverse[argCalc[7]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[8]] <= stresses:
                rooms[student1] = argCalc[8]
                rooms[student2] = argCalc[8]
                roomsReverse[argCalc[8]].append(student1)
                roomsReverse[argCalc[8]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[9]] <= stresses:
                rooms[student1] = argCalc[9]
                rooms[student2] = argCalc[9]
                roomsReverse[argCalc[9]].append(student1)
                roomsReverse[argCalc[9]].append(student2)
                used.remove(student1)
                used.remove(student2)
        elif student1 in used and student2 not in used:
            if calculate_stress_for_room(roomsReverse[rooms[student2]] + [student1], G) <= stresses:
                rooms[student1] = int(rooms[student2])
                roomsReverse[rooms[student2]].append(student1)
                used.remove(student1)
        elif student1 not in used and student2 in used:
            if calculate_stress_for_room(roomsReverse[rooms[student1]] + [student2], G) <= stresses:
                rooms[student2] = int(rooms[student1])
                roomsReverse[rooms[student1]].append(student2)
                used.remove(student2)
        edgeCount += 1
    if is_valid_solution(rooms, G, s, numRooms) and len(used) == 0:
        temp = calculate_happiness(rooms, G)
        if temp > maxHap:
            maxHap = temp
            maxRooms = dict(rooms)
            maxNumRooms = numRooms
    rooms = {}
    used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}
    edgeCount = 0
    numRooms = 11
    stresses = s / numRooms
    roomsReverse = {0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[]}
    while len(used) > 0 and edgeCount < len(edges):
        student1 = edges[edgeCount][0]
        student2 = edges[edgeCount][1]
        if student1 in used and student2 in used:
            temp1 = calculate_stress_for_room(roomsReverse[0] + [student1, student2], G)
            temp2 = calculate_stress_for_room(roomsReverse[1] + [student1, student2], G)
            temp3 = calculate_stress_for_room(roomsReverse[2] + [student1, student2], G)
            temp4 = calculate_stress_for_room(roomsReverse[3] + [student1, student2], G)
            temp5 = calculate_stress_for_room(roomsReverse[4] + [student1, student2], G)
            temp6 = calculate_stress_for_room(roomsReverse[5] + [student1, student2], G)
            temp7 = calculate_stress_for_room(roomsReverse[6] + [student1, student2], G)
            temp8 = calculate_stress_for_room(roomsReverse[7] + [student1, student2], G)
            temp9 = calculate_stress_for_room(roomsReverse[8] + [student1, student2], G)
            temp10 = calculate_stress_for_room(roomsReverse[9] + [student1, student2], G)
            temp11 = calculate_stress_for_room(roomsReverse[10] + [student1, student2], G)
            calcStresses = [temp1, temp2, temp3, temp4, temp5, temp6, temp7, temp8, temp9, temp10, temp11]
            argCalc = np.argsort(calcStresses)
            if calcStresses[argCalc[0]] <= stresses:
                rooms[student1] = argCalc[0]
                rooms[student2] = argCalc[0]
                roomsReverse[argCalc[0]].append(student1)
                roomsReverse[argCalc[0]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[1]] <= stresses:
                rooms[student1] = argCalc[1]
                rooms[student2] = argCalc[1]
                roomsReverse[argCalc[1]].append(student1)
                roomsReverse[argCalc[1]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[2]] <= stresses:
                rooms[student1] = argCalc[2]
                rooms[student2] = argCalc[2]
                roomsReverse[argCalc[2]].append(student1)
                roomsReverse[argCalc[2]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[3]] <= stresses:
                rooms[student1] = argCalc[3]
                rooms[student2] = argCalc[3]
                roomsReverse[argCalc[3]].append(student1)
                roomsReverse[argCalc[3]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[4]] <= stresses:
                rooms[student1] = argCalc[4]
                rooms[student2] = argCalc[4]
                roomsReverse[argCalc[4]].append(student1)
                roomsReverse[argCalc[4]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[5]] <= stresses:
                rooms[student1] = argCalc[5]
                rooms[student2] = argCalc[5]
                roomsReverse[argCalc[5]].append(student1)
                roomsReverse[argCalc[5]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[6]] <= stresses:
                rooms[student1] = argCalc[6]
                rooms[student2] = argCalc[6]
                roomsReverse[argCalc[6]].append(student1)
                roomsReverse[argCalc[6]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[7]] <= stresses:
                rooms[student1] = argCalc[7]
                rooms[student2] = argCalc[7]
                roomsReverse[argCalc[7]].append(student1)
                roomsReverse[argCalc[7]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[8]] <= stresses:
                rooms[student1] = argCalc[8]
                rooms[student2] = argCalc[8]
                roomsReverse[argCalc[8]].append(student1)
                roomsReverse[argCalc[8]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[9]] <= stresses:
                rooms[student1] = argCalc[9]
                rooms[student2] = argCalc[9]
                roomsReverse[argCalc[9]].append(student1)
                roomsReverse[argCalc[9]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[10]] <= stresses:
                rooms[student1] = argCalc[10]
                rooms[student2] = argCalc[10]
                roomsReverse[argCalc[10]].append(student1)
                roomsReverse[argCalc[10]].append(student2)
                used.remove(student1)
                used.remove(student2)
        elif student1 in used and student2 not in used:
            if calculate_stress_for_room(roomsReverse[rooms[student2]] + [student1], G) <= stresses:
                rooms[student1] = int(rooms[student2])
                roomsReverse[rooms[student2]].append(student1)
                used.remove(student1)
        elif student1 not in used and student2 in used:
            if calculate_stress_for_room(roomsReverse[rooms[student1]] + [student2], G) <= stresses:
                rooms[student2] = int(rooms[student1])
                roomsReverse[rooms[student1]].append(student2)
                used.remove(student2)
        edgeCount += 1
    if is_valid_solution(rooms, G, s, numRooms) and len(used) == 0:
        temp = calculate_happiness(rooms, G)
        if temp > maxHap:
            maxHap = temp
            maxRooms = dict(rooms)
            maxNumRooms = numRooms
    rooms = {}
    used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}
    edgeCount = 0
    numRooms = 12
    stresses = s / numRooms
    roomsReverse = {0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[],11:[]}
    while len(used) > 0 and edgeCount < len(edges):
        student1 = edges[edgeCount][0]
        student2 = edges[edgeCount][1]
        if student1 in used and student2 in used:
            temp1 = calculate_stress_for_room(roomsReverse[0] + [student1, student2], G)
            temp2 = calculate_stress_for_room(roomsReverse[1] + [student1, student2], G)
            temp3 = calculate_stress_for_room(roomsReverse[2] + [student1, student2], G)
            temp4 = calculate_stress_for_room(roomsReverse[3] + [student1, student2], G)
            temp5 = calculate_stress_for_room(roomsReverse[4] + [student1, student2], G)
            temp6 = calculate_stress_for_room(roomsReverse[5] + [student1, student2], G)
            temp7 = calculate_stress_for_room(roomsReverse[6] + [student1, student2], G)
            temp8 = calculate_stress_for_room(roomsReverse[7] + [student1, student2], G)
            temp9 = calculate_stress_for_room(roomsReverse[8] + [student1, student2], G)
            temp10 = calculate_stress_for_room(roomsReverse[9] + [student1, student2], G)
            temp11 = calculate_stress_for_room(roomsReverse[10] + [student1, student2], G)
            temp12 = calculate_stress_for_room(roomsReverse[11] + [student1, student2], G)
            calcStresses = [temp1, temp2, temp3, temp4, temp5, temp6, temp7, temp8, temp9, temp10, temp11, temp12]
            argCalc = np.argsort(calcStresses)
            if calcStresses[argCalc[0]] <= stresses:
                rooms[student1] = argCalc[0]
                rooms[student2] = argCalc[0]
                roomsReverse[argCalc[0]].append(student1)
                roomsReverse[argCalc[0]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[1]] <= stresses:
                rooms[student1] = argCalc[1]
                rooms[student2] = argCalc[1]
                roomsReverse[argCalc[1]].append(student1)
                roomsReverse[argCalc[1]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[2]] <= stresses:
                rooms[student1] = argCalc[2]
                rooms[student2] = argCalc[2]
                roomsReverse[argCalc[2]].append(student1)
                roomsReverse[argCalc[2]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[3]] <= stresses:
                rooms[student1] = argCalc[3]
                rooms[student2] = argCalc[3]
                roomsReverse[argCalc[3]].append(student1)
                roomsReverse[argCalc[3]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[4]] <= stresses:
                rooms[student1] = argCalc[4]
                rooms[student2] = argCalc[4]
                roomsReverse[argCalc[4]].append(student1)
                roomsReverse[argCalc[4]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[5]] <= stresses:
                rooms[student1] = argCalc[5]
                rooms[student2] = argCalc[5]
                roomsReverse[argCalc[5]].append(student1)
                roomsReverse[argCalc[5]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[6]] <= stresses:
                rooms[student1] = argCalc[6]
                rooms[student2] = argCalc[6]
                roomsReverse[argCalc[6]].append(student1)
                roomsReverse[argCalc[6]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[7]] <= stresses:
                rooms[student1] = argCalc[7]
                rooms[student2] = argCalc[7]
                roomsReverse[argCalc[7]].append(student1)
                roomsReverse[argCalc[7]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[8]] <= stresses:
                rooms[student1] = argCalc[8]
                rooms[student2] = argCalc[8]
                roomsReverse[argCalc[8]].append(student1)
                roomsReverse[argCalc[8]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[9]] <= stresses:
                rooms[student1] = argCalc[9]
                rooms[student2] = argCalc[9]
                roomsReverse[argCalc[9]].append(student1)
                roomsReverse[argCalc[9]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[10]] <= stresses:
                rooms[student1] = argCalc[10]
                rooms[student2] = argCalc[10]
                roomsReverse[argCalc[10]].append(student1)
                roomsReverse[argCalc[10]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[11]] <= stresses:
                rooms[student1] = argCalc[11]
                rooms[student2] = argCalc[11]
                roomsReverse[argCalc[11]].append(student1)
                roomsReverse[argCalc[11]].append(student2)
                used.remove(student1)
                used.remove(student2)
        elif student1 in used and student2 not in used:
            if calculate_stress_for_room(roomsReverse[rooms[student2]] + [student1], G) <= stresses:
                rooms[student1] = int(rooms[student2])
                roomsReverse[rooms[student2]].append(student1)
                used.remove(student1)
        elif student1 not in used and student2 in used:
            if calculate_stress_for_room(roomsReverse[rooms[student1]] + [student2], G) <= stresses:
                rooms[student2] = int(rooms[student1])
                roomsReverse[rooms[student1]].append(student2)
                used.remove(student2)
        edgeCount += 1
    if is_valid_solution(rooms, G, s, numRooms) and len(used) == 0:
        temp = calculate_happiness(rooms, G)
        if temp > maxHap:
            maxHap = temp
            maxRooms = dict(rooms)
            maxNumRooms = numRooms
    rooms = {}
    used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}
    edgeCount = 0

    edges = list(G.edges(data=True))
    edges.sort(key=lambda x: x[2]["stress"])
    numRooms = 2
    stresses = s / numRooms
    roomsReverse = {0:[],1:[]}
    while len(used) > 0 and edgeCount < len(edges):
        student1 = edges[edgeCount][0]
        student2 = edges[edgeCount][1]
        if student1 in used and student2 in used:
            temp1 = calculate_stress_for_room(roomsReverse[0] + [student1, student2], G)
            temp2 = calculate_stress_for_room(roomsReverse[1] + [student1, student2], G)
            if temp1 < temp2 and temp1 <= stresses:
                rooms[student1] = 0
                rooms[student2] = 0
                roomsReverse[0].append(student1)
                roomsReverse[0].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif temp2 <= stresses:
                rooms[student1] = 1
                rooms[student2] = 1
                roomsReverse[1].append(student1)
                roomsReverse[1].append(student2)
                used.remove(student1)
                used.remove(student2)
        elif student1 in used and student2 not in used:
            if calculate_stress_for_room(roomsReverse[rooms[student2]] + [student1], G) <= stresses:
                rooms[student1] = rooms[student2]
                roomsReverse[rooms[student2]].append(student1)
                used.remove(student1)
        elif student1 not in used and student2 in used:
            if calculate_stress_for_room(roomsReverse[rooms[student1]] + [student2], G) <= stresses:
                rooms[student2] = rooms[student1]
                roomsReverse[rooms[student1]].append(student2)
                used.remove(student2)
        edgeCount += 1
    if is_valid_solution(rooms, G, s, numRooms) and len(used) == 0:
        temp = calculate_happiness(rooms, G)
        if temp > maxHap:
            maxHap = temp
            maxRooms = dict(rooms)
            maxNumRooms = numRooms
    rooms = {}
    used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}
    edgeCount = 0
    numRooms = 3
    stresses = s / numRooms
    roomsReverse = {0:[],1:[],2:[]}
    while len(used) > 0 and edgeCount < len(edges):
        student1 = edges[edgeCount][0]
        student2 = edges[edgeCount][1]
        if student1 in used and student2 in used:
            temp1 = calculate_stress_for_room(roomsReverse[0] + [student1, student2], G)
            temp2 = calculate_stress_for_room(roomsReverse[1] + [student1, student2], G)
            temp3 = calculate_stress_for_room(roomsReverse[2] + [student1, student2], G)
            calcStresses = [temp1, temp2, temp3]
            argCalc = np.argsort(calcStresses)
            if calcStresses[argCalc[0]] <= stresses:
                rooms[student1] = argCalc[0]
                rooms[student2] = argCalc[0]
                roomsReverse[argCalc[0]].append(student1)
                roomsReverse[argCalc[0]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[1]] <= stresses:
                rooms[student1] = argCalc[1]
                rooms[student2] = argCalc[1]
                roomsReverse[argCalc[1]].append(student1)
                roomsReverse[argCalc[1]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[2]] <= stresses:
                rooms[student1] = argCalc[2]
                rooms[student2] = argCalc[2]
                roomsReverse[argCalc[2]].append(student1)
                roomsReverse[argCalc[2]].append(student2)
                used.remove(student1)
                used.remove(student2)
        elif student1 in used and student2 not in used:
            if calculate_stress_for_room(roomsReverse[rooms[student2]] + [student1], G) <= stresses:
                rooms[student1] = int(rooms[student2])
                roomsReverse[rooms[student2]].append(student1)
                used.remove(student1)
        elif student1 not in used and student2 in used:
            if calculate_stress_for_room(roomsReverse[rooms[student1]] + [student2], G) <= stresses:
                rooms[student2] = int(rooms[student1])
                roomsReverse[rooms[student1]].append(student2)
                used.remove(student2)
        edgeCount += 1
    if is_valid_solution(rooms, G, s, numRooms) and len(used) == 0:
        temp = calculate_happiness(rooms, G)
        if temp > maxHap:
            maxHap = temp
            maxRooms = dict(rooms)
            maxNumRooms = numRooms
    rooms = {}
    used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}
    edgeCount = 0
    numRooms = 4
    stresses = s / numRooms
    roomsReverse = {0:[],1:[],2:[],3:[]}
    while len(used) > 0 and edgeCount < len(edges):
        student1 = edges[edgeCount][0]
        student2 = edges[edgeCount][1]
        if student1 in used and student2 in used:
            temp1 = calculate_stress_for_room(roomsReverse[0] + [student1, student2], G)
            temp2 = calculate_stress_for_room(roomsReverse[1] + [student1, student2], G)
            temp3 = calculate_stress_for_room(roomsReverse[2] + [student1, student2], G)
            temp4 = calculate_stress_for_room(roomsReverse[3] + [student1, student2], G)
            calcStresses = [temp1, temp2, temp3, temp4]
            argCalc = np.argsort(calcStresses)
            if calcStresses[argCalc[0]] <= stresses:
                rooms[student1] = argCalc[0]
                rooms[student2] = argCalc[0]
                roomsReverse[argCalc[0]].append(student1)
                roomsReverse[argCalc[0]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[1]] <= stresses:
                rooms[student1] = argCalc[1]
                rooms[student2] = argCalc[1]
                roomsReverse[argCalc[1]].append(student1)
                roomsReverse[argCalc[1]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[2]] <= stresses:
                rooms[student1] = argCalc[2]
                rooms[student2] = argCalc[2]
                roomsReverse[argCalc[2]].append(student1)
                roomsReverse[argCalc[2]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[3]] <= stresses:
                rooms[student1] = argCalc[3]
                rooms[student2] = argCalc[3]
                roomsReverse[argCalc[3]].append(student1)
                roomsReverse[argCalc[3]].append(student2)
                used.remove(student1)
                used.remove(student2)
        elif student1 in used and student2 not in used:
            if calculate_stress_for_room(roomsReverse[rooms[student2]] + [student1], G) <= stresses:
                rooms[student1] = int(rooms[student2])
                roomsReverse[rooms[student2]].append(student1)
                used.remove(student1)
        elif student1 not in used and student2 in used:
            if calculate_stress_for_room(roomsReverse[rooms[student1]] + [student2], G) <= stresses:
                rooms[student2] = int(rooms[student1])
                roomsReverse[rooms[student1]].append(student2)
                used.remove(student2)
        edgeCount += 1
    if is_valid_solution(rooms, G, s, numRooms) and len(used) == 0:
        temp = calculate_happiness(rooms, G)
        if temp > maxHap:
            maxHap = temp
            maxRooms = dict(rooms)
            maxNumRooms = numRooms
    rooms = {}
    used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}
    edgeCount = 0
    numRooms = 5
    stresses = s / numRooms
    roomsReverse = {0:[],1:[],2:[],3:[],4:[]}
    while len(used) > 0 and edgeCount < len(edges):
        student1 = edges[edgeCount][0]
        student2 = edges[edgeCount][1]
        if student1 in used and student2 in used:
            temp1 = calculate_stress_for_room(roomsReverse[0] + [student1, student2], G)
            temp2 = calculate_stress_for_room(roomsReverse[1] + [student1, student2], G)
            temp3 = calculate_stress_for_room(roomsReverse[2] + [student1, student2], G)
            temp4 = calculate_stress_for_room(roomsReverse[3] + [student1, student2], G)
            temp5 = calculate_stress_for_room(roomsReverse[4] + [student1, student2], G)
            calcStresses = [temp1, temp2, temp3, temp4, temp5]
            argCalc = np.argsort(calcStresses)
            if calcStresses[argCalc[0]] <= stresses:
                rooms[student1] = argCalc[0]
                rooms[student2] = argCalc[0]
                roomsReverse[argCalc[0]].append(student1)
                roomsReverse[argCalc[0]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[1]] <= stresses:
                rooms[student1] = argCalc[1]
                rooms[student2] = argCalc[1]
                roomsReverse[argCalc[1]].append(student1)
                roomsReverse[argCalc[1]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[2]] <= stresses:
                rooms[student1] = argCalc[2]
                rooms[student2] = argCalc[2]
                roomsReverse[argCalc[2]].append(student1)
                roomsReverse[argCalc[2]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[3]] <= stresses:
                rooms[student1] = argCalc[3]
                rooms[student2] = argCalc[3]
                roomsReverse[argCalc[3]].append(student1)
                roomsReverse[argCalc[3]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[4]] <= stresses:
                rooms[student1] = argCalc[4]
                rooms[student2] = argCalc[4]
                roomsReverse[argCalc[4]].append(student1)
                roomsReverse[argCalc[4]].append(student2)
                used.remove(student1)
                used.remove(student2)
        elif student1 in used and student2 not in used:
            if calculate_stress_for_room(roomsReverse[rooms[student2]] + [student1], G) <= stresses:
                rooms[student1] = int(rooms[student2])
                roomsReverse[rooms[student2]].append(student1)
                used.remove(student1)
        elif student1 not in used and student2 in used:
            if calculate_stress_for_room(roomsReverse[rooms[student1]] + [student2], G) <= stresses:
                rooms[student2] = int(rooms[student1])
                roomsReverse[rooms[student1]].append(student2)
                used.remove(student2)
        edgeCount += 1
    if is_valid_solution(rooms, G, s, numRooms) and len(used) == 0:
        temp = calculate_happiness(rooms, G)
        if temp > maxHap:
            maxHap = temp
            maxRooms = dict(rooms)
            maxNumRooms = numRooms
    rooms = {}
    used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}
    edgeCount = 0
    numRooms = 6
    stresses = s / numRooms
    roomsReverse = {0:[],1:[],2:[],3:[],4:[],5:[]}
    while len(used) > 0 and edgeCount < len(edges):
        student1 = edges[edgeCount][0]
        student2 = edges[edgeCount][1]
        if student1 in used and student2 in used:
            temp1 = calculate_stress_for_room(roomsReverse[0] + [student1, student2], G)
            temp2 = calculate_stress_for_room(roomsReverse[1] + [student1, student2], G)
            temp3 = calculate_stress_for_room(roomsReverse[2] + [student1, student2], G)
            temp4 = calculate_stress_for_room(roomsReverse[3] + [student1, student2], G)
            temp5 = calculate_stress_for_room(roomsReverse[4] + [student1, student2], G)
            temp6 = calculate_stress_for_room(roomsReverse[5] + [student1, student2], G)
            calcStresses = [temp1, temp2, temp3, temp4, temp5, temp6]
            argCalc = np.argsort(calcStresses)
            if calcStresses[argCalc[0]] <= stresses:
                rooms[student1] = argCalc[0]
                rooms[student2] = argCalc[0]
                roomsReverse[argCalc[0]].append(student1)
                roomsReverse[argCalc[0]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[1]] <= stresses:
                rooms[student1] = argCalc[1]
                rooms[student2] = argCalc[1]
                roomsReverse[argCalc[1]].append(student1)
                roomsReverse[argCalc[1]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[2]] <= stresses:
                rooms[student1] = argCalc[2]
                rooms[student2] = argCalc[2]
                roomsReverse[argCalc[2]].append(student1)
                roomsReverse[argCalc[2]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[3]] <= stresses:
                rooms[student1] = argCalc[3]
                rooms[student2] = argCalc[3]
                roomsReverse[argCalc[3]].append(student1)
                roomsReverse[argCalc[3]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[4]] <= stresses:
                rooms[student1] = argCalc[4]
                rooms[student2] = argCalc[4]
                roomsReverse[argCalc[4]].append(student1)
                roomsReverse[argCalc[4]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[5]] <= stresses:
                rooms[student1] = argCalc[5]
                rooms[student2] = argCalc[5]
                roomsReverse[argCalc[5]].append(student1)
                roomsReverse[argCalc[5]].append(student2)
                used.remove(student1)
                used.remove(student2)
        elif student1 in used and student2 not in used:
            if calculate_stress_for_room(roomsReverse[rooms[student2]] + [student1], G) <= stresses:
                rooms[student1] = int(rooms[student2])
                roomsReverse[rooms[student2]].append(student1)
                used.remove(student1)
        elif student1 not in used and student2 in used:
            if calculate_stress_for_room(roomsReverse[rooms[student1]] + [student2], G) <= stresses:
                rooms[student2] = int(rooms[student1])
                roomsReverse[rooms[student1]].append(student2)
                used.remove(student2)
        edgeCount += 1
    if is_valid_solution(rooms, G, s, numRooms) and len(used) == 0:
        temp = calculate_happiness(rooms, G)
        if temp > maxHap:
            maxHap = temp
            maxRooms = dict(rooms)
            maxNumRooms = numRooms
    rooms = {}
    used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}
    edgeCount = 0
    numRooms = 7
    stresses = s / numRooms
    roomsReverse = {0:[],1:[],2:[],3:[],4:[],5:[],6:[]}
    while len(used) > 0 and edgeCount < len(edges):
        student1 = edges[edgeCount][0]
        student2 = edges[edgeCount][1]
        if student1 in used and student2 in used:
            temp1 = calculate_stress_for_room(roomsReverse[0] + [student1, student2], G)
            temp2 = calculate_stress_for_room(roomsReverse[1] + [student1, student2], G)
            temp3 = calculate_stress_for_room(roomsReverse[2] + [student1, student2], G)
            temp4 = calculate_stress_for_room(roomsReverse[3] + [student1, student2], G)
            temp5 = calculate_stress_for_room(roomsReverse[4] + [student1, student2], G)
            temp6 = calculate_stress_for_room(roomsReverse[5] + [student1, student2], G)
            temp7 = calculate_stress_for_room(roomsReverse[6] + [student1, student2], G)
            calcStresses = [temp1, temp2, temp3, temp4, temp5, temp6, temp7]
            argCalc = np.argsort(calcStresses)
            if calcStresses[argCalc[0]] <= stresses:
                rooms[student1] = argCalc[0]
                rooms[student2] = argCalc[0]
                roomsReverse[argCalc[0]].append(student1)
                roomsReverse[argCalc[0]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[1]] <= stresses:
                rooms[student1] = argCalc[1]
                rooms[student2] = argCalc[1]
                roomsReverse[argCalc[1]].append(student1)
                roomsReverse[argCalc[1]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[2]] <= stresses:
                rooms[student1] = argCalc[2]
                rooms[student2] = argCalc[2]
                roomsReverse[argCalc[2]].append(student1)
                roomsReverse[argCalc[2]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[3]] <= stresses:
                rooms[student1] = argCalc[3]
                rooms[student2] = argCalc[3]
                roomsReverse[argCalc[3]].append(student1)
                roomsReverse[argCalc[3]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[4]] <= stresses:
                rooms[student1] = argCalc[4]
                rooms[student2] = argCalc[4]
                roomsReverse[argCalc[4]].append(student1)
                roomsReverse[argCalc[4]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[5]] <= stresses:
                rooms[student1] = argCalc[5]
                rooms[student2] = argCalc[5]
                roomsReverse[argCalc[5]].append(student1)
                roomsReverse[argCalc[5]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[6]] <= stresses:
                rooms[student1] = argCalc[6]
                rooms[student2] = argCalc[6]
                roomsReverse[argCalc[6]].append(student1)
                roomsReverse[argCalc[6]].append(student2)
                used.remove(student1)
                used.remove(student2)
        elif student1 in used and student2 not in used:
            if calculate_stress_for_room(roomsReverse[rooms[student2]] + [student1], G) <= stresses:
                rooms[student1] = int(rooms[student2])
                roomsReverse[rooms[student2]].append(student1)
                used.remove(student1)
        elif student1 not in used and student2 in used:
            if calculate_stress_for_room(roomsReverse[rooms[student1]] + [student2], G) <= stresses:
                rooms[student2] = int(rooms[student1])
                roomsReverse[rooms[student1]].append(student2)
                used.remove(student2)
        edgeCount += 1
    if is_valid_solution(rooms, G, s, numRooms) and len(used) == 0:
        temp = calculate_happiness(rooms, G)
        if temp > maxHap:
            maxHap = temp
            maxRooms = dict(rooms)
            maxNumRooms = numRooms
    rooms = {}
    used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}
    edgeCount = 0
    numRooms = 8
    stresses = s / numRooms
    roomsReverse = {0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[]}
    while len(used) > 0 and edgeCount < len(edges):
        student1 = edges[edgeCount][0]
        student2 = edges[edgeCount][1]
        if student1 in used and student2 in used:
            temp1 = calculate_stress_for_room(roomsReverse[0] + [student1, student2], G)
            temp2 = calculate_stress_for_room(roomsReverse[1] + [student1, student2], G)
            temp3 = calculate_stress_for_room(roomsReverse[2] + [student1, student2], G)
            temp4 = calculate_stress_for_room(roomsReverse[3] + [student1, student2], G)
            temp5 = calculate_stress_for_room(roomsReverse[4] + [student1, student2], G)
            temp6 = calculate_stress_for_room(roomsReverse[5] + [student1, student2], G)
            temp7 = calculate_stress_for_room(roomsReverse[6] + [student1, student2], G)
            temp8 = calculate_stress_for_room(roomsReverse[7] + [student1, student2], G)
            calcStresses = [temp1, temp2, temp3, temp4, temp5, temp6, temp7, temp8]
            argCalc = np.argsort(calcStresses)
            if calcStresses[argCalc[0]] <= stresses:
                rooms[student1] = argCalc[0]
                rooms[student2] = argCalc[0]
                roomsReverse[argCalc[0]].append(student1)
                roomsReverse[argCalc[0]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[1]] <= stresses:
                rooms[student1] = argCalc[1]
                rooms[student2] = argCalc[1]
                roomsReverse[argCalc[1]].append(student1)
                roomsReverse[argCalc[1]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[2]] <= stresses:
                rooms[student1] = argCalc[2]
                rooms[student2] = argCalc[2]
                roomsReverse[argCalc[2]].append(student1)
                roomsReverse[argCalc[2]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[3]] <= stresses:
                rooms[student1] = argCalc[3]
                rooms[student2] = argCalc[3]
                roomsReverse[argCalc[3]].append(student1)
                roomsReverse[argCalc[3]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[4]] <= stresses:
                rooms[student1] = argCalc[4]
                rooms[student2] = argCalc[4]
                roomsReverse[argCalc[4]].append(student1)
                roomsReverse[argCalc[4]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[5]] <= stresses:
                rooms[student1] = argCalc[5]
                rooms[student2] = argCalc[5]
                roomsReverse[argCalc[5]].append(student1)
                roomsReverse[argCalc[5]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[6]] <= stresses:
                rooms[student1] = argCalc[6]
                rooms[student2] = argCalc[6]
                roomsReverse[argCalc[6]].append(student1)
                roomsReverse[argCalc[6]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[7]] <= stresses:
                rooms[student1] = argCalc[7]
                rooms[student2] = argCalc[7]
                roomsReverse[argCalc[7]].append(student1)
                roomsReverse[argCalc[7]].append(student2)
                used.remove(student1)
                used.remove(student2)
        elif student1 in used and student2 not in used:
            if calculate_stress_for_room(roomsReverse[rooms[student2]] + [student1], G) <= stresses:
                rooms[student1] = int(rooms[student2])
                roomsReverse[rooms[student2]].append(student1)
                used.remove(student1)
        elif student1 not in used and student2 in used:
            if calculate_stress_for_room(roomsReverse[rooms[student1]] + [student2], G) <= stresses:
                rooms[student2] = int(rooms[student1])
                roomsReverse[rooms[student1]].append(student2)
                used.remove(student2)
        edgeCount += 1
    if is_valid_solution(rooms, G, s, numRooms) and len(used) == 0:
        temp = calculate_happiness(rooms, G)
        if temp > maxHap:
            maxHap = temp
            maxRooms = dict(rooms)
            maxNumRooms = numRooms
    rooms = {}
    used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}
    edgeCount = 0
    numRooms = 9
    stresses = s / numRooms
    roomsReverse = {0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[]}
    while len(used) > 0 and edgeCount < len(edges):
        student1 = edges[edgeCount][0]
        student2 = edges[edgeCount][1]
        if student1 in used and student2 in used:
            temp1 = calculate_stress_for_room(roomsReverse[0] + [student1, student2], G)
            temp2 = calculate_stress_for_room(roomsReverse[1] + [student1, student2], G)
            temp3 = calculate_stress_for_room(roomsReverse[2] + [student1, student2], G)
            temp4 = calculate_stress_for_room(roomsReverse[3] + [student1, student2], G)
            temp5 = calculate_stress_for_room(roomsReverse[4] + [student1, student2], G)
            temp6 = calculate_stress_for_room(roomsReverse[5] + [student1, student2], G)
            temp7 = calculate_stress_for_room(roomsReverse[6] + [student1, student2], G)
            temp8 = calculate_stress_for_room(roomsReverse[7] + [student1, student2], G)
            temp9 = calculate_stress_for_room(roomsReverse[8] + [student1, student2], G)
            calcStresses = [temp1, temp2, temp3, temp4, temp5, temp6, temp7, temp8, temp9]
            argCalc = np.argsort(calcStresses)
            if calcStresses[argCalc[0]] <= stresses:
                rooms[student1] = argCalc[0]
                rooms[student2] = argCalc[0]
                roomsReverse[argCalc[0]].append(student1)
                roomsReverse[argCalc[0]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[1]] <= stresses:
                rooms[student1] = argCalc[1]
                rooms[student2] = argCalc[1]
                roomsReverse[argCalc[1]].append(student1)
                roomsReverse[argCalc[1]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[2]] <= stresses:
                rooms[student1] = argCalc[2]
                rooms[student2] = argCalc[2]
                roomsReverse[argCalc[2]].append(student1)
                roomsReverse[argCalc[2]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[3]] <= stresses:
                rooms[student1] = argCalc[3]
                rooms[student2] = argCalc[3]
                roomsReverse[argCalc[3]].append(student1)
                roomsReverse[argCalc[3]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[4]] <= stresses:
                rooms[student1] = argCalc[4]
                rooms[student2] = argCalc[4]
                roomsReverse[argCalc[4]].append(student1)
                roomsReverse[argCalc[4]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[5]] <= stresses:
                rooms[student1] = argCalc[5]
                rooms[student2] = argCalc[5]
                roomsReverse[argCalc[5]].append(student1)
                roomsReverse[argCalc[5]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[6]] <= stresses:
                rooms[student1] = argCalc[6]
                rooms[student2] = argCalc[6]
                roomsReverse[argCalc[6]].append(student1)
                roomsReverse[argCalc[6]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[7]] <= stresses:
                rooms[student1] = argCalc[7]
                rooms[student2] = argCalc[7]
                roomsReverse[argCalc[7]].append(student1)
                roomsReverse[argCalc[7]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[8]] <= stresses:
                rooms[student1] = argCalc[8]
                rooms[student2] = argCalc[8]
                roomsReverse[argCalc[8]].append(student1)
                roomsReverse[argCalc[8]].append(student2)
                used.remove(student1)
                used.remove(student2)
        elif student1 in used and student2 not in used:
            if calculate_stress_for_room(roomsReverse[rooms[student2]] + [student1], G) <= stresses:
                rooms[student1] = int(rooms[student2])
                roomsReverse[rooms[student2]].append(student1)
                used.remove(student1)
        elif student1 not in used and student2 in used:
            if calculate_stress_for_room(roomsReverse[rooms[student1]] + [student2], G) <= stresses:
                rooms[student2] = int(rooms[student1])
                roomsReverse[rooms[student1]].append(student2)
                used.remove(student2)
        edgeCount += 1
    if is_valid_solution(rooms, G, s, numRooms) and len(used) == 0:
        temp = calculate_happiness(rooms, G)
        if temp > maxHap:
            maxHap = temp
            maxRooms = dict(rooms)
            maxNumRooms = numRooms
    rooms = {}
    used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}
    edgeCount = 0
    numRooms = 10
    stresses = s / numRooms
    roomsReverse = {0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[]}
    while len(used) > 0 and edgeCount < len(edges):
        student1 = edges[edgeCount][0]
        student2 = edges[edgeCount][1]
        if student1 in used and student2 in used:
            temp1 = calculate_stress_for_room(roomsReverse[0] + [student1, student2], G)
            temp2 = calculate_stress_for_room(roomsReverse[1] + [student1, student2], G)
            temp3 = calculate_stress_for_room(roomsReverse[2] + [student1, student2], G)
            temp4 = calculate_stress_for_room(roomsReverse[3] + [student1, student2], G)
            temp5 = calculate_stress_for_room(roomsReverse[4] + [student1, student2], G)
            temp6 = calculate_stress_for_room(roomsReverse[5] + [student1, student2], G)
            temp7 = calculate_stress_for_room(roomsReverse[6] + [student1, student2], G)
            temp8 = calculate_stress_for_room(roomsReverse[7] + [student1, student2], G)
            temp9 = calculate_stress_for_room(roomsReverse[8] + [student1, student2], G)
            temp10 = calculate_stress_for_room(roomsReverse[9] + [student1, student2], G)
            calcStresses = [temp1, temp2, temp3, temp4, temp5, temp6, temp7, temp8, temp9, temp10]
            argCalc = np.argsort(calcStresses)
            if calcStresses[argCalc[0]] <= stresses:
                rooms[student1] = argCalc[0]
                rooms[student2] = argCalc[0]
                roomsReverse[argCalc[0]].append(student1)
                roomsReverse[argCalc[0]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[1]] <= stresses:
                rooms[student1] = argCalc[1]
                rooms[student2] = argCalc[1]
                roomsReverse[argCalc[1]].append(student1)
                roomsReverse[argCalc[1]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[2]] <= stresses:
                rooms[student1] = argCalc[2]
                rooms[student2] = argCalc[2]
                roomsReverse[argCalc[2]].append(student1)
                roomsReverse[argCalc[2]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[3]] <= stresses:
                rooms[student1] = argCalc[3]
                rooms[student2] = argCalc[3]
                roomsReverse[argCalc[3]].append(student1)
                roomsReverse[argCalc[3]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[4]] <= stresses:
                rooms[student1] = argCalc[4]
                rooms[student2] = argCalc[4]
                roomsReverse[argCalc[4]].append(student1)
                roomsReverse[argCalc[4]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[5]] <= stresses:
                rooms[student1] = argCalc[5]
                rooms[student2] = argCalc[5]
                roomsReverse[argCalc[5]].append(student1)
                roomsReverse[argCalc[5]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[6]] <= stresses:
                rooms[student1] = argCalc[6]
                rooms[student2] = argCalc[6]
                roomsReverse[argCalc[6]].append(student1)
                roomsReverse[argCalc[6]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[7]] <= stresses:
                rooms[student1] = argCalc[7]
                rooms[student2] = argCalc[7]
                roomsReverse[argCalc[7]].append(student1)
                roomsReverse[argCalc[7]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[8]] <= stresses:
                rooms[student1] = argCalc[8]
                rooms[student2] = argCalc[8]
                roomsReverse[argCalc[8]].append(student1)
                roomsReverse[argCalc[8]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[9]] <= stresses:
                rooms[student1] = argCalc[9]
                rooms[student2] = argCalc[9]
                roomsReverse[argCalc[9]].append(student1)
                roomsReverse[argCalc[9]].append(student2)
                used.remove(student1)
                used.remove(student2)
        elif student1 in used and student2 not in used:
            if calculate_stress_for_room(roomsReverse[rooms[student2]] + [student1], G) <= stresses:
                rooms[student1] = int(rooms[student2])
                roomsReverse[rooms[student2]].append(student1)
                used.remove(student1)
        elif student1 not in used and student2 in used:
            if calculate_stress_for_room(roomsReverse[rooms[student1]] + [student2], G) <= stresses:
                rooms[student2] = int(rooms[student1])
                roomsReverse[rooms[student1]].append(student2)
                used.remove(student2)
        edgeCount += 1
    if is_valid_solution(rooms, G, s, numRooms) and len(used) == 0:
        temp = calculate_happiness(rooms, G)
        if temp > maxHap:
            maxHap = temp
            maxRooms = dict(rooms)
            maxNumRooms = numRooms
    rooms = {}
    used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}
    edgeCount = 0
    numRooms = 11
    stresses = s / numRooms
    roomsReverse = {0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[]}
    while len(used) > 0 and edgeCount < len(edges):
        student1 = edges[edgeCount][0]
        student2 = edges[edgeCount][1]
        if student1 in used and student2 in used:
            temp1 = calculate_stress_for_room(roomsReverse[0] + [student1, student2], G)
            temp2 = calculate_stress_for_room(roomsReverse[1] + [student1, student2], G)
            temp3 = calculate_stress_for_room(roomsReverse[2] + [student1, student2], G)
            temp4 = calculate_stress_for_room(roomsReverse[3] + [student1, student2], G)
            temp5 = calculate_stress_for_room(roomsReverse[4] + [student1, student2], G)
            temp6 = calculate_stress_for_room(roomsReverse[5] + [student1, student2], G)
            temp7 = calculate_stress_for_room(roomsReverse[6] + [student1, student2], G)
            temp8 = calculate_stress_for_room(roomsReverse[7] + [student1, student2], G)
            temp9 = calculate_stress_for_room(roomsReverse[8] + [student1, student2], G)
            temp10 = calculate_stress_for_room(roomsReverse[9] + [student1, student2], G)
            temp11 = calculate_stress_for_room(roomsReverse[10] + [student1, student2], G)
            calcStresses = [temp1, temp2, temp3, temp4, temp5, temp6, temp7, temp8, temp9, temp10, temp11]
            argCalc = np.argsort(calcStresses)
            if calcStresses[argCalc[0]] <= stresses:
                rooms[student1] = argCalc[0]
                rooms[student2] = argCalc[0]
                roomsReverse[argCalc[0]].append(student1)
                roomsReverse[argCalc[0]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[1]] <= stresses:
                rooms[student1] = argCalc[1]
                rooms[student2] = argCalc[1]
                roomsReverse[argCalc[1]].append(student1)
                roomsReverse[argCalc[1]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[2]] <= stresses:
                rooms[student1] = argCalc[2]
                rooms[student2] = argCalc[2]
                roomsReverse[argCalc[2]].append(student1)
                roomsReverse[argCalc[2]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[3]] <= stresses:
                rooms[student1] = argCalc[3]
                rooms[student2] = argCalc[3]
                roomsReverse[argCalc[3]].append(student1)
                roomsReverse[argCalc[3]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[4]] <= stresses:
                rooms[student1] = argCalc[4]
                rooms[student2] = argCalc[4]
                roomsReverse[argCalc[4]].append(student1)
                roomsReverse[argCalc[4]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[5]] <= stresses:
                rooms[student1] = argCalc[5]
                rooms[student2] = argCalc[5]
                roomsReverse[argCalc[5]].append(student1)
                roomsReverse[argCalc[5]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[6]] <= stresses:
                rooms[student1] = argCalc[6]
                rooms[student2] = argCalc[6]
                roomsReverse[argCalc[6]].append(student1)
                roomsReverse[argCalc[6]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[7]] <= stresses:
                rooms[student1] = argCalc[7]
                rooms[student2] = argCalc[7]
                roomsReverse[argCalc[7]].append(student1)
                roomsReverse[argCalc[7]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[8]] <= stresses:
                rooms[student1] = argCalc[8]
                rooms[student2] = argCalc[8]
                roomsReverse[argCalc[8]].append(student1)
                roomsReverse[argCalc[8]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[9]] <= stresses:
                rooms[student1] = argCalc[9]
                rooms[student2] = argCalc[9]
                roomsReverse[argCalc[9]].append(student1)
                roomsReverse[argCalc[9]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[10]] <= stresses:
                rooms[student1] = argCalc[10]
                rooms[student2] = argCalc[10]
                roomsReverse[argCalc[10]].append(student1)
                roomsReverse[argCalc[10]].append(student2)
                used.remove(student1)
                used.remove(student2)
        elif student1 in used and student2 not in used:
            if calculate_stress_for_room(roomsReverse[rooms[student2]] + [student1], G) <= stresses:
                rooms[student1] = int(rooms[student2])
                roomsReverse[rooms[student2]].append(student1)
                used.remove(student1)
        elif student1 not in used and student2 in used:
            if calculate_stress_for_room(roomsReverse[rooms[student1]] + [student2], G) <= stresses:
                rooms[student2] = int(rooms[student1])
                roomsReverse[rooms[student1]].append(student2)
                used.remove(student2)
        edgeCount += 1
    if is_valid_solution(rooms, G, s, numRooms) and len(used) == 0:
        temp = calculate_happiness(rooms, G)
        if temp > maxHap:
            maxHap = temp
            maxRooms = dict(rooms)
            maxNumRooms = numRooms
    rooms = {}
    used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}
    edgeCount = 0
    numRooms = 12
    stresses = s / numRooms
    roomsReverse = {0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[],11:[]}
    while len(used) > 0 and edgeCount < len(edges):
        student1 = edges[edgeCount][0]
        student2 = edges[edgeCount][1]
        if student1 in used and student2 in used:
            temp1 = calculate_stress_for_room(roomsReverse[0] + [student1, student2], G)
            temp2 = calculate_stress_for_room(roomsReverse[1] + [student1, student2], G)
            temp3 = calculate_stress_for_room(roomsReverse[2] + [student1, student2], G)
            temp4 = calculate_stress_for_room(roomsReverse[3] + [student1, student2], G)
            temp5 = calculate_stress_for_room(roomsReverse[4] + [student1, student2], G)
            temp6 = calculate_stress_for_room(roomsReverse[5] + [student1, student2], G)
            temp7 = calculate_stress_for_room(roomsReverse[6] + [student1, student2], G)
            temp8 = calculate_stress_for_room(roomsReverse[7] + [student1, student2], G)
            temp9 = calculate_stress_for_room(roomsReverse[8] + [student1, student2], G)
            temp10 = calculate_stress_for_room(roomsReverse[9] + [student1, student2], G)
            temp11 = calculate_stress_for_room(roomsReverse[10] + [student1, student2], G)
            temp12 = calculate_stress_for_room(roomsReverse[11] + [student1, student2], G)
            calcStresses = [temp1, temp2, temp3, temp4, temp5, temp6, temp7, temp8, temp9, temp10, temp11, temp12]
            argCalc = np.argsort(calcStresses)
            if calcStresses[argCalc[0]] <= stresses:
                rooms[student1] = argCalc[0]
                rooms[student2] = argCalc[0]
                roomsReverse[argCalc[0]].append(student1)
                roomsReverse[argCalc[0]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[1]] <= stresses:
                rooms[student1] = argCalc[1]
                rooms[student2] = argCalc[1]
                roomsReverse[argCalc[1]].append(student1)
                roomsReverse[argCalc[1]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[2]] <= stresses:
                rooms[student1] = argCalc[2]
                rooms[student2] = argCalc[2]
                roomsReverse[argCalc[2]].append(student1)
                roomsReverse[argCalc[2]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[3]] <= stresses:
                rooms[student1] = argCalc[3]
                rooms[student2] = argCalc[3]
                roomsReverse[argCalc[3]].append(student1)
                roomsReverse[argCalc[3]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[4]] <= stresses:
                rooms[student1] = argCalc[4]
                rooms[student2] = argCalc[4]
                roomsReverse[argCalc[4]].append(student1)
                roomsReverse[argCalc[4]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[5]] <= stresses:
                rooms[student1] = argCalc[5]
                rooms[student2] = argCalc[5]
                roomsReverse[argCalc[5]].append(student1)
                roomsReverse[argCalc[5]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[6]] <= stresses:
                rooms[student1] = argCalc[6]
                rooms[student2] = argCalc[6]
                roomsReverse[argCalc[6]].append(student1)
                roomsReverse[argCalc[6]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[7]] <= stresses:
                rooms[student1] = argCalc[7]
                rooms[student2] = argCalc[7]
                roomsReverse[argCalc[7]].append(student1)
                roomsReverse[argCalc[7]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[8]] <= stresses:
                rooms[student1] = argCalc[8]
                rooms[student2] = argCalc[8]
                roomsReverse[argCalc[8]].append(student1)
                roomsReverse[argCalc[8]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[9]] <= stresses:
                rooms[student1] = argCalc[9]
                rooms[student2] = argCalc[9]
                roomsReverse[argCalc[9]].append(student1)
                roomsReverse[argCalc[9]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[10]] <= stresses:
                rooms[student1] = argCalc[10]
                rooms[student2] = argCalc[10]
                roomsReverse[argCalc[10]].append(student1)
                roomsReverse[argCalc[10]].append(student2)
                used.remove(student1)
                used.remove(student2)
            elif calcStresses[argCalc[11]] <= stresses:
                rooms[student1] = argCalc[11]
                rooms[student2] = argCalc[11]
                roomsReverse[argCalc[11]].append(student1)
                roomsReverse[argCalc[11]].append(student2)
                used.remove(student1)
                used.remove(student2)
        elif student1 in used and student2 not in used:
            if calculate_stress_for_room(roomsReverse[rooms[student2]] + [student1], G) <= stresses:
                rooms[student1] = int(rooms[student2])
                roomsReverse[rooms[student2]].append(student1)
                used.remove(student1)
        elif student1 not in used and student2 in used:
            if calculate_stress_for_room(roomsReverse[rooms[student1]] + [student2], G) <= stresses:
                rooms[student2] = int(rooms[student1])
                roomsReverse[rooms[student1]].append(student2)
                used.remove(student2)
        edgeCount += 1
    if is_valid_solution(rooms, G, s, numRooms) and len(used) == 0:
        temp = calculate_happiness(rooms, G)
        if temp > maxHap:
            maxHap = temp
            maxRooms = dict(rooms)
            maxNumRooms = numRooms
    rooms = {}
    used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}
    edgeCount = 0

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
    # numRooms = 1
    # for student in range(20):
    #     rooms[student] = 0
    # if is_valid_solution(rooms, G, s, numRooms):
    #         temp = calculate_happiness(rooms, G)
    #         if temp > maxHap:
    #             maxHap = temp
    #             maxRooms = rooms
    #             maxNumRooms = numRooms
    # rooms = {}
    # used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}
    # numRooms = 2
    # for i in range(1, 20):
    #     for comb in itertools.combinations(used, i):
    #         for student in comb:
    #             rooms[student] = 0
    #             used.remove(student)
    #         for student in used:
    #             rooms[student] = 1
    #         if is_valid_solution(rooms, G, s, numRooms):
    #                 temp = calculate_happiness(rooms, G)
    #                 if temp > maxHap:
    #                     maxHap = temp
    #                     maxRooms = rooms
    #                     maxNumRooms = numRooms
    #         rooms = {}
    #         used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}
    # numRooms = 3
    # for i in range(1, 20):
    #     for comb1 in itertools.combinations(used, i):
    #         for student in comb1:
    #             rooms[student] = 0
    #             used.remove(student)
    #         rooms1 = dict(rooms)
    #         used1 = set(used)
    #         for j in range(1, 20-i):
    #             for comb2 in itertools.combinations(used, j):
    #                 for student in comb2:
    #                     rooms[student] = 1
    #                     used.remove(student)
    #                 for student in used:
    #                     rooms[student] = 2
    #                 if is_valid_solution(rooms, G, s, numRooms):
    #                         temp = calculate_happiness(rooms, G)
    #                         if temp > maxHap:
    #                             maxHap = temp
    #                             maxRooms = rooms
    #                             maxNumRooms = numRooms
    #                 rooms = dict(rooms1)
    #                 used = set(used1)
    #         rooms = {}
    #         used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}
    # numRooms = 4
    # for i in range(1, 20):
    #     for comb1 in itertools.combinations(used, i):
    #         for student in comb1:
    #             rooms[student] = 0
    #             used.remove(student)
    #         rooms1 = dict(rooms)
    #         used1 = set(used)
    #         for j in range(1, 20-i):
    #             for comb2 in itertools.combinations(used, j):
    #                 for student in comb2:
    #                     rooms[student] = 1
    #                     used.remove(student)
    #                 rooms2 = dict(rooms)
    #                 used2 = set(used)
    #                 for k in range(1, 20-i-j):
    #                     for comb3 in itertools.combinations(used, k):
    #                         for student in comb3:
    #                             rooms[student] = 2
    #                             used.remove(student)
    #                         for student in used:
    #                             rooms[student] = 3
    #                         if is_valid_solution(rooms, G, s, numRooms):
    #                                 temp = calculate_happiness(rooms, G)
    #                                 if temp > maxHap:
    #                                     maxHap = temp
    #                                     maxRooms = rooms
    #                                     maxNumRooms = numRooms
    #                         rooms = dict(rooms2)
    #                         used = set(used2)
    #                 rooms = dict(rooms1)
    #                 used = set(used1)
    #         rooms = {}
    #         used = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}


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
    inputs = glob.glob('inputs/medium/*')
    for input_path in inputs:
        output_path = 'outputs/medium/' + os.path.basename(os.path.normpath(input_path))[:-3] + '.out'
        G, s = read_input_file(input_path, 100)
        D, k = solve(G, s)
        assert is_valid_solution(D, G, s, k)
        cost_t = calculate_happiness(D, G)
        print(cost_t)
        write_output_file(D, output_path)
