##################################################################################################
#
#   A* Algorithm Implementation to find Shortest Path in a Randomly Generated Maze
#   Contributions: Nirjal Shakya, Kamontat Swasdikulavath, Sparsh Rawlani, Xavier Betancourt
#   Copyright @ Nirjal, Kamontat, Sparsh, Xavier in 12/15/2021 
#
##################################################################################################


from heapq import heappush, heappop
import pandas as pd


import time
#  Update: A* Algorithm Implemented
def inverse_num(x):
    if x == 1:
        return 0
    if x == 0:
        return 1
    else:
        print("wtf")



pandas_dataframe = {'x': [0], 'y': [0],'time':[0]}



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
    start_time = time.process_time()
    start_node = cell(start[0], start[1], 0, None)
    start_node.heuristics(goal)
    start_node.calc_f()

    # Initialize the open list & place the starting node in it
    open_list = [start_node]
    # Initialize the closed list
    closed_list = []

    # Initializing dictionaries to keep track of the opened/closed nodes
    open_track_dict = {f"{start[0]} {start[1]}": open_list[0]}
    closed_track_dict = {}
    final_count = 0
    # loop while the open_list is not empty
    while open_list:
        # sort the open_list based on the least score for each node
        # the nearest node will be at position [0]
        # open_list = sorted(open_list, key=lambda x: x.f)  # sort by f
        # q = open_list.pop(0)  # take out the one with lowest f
        q = heappop(open_list)
        final_count +=1
        # print(f"Searching at pint i:{q.x} j:{q.y}")
        x, y, g = q.x, q.y, q.g
        # open_track_dict.pop(f"{x} {y}")  # delete from the dict
        # checks if x is closer to the wall (the boundary or if the node is a wall)
        # this particularly checks for the maze wall above the current position
        if x < n - 1 and maze_arr[x + 1][y] != 1:
            new_up = cell(x + 1, y, g + 1, q)
            new_up.heuristics(goal)  # give us new_up.h
            new_up.calc_f()  # give us new_up.f

            # checks if the neighbor the exit point
            #   if true, it prints that it found the answer
            if new_up.x == goal[0] and new_up.y == goal[1]:
                pandas_dataframe['x'].append(len(maze_arr))
                pandas_dataframe['y'].append(final_count)
                end_time = time.process_time()
                pandas_dataframe['time'].append(end_time-start_time)
                return new_up
            # If the successor has more score than equivalent in open list, skip
            elif (
                f"{new_up.x} {new_up.y}" in open_track_dict
                and new_up.f > open_track_dict[f"{new_up.x} {new_up.y}"].f
            ):
                pass
            # If the successor has more score than equivalent in closed list, skip
            elif (
                f"{new_up.x} {new_up.y}" in closed_track_dict
                and new_up.f > closed_track_dict[f"{new_up.x} {new_up.y}"].f
            ):
                pass
            else:
                open_track_dict[f"{new_up.x} {new_up.y}"] = new_up
                heappush(open_list, new_up)
                # open_list.append(new_up)

        if y < n - 1 and maze_arr[x][y + 1] != 1:
            new_right = cell(x, y + 1, g + 1, q)
            new_right.heuristics(goal)  # give us new_up.h
            new_right.calc_f()  # give us new_up.f

            # checks if the neighbor the exit point
            #   if true, it prints that it found the answer
            if new_right.x == goal[0] and new_right.y == goal[1]:
                pandas_dataframe['x'].append(len(maze_arr))
                pandas_dataframe['y'].append(final_count)
                end_time = time.process_time()
                pandas_dataframe['time'].append(end_time-start_time)
                return new_right
            # If the successor has more score than equivalent in open list, skip
            elif (
                f"{new_right.x} {new_right.y}" in open_track_dict
                and new_right.f > open_track_dict[f"{new_right.x} {new_right.y}"].f
            ):
                pass
            # If the successor has more score than equivalent in closed list, skip
            elif (
                f"{new_right.x} {new_right.y}" in closed_track_dict
                and new_right.f > closed_track_dict[f"{new_right.x} {new_right.y}"].f
            ):
                pass
            else:
                open_track_dict[f"{new_right.x} {new_right.y}"] = new_right
                # open_list.append(new_right)
                heappush(open_list, new_right)

        if x > 0 and maze_arr[x - 1][y] != 1:
            new_down = cell(x - 1, y, g + 1, q)
            new_down.heuristics(goal)  # give us new_up.h
            new_down.calc_f()  # give us new_up.f

            # checks if x is closer to the wall (the boundary or if the node is a wall)
            # this particularly checks for the maze wall above the current position
            if new_down.x == goal[0] and new_down.y == goal[1]:
                pandas_dataframe['x'].append(len(maze_arr))
                pandas_dataframe['y'].append(final_count)
                end_time = time.process_time()
                pandas_dataframe['time'].append(end_time-start_time)
                return new_down
            # If the successor has more score than equivalent in open list, skip
            elif (
                f"{new_down.x} {new_down.y}" in open_track_dict
                and new_down.f > open_track_dict[f"{new_down.x} {new_down.y}"].f
            ):
                pass
            # If the successor has more score than equivalent in closed list, skip
            elif (
                f"{new_down.x} {new_down.y}" in closed_track_dict
                and new_down.f > closed_track_dict[f"{new_down.x} {new_down.y}"].f
            ):
                pass
            else:
                open_track_dict[f"{new_down.x} {new_down.y}"] = new_down
                # open_list.append(new_down)
                heappush(open_list, new_down)

        if y > 0 and maze_arr[x][y - 1] != 1:
            new_left = cell(x, y - 1, g + 1, q)
            new_left.heuristics(goal)  # give us new_up.h
            new_left.calc_f()  # give us new_up.f

            # checks if x is closer to the wall (the boundary or if the node is a wall)
            # this particularly checks for the maze wall above the current position
            if new_left.x == goal[0] and new_left.y == goal[1]:
                pandas_dataframe['x'].append(len(maze_arr))
                pandas_dataframe['y'].append(final_count)
                end_time = time.process_time()
                pandas_dataframe['time'].append(end_time-start_time)
                return new_left

            # If the successor has more score than equivalent in open list, skip
            elif (
                f"{new_left.x} {new_left.y}" in open_track_dict
                and new_left.f > open_track_dict[f"{new_left.x} {new_left.y}"].f
            ):
                pass
            # If the successor has more score than equivalent in closed list, skip
            elif (
                f"{new_left.x} {new_left.y}" in closed_track_dict
                and new_left.f > closed_track_dict[f"{new_left.x} {new_left.y}"].f
            ):
                pass
            else:
                open_track_dict[f"{new_left.x} {new_left.y}"] = new_left
                # open_list.append(new_left)
                heappush(open_list, new_left)

        # After we are done with checking all the possible neighbors for the node,
        # We put it in the closed_list
        closed_list.append(q)
        closed_track_dict[f"{q.x} {q.y}"] = q


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
    with open("output.txt", "a") as o:
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
    pandas_dataframe = pd.DataFrame(data=pandas_dataframe)
    pandas_dataframe.to_csv('csv_test.csv',index=False,columns = ['x','y','time'])