using System;
using System.Linq;
using System.Collections.Generic;
using System.IO;
using System.Text;
/*
* ADVANCED ALGORITHMS - FINAL PROJECT - Whitworth University
* Collaborators: Sparsh Rawlani, Nirjal Shakya, Kamontat Swasdikulavath, Xavier Betancourt
* Instructor: Dr. Kent Jones
* Date: December 16, 2021
*/
namespace MazeGenerator
{
    // Represent a node in the grid with x and y directions to move to
    public class Node
    {
        public int xDirection;
        public int yDirection;
        
        public Node(int x, int y)
        {
            this.xDirection = x;
            this.yDirection = y;
        }
    }

    // Perform all logical operations to generate a 2D maze of ones and zeros using a DFS search approach. Incrementing this way
    // the likelihood of getting mazes with open paths for a solution
    public class MazeGenerator
    {
        public int dimension; // an int dimension that will hold the dimension (x*x) of the maze
        public Stack<Node> helperStack = new Stack<Node>();// a stack of Nodes to push and pop from
        public Random rand = new Random();// a random variable that will generate the random maze
        public int[,] mazeSolution;// an array to hold the 0s and 1s seprated by a comma

        // Initialize a maze solution
        // Input: dimensions of the nxn matrix
        public MazeGenerator(int dimension)
        {
            this.dimension = dimension;
            this.mazeSolution = new int[dimension, dimension];// this is how the solution will appear with 0's and 1's
        }

        /// <summary>
        /// function to generate the maze with a default position for the starting node
        /// </summary>
        public void generateMaze()
        {
            this.helperStack.Push(new Node(0, 0));// begin with pushing the new node to the stack
            while(this.helperStack.Count != 0)// until we reach the end of the stack
            {
                Node next = this.helperStack.Pop();// store the popped node
                if (validNextNode(next))
                {
                    mazeSolution[next.yDirection, next.xDirection] = 1;// store the solution with x's and y's
                    List<Node> neighbors = findNeighbors(next);// create a new list to store the neighboring nodes and used the popped node to find the neighbors
                    addNodesToStack(neighbors);// add neighbors to the stack
                }
            }
        }   

        /// <summary>
        /// boolean function to check the neighboring node
        /// return true if the next node is valid, otherwise returns false
        /// </summary>
        /// <param name="node"></param>
        /// <returns></returns>
        public bool validNextNode(Node node)
        {
            int numNeighborOnes = 0;// an int to store the number of 1's around the neighboring node
            for(int y = node.yDirection - 1; y < node.yDirection + 2; y++)
            {
                for(int x = node.xDirection - 1; x < node.xDirection + 2; x++)
                {
                    // if the neighboring node is not in the way, push 1 to the solution array
                    if(pointIsOnGrid(x,y) && pointIsNotNode(node, x, y) && this.mazeSolution[y, x] == 1)
                    {
                        numNeighborOnes++;
                    }
                }
            }
            return (numNeighborOnes < 3) && this.mazeSolution[node.yDirection, node.xDirection] != 1; // make sure there's a path next to this node
        }
        
        /// <summary>
        /// function to add new nodes to the stack
        /// </summary>
        /// <param name="nodes"></param>
        public void addNodesToStack(List<Node> nodes)
        {
            int target;// an int to store the number for the desired maze: rand in this case
            while(nodes.Count != 0)
            {
                target = rand.Next(nodes.Count);// set the target
                var toBeRemoved = nodes.ElementAt(target); //another variable to store the element of the node that needs to be popped 
                helperStack.Push(toBeRemoved);// add the node to stack
                nodes.RemoveAt(target);  // remove the targeted node           
            }
        }

