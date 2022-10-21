# Breadth-First Search Maze Solution

This code demonstrates the breadth-first search method implementation in a
maze environment, of 10 x 10 regions (squares of 50 pixels each). It has as functions the graphical display 
of the items (GUI made using TKinter), in addition to the following methods:
successor from current position in maze, agent position update, arrival check
to the objective, and the search method itself, which uses these previous functions in its execution.

As for the graph, the green squares represent the beginning of the maze (number 2), the colored red squares
represent the end (number 3), the white ones represent the free paths (number 1) and the
gray color represent the walls (number 0). The paths taken are indicated by the blue color on the interface,
and the agent's current position is in yellow.

The mazes are displayed from text files with their configuration, with the numbers of each line and
column indicating whether that position is a free space, a wall, start or end. This text file must be passed
as a parameter to the script, and a text file is defined by default in the code (maze_1.txt). At the end of execution,
pressing the 'esc' key closes the graphic window and the program is terminated.

# Instructions to run the script:

To run the application, do the following steps:

1) Access the directory where the maze files you want to run (.txt) and the Python script are located through the terminal.
2) Run the following command: python maze_solution_bfs.py file_name_maze.txt

** Where file_name_maze.txt is the name of the text file containing the data about the maze (in the sent folder, there are already 4 files of this type for testing)
