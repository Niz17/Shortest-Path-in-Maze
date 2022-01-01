#  Update: A* Algorithm Implemented
#   We are yet to trace the shortest path back from the start to the end point
import copy
import numpy
from heapq import heappush, heappop

def inverse_num(x):
    if x==1:
        return 0
    if x ==0:
        return 1
    else:
        print("...")
# Creating the maze
# Referenced in the main()
def take_maze(data_lines):
    maze = []
    size = int(data_lines[0])
    for x in range(1, size + 1):
        maze.append(list(map(int, data_lines[x].split())))
    del data_lines[0 : size + 2]
    for i in range(len(maze)):
        maze[i] = list(map(inverse_num,maze[i]))
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
    def __init__(self,x,y,g,parent,maze) -> None:
        self.x = x
        self.y = y
        self.g = g
        self.parent = parent
        self.h = -11111
        self.f = -11111
        self.maze = maze

    # Calculates the heuristics value for each node based on an attributed goal 
    #   referenced from https://www.geeksforgeeks.org/a-search-algorithm/
    def heuristics(self,goal):
        self.h = abs(self.x - goal[0]) + abs(self.y - goal[1])

    # Calculates the f (score) value based on the value of g & h of node
    #   => this is the considered score before we move through the maze, 
    #      the lesser the score the closer the next node is to the exit. 
    def calc_f(self):
        self.f = self.h + self.g
        return self.f
    def __lt__(self, other):
        return self.f < other.f

def maze_update(maze):
    new_maze = copy.deepcopy(maze)
    for x in new_maze:
        temp = x.pop(0)
        x.append(temp)
    return new_maze

# Implementation of A* algorithm
def start_astar_move(maze_arr,start,goal,n):
    # initialize the starting node (which is at )
    start_node = cell(start[0],start[1],0,None,maze_arr)
    start_node.heuristics(goal)
    start_node.calc_f()

    # Initialize the open list & place the starting node in it
    open_list = [start_node]
    # Initialize the closed list
    closed_list = []

    # Initializing dictionaries to keep track of the opened/closed nodes
    open_track_dict = {f"{start[0]} {start[1]}":open_list[0]}
    closed_track_dict = {}
    # loop while the open_list is not empty 
    while open_list:
        successed = False
        q = heappop(open_list)
        x, y, g = q.x,q.y,q.g  
        update_closed_track = True
        maze_arr = q.maze
        if x < n-1 and q.maze[x+1][y] != 1:
            new_up = cell(x + 1, y,g+1, q, maze_update(maze_arr)) 
            new_up.heuristics(goal) # give us new_up.h
            new_up.calc_f() # give us new_up.f
            successed = True

            # checks if the neighbor the exit point
            #   if true, it prints that it found the answer
            if new_up.x == goal[0] and new_up.y == goal[1]:
                return [True, new_up]
            # If the successor has more score than equivalent in open list, skip
            elif f"{new_up.x} {new_up.y}" in open_track_dict and new_up.f > open_track_dict[f"{new_up.x} {new_up.y}"].f:
                pass
            # If the successor has more score than equivalent in closed list, skip
            elif f"{new_up.x} {new_up.y}" in closed_track_dict and new_up.f > closed_track_dict[f"{new_up.x} {new_up.y}"].f:
                successed = False
                pass
            else:
                open_track_dict[f"{new_up.x} {new_up.y}"] = new_up
                heappush(open_list, new_up)

        if x > 0 and q.maze[x-1][y] != 1:
            new_down = cell(x - 1, y,g+1, q, maze_update(maze_arr))
            new_down.heuristics(goal) # give us new_up.h
            new_down.calc_f() # give us new_up.f
            successed = True
            if new_down.x == goal[0] and new_down.y == goal[1]:
                return [True, new_down]
            # If the successor has more score than equivalent in open list, skip
            elif f"{new_down.x} {new_down.y}" in open_track_dict and new_down.f > open_track_dict[f"{new_down.x} {new_down.y}"].f:
                pass
            # If the successor has more score than equivalent in closed list, skip
            elif f"{new_down.x} {new_down.y}" in closed_track_dict and new_down.f > closed_track_dict[f"{new_down.x} {new_down.y}"].f:
                successed = False
                pass
            else:
                open_track_dict[f"{new_down.x} {new_down.y}"] = new_down
                heappush(open_list, new_down)

        
        if y<n-1 and q.maze[x][y+1] != 1 :
            new_right = cell(x, y+1, g+1,q, maze_update(maze_arr))
            new_right.heuristics(goal) # give us new_up.h
            new_right.calc_f() # give us new_up.f
            successed = True

            # checks if the neighbor the exit point
            #   if true, it prints that it found the answer
            if new_right.x == goal[0] and new_right.y == goal[1]:
                return [True, new_right]
            # If the successor has more score than equivalent in open list, skip
            elif f"{new_right.x} {new_right.y}" in open_track_dict and new_right.f > open_track_dict[f"{new_right.x} {new_right.y}"].f:
                pass
            # If the successor has more score than equivalent in closed list, skip
            elif f"{new_right.x} {new_right.y}" in closed_track_dict and new_right.f > closed_track_dict[f"{new_right.x} {new_right.y}"].f:
                successed = False
                pass
            else:
                open_track_dict[f"{new_right.x} {new_right.y}"] = new_right
                heappush(open_list, new_right)


        if y>0 and q.maze[x][y-1] != 1:
            new_left = cell(x, y-1,g+1, q, maze_update(maze_arr))
            new_left.heuristics(goal) # give us new_up.h
            new_left.calc_f() # give us new_up.f
            successed = True

            # checks if x is closer to the wall (the boundary or if the node is a wall)
            # this particularly checks for the maze wall above the current position
            if new_left.x == goal[0] and new_left.y == goal[1]:
                print("We Found The Answer!")
                return [True, new_left]
            # If the successor has more score than equivalent in open list, skip
            elif f"{new_left.x} {new_left.y}" in open_track_dict and new_left.f > open_track_dict[f"{new_left.x} {new_left.y}"].f:
                pass
            # If the successor has more score than equivalent in closed list, skip
            elif f"{new_left.x} {new_left.y}" in closed_track_dict and new_left.f > closed_track_dict[f"{new_left.x} {new_left.y}"].f:
                successed = False
                pass
            else:
                open_track_dict[f"{new_left.x} {new_left.y}"] = new_left
                heappush(open_list, new_left)
        
        if successed == False:
            new_q = cell(x, y,g+1, q, maze_update(maze_arr)) 
            open_track_dict[f"{x} {y}"] = new_q 
            heappush(open_list, new_q)


        # path_s(q.maze,q,1)
        # After we are done with checking all the possible neighbors for the node, 
        # We put it in the closed_list
        if successed == True:
            closed_list.append(q)
            closed_track_dict[f"{q.x} {q.y}"] = q

    return [False, closed_list]