        /// <summary>
        /// function to find the neighbor of the node in the maze
        /// returns a list of neighboring nodes
        /// </summary>
        /// <param name="node"></param>
        /// <returns></returns>
        public List<Node> findNeighbors(Node node)
        {
            List<Node> neighbors = new List<Node>();// a new list of nodes to be returned from the function
            for(int y = node.yDirection - 1; y < node.yDirection + 2; y++)
            {
                for(int x = node.xDirection - 1; x < node.xDirection + 2; x++)
                {
                    // if the neighbor is found
                    if(pointIsOnGrid(x, y) && pointIsNotCorner(node, x, y) && pointIsNotNode(node, x, y))
                    {
                        neighbors.Add(new Node(x, y)); // add the new node to the list
                    }
                }
            }
            return neighbors; // return the new list
        }

        // Check a specified point is inside the boundaries of the grid (greater than zero and less than the dimensions of the matrix)
        public bool pointIsOnGrid(int x, int y)
        {
            //returns true is point is on the maze, otherwise resturn false
            return (x >= 0 && y >= 0 && x < this.dimension && y < this.dimension);
        }

        // Check a specified point is not a corner in the grid
        // Input: grid node, x direction, and y direction
        public bool pointIsNotCorner(Node node, int x, int y)
        {
            // return true if the point is in the corner of the maze, otherise returns false
            return (x == node.xDirection || y == node.yDirection);
        }

        /// <summary>
        /// returns true if a point a not a node, otherwise returns false
        /// </summary>
        /// <param name="node"></param>
        /// <param name="x"></param>
        /// <param name="y"></param>
        /// <returns></returns>
        public bool pointIsNotNode(Node node, int x, int y)
        {
            return !(x == node.xDirection && y == node.yDirection);
        }

        /// <summary>
        /// function to put the maze in a form a string and print it to a text file, so that it can be used as an input to the A* star algorithm
        /// </summary>
        /// <param name="dimension"></param>
        /// <returns></returns>
        public string getStringMaze(int dimension)
        {
            // a c# method used to create strings
            StringBuilder sb = new StringBuilder();
            sb.Append(dimension + "\n");

            for (int i = 0; i < this.mazeSolution.GetLength(0); i++) // Iterate throught the 2D maze row by row and append to the string 
            {             
                for(int j = 0; j < this.mazeSolution.GetLength(1); j++)
                {
                    sb.Append(this.mazeSolution[i, j].ToString() + " ");
                }
                sb.Append("\n");
            }
            return sb.ToString();
            // return the maze in the form of a string
        }
    }

    /// <summary>
    /// a class that holds a method for the file handlers
    /// </summary>
    public class FileHandler
    {
        public string filePath;
        public FileHandler(string filePath)
        {
            this.filePath = filePath;
        }
    }

    /// <summary>
    /// class Fileoutput: outputs data to a text file
    /// </summary>
    public class FileOutput
    {
        public FileHandler file;
        public string maze;
        public FileOutput(FileHandler file, string maze)
        {
            this.file = file;
            this.maze = maze;
        }

        /// <summary>
        /// method that uses the filepath from the constructor and appends all text to the text file
        /// </summary>
        public void WriteToFile()
        {          
            File.AppendAllText(this.file.filePath, this.maze + "\n");         
        }
    }

    /// <summary>
    /// class for the main function
    /// </summary>
    class Program
    {
        static void Main(string[] args)
        {
            // Set up your current file directory here
            FileHandler file = new FileHandler(@"C:\Users\xavi9\OneDrive\Documentos\SENIOR\Algorithms\Final_Project_Elm\newMazes.txt");

            //  setting up the number for the number of mazes
            const int NumOfMazes = 400;
            var randNumGenerator = new Random();     
            int mazeDimension = 2; // an int to store the dimensions of the maze
            MazeGenerator maze;  // object for class maze         
            string stringMaze; // output string to store the maze output
            FileOutput outputFile; // object for the output File class
            int counter = 1;

            // loop to generate the mazes
            for(int i = 0;  i < NumOfMazes; i++)
            {
                maze = new MazeGenerator(mazeDimension);
                maze.generateMaze();
                stringMaze = maze.getStringMaze(mazeDimension);              
                outputFile = new FileOutput(file, stringMaze); // printint the string to the output file
                outputFile.WriteToFile();
                counter++;
                if(counter == 5)
                {
                    mazeDimension++;
                    counter = 1;
                }
            }           
        }
    }
}
