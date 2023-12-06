#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 22 Day 12 - Hill Climbing Algorithm """

from paoc.helper import get_input, print_summary
import numpy as np


def p1() -> any:
    heightmap_str = get_input(12)
    heightmap_str_arr = np.array([list(row) for row in heightmap_str])
    start_pos = np.argwhere(heightmap_str_arr == 'S')[0]
    goal_pos = np.argwhere(heightmap_str_arr == 'E')[0]

    # Create a numpy array of the heightmap with the height of each position as int
    # first we have to map S and E to the lowest and highest elevation, respectively
    heightmap_str_arr[heightmap_str_arr == 'S'] = 'a'
    heightmap_str_arr[heightmap_str_arr == 'E'] = 'z'
    heightmap = np.array([[ord(c) - 97 for c in row] for row in heightmap_str_arr])

    # plt.imshow(heightmap)
    # plt.show()

    # Create a graph where each node is a position on the heightmap
    # We then add edges between nodes that are adjacent and have a height difference of at most +1
    # negative height differences are allowed
    graph = {}
    for i in range(heightmap.shape[0]):
        for j in range(heightmap.shape[1]):
            graph[(i, j)] = []
            for i2 in range(i - 1, i + 2):
                for j2 in range(j - 1, j + 2):
                    if i2 == i and j2 == j:
                        continue
                    # continue on diagonals
                    if i2 != i and j2 != j:
                        continue
                    if i2 < 0 or i2 >= heightmap.shape[0] or j2 < 0 or j2 >= heightmap.shape[1]:
                        continue
                    if abs(heightmap[i, j] - heightmap[i2, j2]) <= 1 or heightmap[i2, j2] < heightmap[i, j]:
                        graph[(i, j)].append((i2, j2))

    # Use A* to find the shortest path from S to E
    # We use the manhattan distance as heuristic
    def heuristic(pos):
        return abs(pos[0] - goal_pos[0]) + abs(pos[1] - goal_pos[1])

    def a_star(start, goal):
        frontier = [(0, start)]
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while frontier:
            current = frontier.pop(0)[1]
            if current == goal:
                break

            for next in graph[current]:
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + heuristic(next)
                    frontier.append((priority, next))
                    came_from[next] = current

        return cost_so_far[goal]

    return a_star(tuple(start_pos), tuple(goal_pos))

def p2() -> any:
    heightmap_str = get_input(12)
    heightmap_str_arr = np.array([list(row) for row in heightmap_str])

    # get other starting positions
    start_positions = []
    for i in range(heightmap_str_arr.shape[0]):
        for j in range(heightmap_str_arr.shape[1]):
            if heightmap_str_arr[i, j] == 'a' or heightmap_str_arr[i, j] == 'S':
                start_positions.append((i, j))

    goal_pos = np.argwhere(heightmap_str_arr == 'E')[0]

    results = set()
    for start_pos in start_positions:
        res = finish_rest(start_pos, heightmap_str_arr, goal_pos)
        results.add(res)
    return min(results)

def finish_rest(start_pos, heightmap_str_arr, goal_pos):
    # Create a numpy array of the heightmap with the height of each position as int
    # first we have to map S and E to the lowest and highest elevation, respectively
    heightmap_str_arr[heightmap_str_arr == 'S'] = 'a'
    heightmap_str_arr[heightmap_str_arr == 'E'] = 'z'
    heightmap = np.array([[ord(c) - 97 for c in row] for row in heightmap_str_arr])

    # plt.imshow(heightmap)
    # plt.show()

    # Create a graph where each node is a position on the heightmap
    # We then add edges between nodes that are adjacent and have a height difference of at most +1
    # negative height differences are allowed
    graph = {}
    for i in range(heightmap.shape[0]):
        for j in range(heightmap.shape[1]):
            graph[(i, j)] = []
            for i2 in range(i - 1, i + 2):
                for j2 in range(j - 1, j + 2):
                    if i2 == i and j2 == j:
                        continue
                    # continue on diagonals
                    if i2 != i and j2 != j:
                        continue
                    if i2 < 0 or i2 >= heightmap.shape[0] or j2 < 0 or j2 >= heightmap.shape[1]:
                        continue
                    if abs(heightmap[i, j] - heightmap[i2, j2]) <= 1 or heightmap[i2, j2] < heightmap[i, j]:
                        graph[(i, j)].append((i2, j2))

    # Use A* to find the shortest path from S to E
    # We use the manhattan distance as heuristic
    def heuristic(pos):
        return abs(pos[0] - goal_pos[0]) + abs(pos[1] - goal_pos[1])

    def a_star(start, goal):
        frontier = [(0, start)]
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while frontier:
            current = frontier.pop(0)[1]
            if current == goal:
                break

            for next in graph[current]:
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + heuristic(next)
                    frontier.append((priority, next))
                    came_from[next] = current
        try:
            return cost_so_far[goal]
        except KeyError:
            return 1000000

    return a_star(tuple(start_pos), tuple(goal_pos))


if __name__ == '__main__':
    print_summary(__file__, p1, p2, n=10)