def display(new_path_maze, count):
    with open('outputmove.txt','a') as o:
        # o.write("Maze "  + str(count) + " succeeded in finding a way out \n")
        # o.write("Displaying Maze: "  + str(count) + "\n")
        for x in new_path_maze:
            o.write('\t'.join(map(str,x)))
            o.write('\n')
        o.write('\n')

# Setting up the path based on if the maze was successful
def path_s(new_path_maze, k,count):
    num = 0
    while k.parent != None:
        new_path_maze[k.x][k.y] = "[o]"
        num += 1
        k = k.parent
    new_path_maze[k.x][k.y] = "[o]"
    display(new_path_maze, count)

# Setting up the path based on if the maze failed
def path_f(new_path_maze, path_arr,count):
    for x in path_arr:
        new_path_maze[x.x][x.y] = "[x]"
    display(new_path_maze, count)

def print_path(node):
    maze = ''
    while node is not None:
        maze_array = node.maze
        maze_array[node.x][node.y] = "[o]"
        for i in range(len(maze_array)):
            maze += '\t'.join(list(map(str,node.maze[i])))
            maze += '\n'
        maze += '\n'
        node = node.parent
    maze = maze.split('\n\n')
    maze = maze[::-1]
    maze = '\n\n'.join(maze)
    maze += '\n\n'
    with open('outputmove.txt','a') as o:
        o.write(maze)


if __name__ == "__main__":
    # Open the maze document
    with open("newMazes.txt",'r') as data:
        h = data.read()
    new_data = h.split('\n')
    # array that stores the maze 
    maze_arr = []
    # initializing the start node - which is 0,0 in this case.
    start = [0,0,None]
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
        # initializes the goal of the maze - which is at the bottom right element
        goal = [n-1,n-1]
        # start the A* algorithm
        # returns a boolean value for success and a node
        #   if it succeeded, then it returns True and the final node
        #   if it failed, then it returns False and the last node it could access
        success, node = start_astar_move(maze_arr,start,goal,n)
        # increment count (each iterated node)
        count += 1
        with open('outputmove.txt','a') as o:
            o.write(f"Current Maze: {count}\n")
        if success:
            print_path(node)
        else:
            # print_path(node)
            path_f(maze_arr,node,count)
 
