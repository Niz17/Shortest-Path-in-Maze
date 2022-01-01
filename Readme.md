# Final Project
Class: CS 473 - Advanced Algorithms 
Last Modified: 12/18/2021
Colloborator: Sparsh Rawlani, Xavier Betancourt, Nirjal Shakya, Kamontat Swasdikulavath


## A* Maze Search Algorithm

### What is A* and how it works
As group Elm, we implemented the A* search algorithm that smartly finds the path through a maze full of blockers. Let's consider a maze of n*n dimensions, and the algorithm targets to find the shortest path from any random point A to point B in the maze. The reason behind using this algorithm over other traversal algorithms such as DFS or BFS is the optimality and efficiency of this algorithms over the othe ones. 

At each iteration of its loop, A* works to determine in which direction to extend. In our version of A* algorithm, **it can either extend horizontally or vertically** which is slighly different than the traditional version of A* which can also extend diagnally when searching for the shortest path. The way in which this algorithms computes the shortest distance is given by:
                f(n) = g(n) + h(n)
where n is the next node on the path, g(n) is the cost of the path from the start node to n, and h(n) estimates the cost of the cheapest path fron n to the goal point. 
Similarly, our algorithm used the same approach and finds the shortest path in the randomly generated maze. 


### How to Run the Program
To be able to generate mazes to be used as input for the program, it is necessary to run the code from "MazeGenerator", which was implemented separately using C#
as the main language for generation. A recomendation is to use Visual Studio and run the program from there. Within MazeGenerator, the user can specify the number of mazes to be generated as well as the file directory to write to. Once these are specified, run the program (F5) and it will write to a text file "mazes.txt" which will be used as input for the A* algorithm. NOTE: The MazeGenerator appends new mazes to the existent ones, if user wants to start fresh, it would be a good idea to delete the contents of the mazes.txt file first.

First, run C# code in visual studio to generate mazes.txt

Place mazes.txt in root folder

run 
```python
python alphastar.py
```


For BFS example
```
python "BFS counterpart.py"
```

### Assumptions
Inputs is 1 and 0s in mazes. 1 is a path, 0 is a wall

Output is also 1 and 0, but 1 is a wall, and 0 is a path.

### Description of code
Maze Generator
The maze generation and file handling process is composed of four important classes. For the maze generation itself, two classes are needed:
1) Node Class
   - In this class, the x and y directions are stored to be able to populates nodes in the maze
2) Maze Generator Class
   - This class drives the actual implementation of the algorithm to generate mazes with correct solutions or open paths. 
   - Within this class, key variables are: 'dimension' and a 2D array 'mazeSolution' that are used to build up a maze. Key methods are 'pointIsNotNode',    'pointIsNotCorner', 'pointIsOnGrid' which are constantly used to make sure the posible nodes to be added are within the boundaries of the maze and comply with the     rules to make an effective maze solution. 
   - The methods 'findNeighbors', 'addNodesToStack', and 'validNextNode' use the methods described above to validate the nodes being added respect boundaries and offer a correct solution.
   - Lastly, the method 'getStringMaze' uses a StringBuilder object to transform the mazeSolution 2D array into a string that can be used for the file handler to write to a file.
For File Handling, another two classes are needed:
3) File Handler Class
   - This class sets up the file path specified from the user, here the user specifies where the 'mazes.txt' file is located locally.
4) File Output Class
   - This class stores a File Handler object that has the file path to the 'maze.txt' file, as well as the maze converted to a string from the Maze Generator class.
   - Within this class is the method 'WriteToFile' that will append text to the 'maze.txt' file using the path and the string maze.
(include screenshots)


The heuristic function is correct and not useless.


### Description of code

1. Initialize Open list (priority queue sorted by f score)
2. Initialize closed list
3. Put the starting node in open list
4. While Open list not empty
    1. pop out data of node with least score
    2. create 4 successsors (up, down, left, right)
    3. If successor is at goal, return answer node.
    4. If successor is already exists in open list or closed list, skip them.
    5. Else, check if successor is valid, calculate their heruestic score and step score, and add them up to give the cell the f score
    6. Add the node to closed list
5. If answer is returned, use its parent to slowly skip back to beginning
    Else, say there is no answer.



## Screenshots of solved maze
### Unsolved (1) is path (0) is a wall
![alt text](initialmaze.PNG)
### Solved (0) is path (1) is a wall
![alt text](Solved.PNG)


## Analysis
The time complexity is O(n^2) at worst according to Geek for Geeks. This is understandable due to the fact that, in worst case, the worst time complexity will be the same as a normal BFS. It simply depends on the effectiveness of the heuristic function and the maze's outlook. There is no clear "benchmark" for us to set and compare. However we can see that it is somewhat exponential given enough datapoints: illustrated below.

We graph out the output of the size of graph and its time and # of steps it took to traverse through: (4 datapoint for each size)

![alt text](nodewalked.PNG)

![alt text](time.PNG)


### Works Cited
AlgoExpert. (2021). A* Algorithm. Retrieved from AlgoExpert: https://www.algoexpert.io/questions/A*%20Algorithm

https://www.geeksforgeeks.org/a-search-algorithm/
