from heapq import heappush, heappop
import itertools

#  Update: A* Algorithm Implemented
# import copy
# import numpy


def inverse_num(x):
    if x == 1:
        return 0
    if x == 0:
        return 1
    else:
        print("wtf")


# Creating the maze
# Referenced in the main()
def take_maze(data_lines):
    maze = []
    size = int(data_lines[0])
    for x in range(1, size + 1):
        maze.append(list(map(int, data_lines[x].split())))
    del data_lines[0 : size + 2]
    for i in range(len(maze)):
        maze[i] = list(map(inverse_num, maze[i]))
    return data_lines, maze


# Cell class for each node in the path
class cell:
    # Default constructor that stores
    #   x,y coordinates,
    #   g - distance from the starting location
    #   parent - parent node
    #   h - heuristically calculated value for distance from the end point
    #       set to -1111 as default.
    #   f - total score for the nodes (sum of g and h values)
    #       set to -1111 as default.
    def __init__(self, x, y, g, parent) -> None:
        self.x = x
        self.y = y
        self.g = g
        self.parent = parent
        self.h = -11111
        self.f = -11111

    # Calculates the heuristics value for each node based on an attributed goal
    #   referenced from https://www.geeksforgeeks.org/a-search-algorithm/
    def heuristics(self, goal):
        self.h = abs(self.x - goal[0]) + abs(self.y - goal[1])

    # Calculates the f (score) value based on the value of g & h of node
    #   => this is the considered score before we move through the maze,
    #      the lesser the score the closer the next node is to the exit.
    def calc_f(self):
        self.f = self.h + self.g
        return self.h + self.g

    def __lt__(self, other):
        return self.f < other.f


# Implementation of A* algorithm
def start_astar(maze_arr, start, goal, n):
    # initialize the starting node (which is at )
    start_node = cell(start[0], start[1], 0, None)

    # Initialize the open list & place the starting node in it
    open_list = [start_node]

    visited = {}
    # loop while the open_list is not empty
    while open_list:
        q = open_list.pop(0)
        x, y, g = q.x, q.y, q.g
        print(f"Searching at pint i:{q.x} j:{q.y}")
        if f"{q.x} {q.y}" not in visited:
            if x < n - 1 and maze_arr[x + 1][y] != 1:
                new_up = cell(x + 1, y, g + 1, q)
                if new_up.x == goal[0] and new_up.y == goal[1]:
                    return new_up
                # If the successor has more score than equivalent in open list, skip
                else:
                    open_list.append(new_up)

            if y < n - 1 and maze_arr[x][y + 1] != 1:
                new_right = cell(x, y + 1, g + 1, q)
                if new_right.x == goal[0] and new_right.y == goal[1]:
                    return new_right
                else:
                    open_list.append(new_right)

            if x > 0 and maze_arr[x - 1][y] != 1:
                new_down = cell(x - 1, y, g + 1, q)
                if new_down.x == goal[0] and new_down.y == goal[1]:
                    return new_down
                else:
                    open_list.append(new_down)

            if y > 0 and maze_arr[x][y - 1] != 1:
                new_left = cell(x, y - 1, g + 1, q)
                if new_left.x == goal[0] and new_left.y == goal[1]:
                    return new_left
                # If the successor has more score than equivalent in open list, skip
                else:
                    open_list.append(new_left)

            # After we are done with checking all the possible neighbors for the node,
            # We put it in the closed_list\
            visited[f"{q.x} {q.y}"] = True


# iterates through each node.parent (the direction where it came from)
# #  until node.parent is None (reaches the start point)
#   checks the node.parent and stores it in node
def get_shortestPath(node):
    store = []
    while node.parent is not None:
        store.append([f"{node.x} {node.y}"])
        node = node.parent
    store.append([f"{node.x} {node.y}"])
    return store


def display_path(new_path_maze, k, count):
    num = 0
    while k.parent is not None:
        new_path_maze[k.x][k.y] = num
        num += 10
        k = k.parent
    new_path_maze[k.x][k.y] = num
    with open("outputBFS.txt", "a") as o:
        # write.write(' '.join(str(x) for x in new_path_maze))
        o.write("Displaying Maze: " + str(count) + "\n")
        for x in new_path_maze:
            o.write("\t".join(map(str, x)))
            o.write("\n")
        o.write("\n")


if __name__ == "__main__":
    # Open the maze document
    with open("mazes.txt", "r") as data:
        h = data.read()
    new_data = h.split("\n")
    # array that stores the maze
    maze_arr = []
    # initializing the start node - which is 0,0 in this case.
    start = [0, 0, None]
    # holds the output for each successful maze
    output = []
    count = 0

    # iterates through all the mazes
    while new_data:
        # clears the maze for the new maze
        maze_arr.clear()
        # calls the take_maze() function that
        #   (1) Creates the maze
        #   (2) Removes the maze of new_data
        #   (3) Returns the (new) new_data and maze
        new_data, maze_arr = take_maze(new_data)
        # number of rows in the maze
        n = len(maze_arr)
        # initializes the goal of the maze-which is at the bottom right element
        goal = [n - 1, n - 1]
        # start the A* algorithm
        node = start_astar(maze_arr, start, goal, n)
        # increment count (each iterated node)
        count += 1
        # checks if it found the node or got lost
        #   None - signifies the maze didn't have a way out.
        #   class (cell) - returns the goal_node
        if node is None:
            # displays that it couldn't work
            print("Welp! Maze", count, "didn't work, I guess we're stuck \n")
        else:
            print("Wohoo! Maze", count, "passed the test with", node.g, "steps\n")
            display_path(maze_arr, node, count)
            pass
            # # get_shortestPath returns the shortest path of the node
            # output = get_shortestPath(node)
            # print("Maze",count, "was a success!")
            # output.reverse()
            # print(' '.join(str(x) for x in output), "\n")
