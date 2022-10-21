
from tkinter import *
import sys
import numpy as np
import time, threading


# Instatiating the matrix that will represent the maze
def alocate_map():
    
    map_colors = []
    map_colors_rows = []

    for i in range(ms):
        map_colors_rows = []
        for j in range(ms):
            map_colors_rows.append('')
        map_colors.append(map_colors_rows)

    return map_colors


# Reads the maze file in .txt format - 0 is for good paths, and 1 for walls
def read_maze_file(name_file):

    file = open(name_file,'r')
    list_rows = file.readlines()

    line_count = 0
    content_row = []
    for row in list_rows:
        for col in row:
            if col != ' ' and col != '\n':
                content_row.append(col)
        map_colors[line_count][:] = content_row
        content_row = []
        line_count += 1

    return map_colors


# Filling the maze
def populate_maze():

    for i in range(ms):
        for j in range(ms):
            if map_colors[i][j] == '2': # Beggining of the maze
                map_colors[i][j] = 'green'
                
                current_row = i # Setting the current row and column (at the beggining of the maze) - Initial position
                current_col = j

                list_possible_paths.append([i,j])
            
            elif map_colors[i][j] == '3': # Ending of the maze
                map_colors[i][j] = 'red'
            elif map_colors[i][j] == '0': # Walls
                map_colors[i][j] = 'grey'
            elif map_colors[i][j] == '1': # Free path
                map_colors[i][j] = 'white' 

    return map_colors,current_row,current_col


# Create a rectangle with draw function with determined color by the position of maze
def create():   
    for row in range(ms):
        for col in range(ms):
            color = map_colors[row][col]
            draw(row, col, color)

# Drawing the rectangle at the screen
def draw(row, col, color):
    
    x1 = col * cell_size
    y1 = row * cell_size
    x2 = x1 + cell_size
    y2 = y1 + cell_size

    ffs.create_rectangle(x1, y1, x2, y2, fill=color)

# Used to update the agent position after a move
def draw_rect(row,col):

    x1 = col*cell_size
    y1 = row*cell_size

    ffs.create_rectangle((x1, y1, x1 + cell_size, y1 + cell_size), fill="yellow") 

# Used to fill the place where the agent was before the move
def del_rect(row,col):

    x1 = col*cell_size
    y1 = row*cell_size
    
    if map_colors[row][col] != 'green':
        ffs.create_rectangle((x1, y1, x1 + cell_size, y1 + cell_size), fill="blue")


## ---------------------------------------------------- Resolution of the maze -------------------------------------------------- ##


def check_sucessor(current_row,current_col): # Verifying which places are free to the agent move

    list_directions = [0,0,0,0] # list of the possible directions (up, down, left, right)

    if current_col + 1 < ms:
        if map_colors[current_row][current_col+1] == 'white' or map_colors[current_row][current_col+1] == 'red': # moving to right
            list_directions[2] = 1 # right
    if current_col - 1 >= 0: 
        if map_colors[current_row][current_col-1] == 'white' or map_colors[current_row][current_col-1] == 'red': # moving to left
            list_directions[3] = 1 # left
    if current_row + 1 < ms: 
        if map_colors[current_row+1][current_col] == 'white' or map_colors[current_row+1][current_col] == 'red': # moving down
            list_directions[1] = 1 # down
    if current_row - 1 >= 0: 
        if map_colors[current_row-1][current_col] == 'white' or map_colors[current_row-1][current_col] == 'red': # moving up
            list_directions[0] = 1 # up

    return list_directions


def update_possible_paths(possible_paths,list_directions,current_row,current_col): # Update the list of possible paths

    for i in range(len(list_directions)):
        if i == 0: # up
            if list_directions[i] == 1 and [current_row-1,current_col] not in list_already_percurred and [current_row-1,current_col] not in possible_paths:
                possible_paths.append([current_row-1,current_col])
        if i == 1: # down
            if list_directions[i] == 1 and [current_row+1,current_col] not in list_already_percurred and [current_row+1,current_col] not in possible_paths:
                possible_paths.append([current_row+1,current_col])
        if i == 2: # right
            if list_directions[i] == 1 and [current_row,current_col+1] not in list_already_percurred and [current_row,current_col+1] not in possible_paths:
                possible_paths.append([current_row,current_col+1])
        if i == 3: # left
            if list_directions[i] == 1 and [current_row,current_col-1] not in list_already_percurred and [current_row,current_col-1] not in possible_paths:
                possible_paths.append([current_row,current_col-1])


def move(possible_paths,current_row,current_col): # Actually moves the agent around the maze

    if [current_row,current_col] not in list_already_percurred:
        list_already_percurred.append([current_row,current_col])
    
    del_rect(current_row,current_col)
 
    # BFS
    if len(possible_paths) > 0: # Removing position already percurred
        possible_paths.pop(0)

    if len(possible_paths) > 0: # getting the position from the first item of the list to move (FIFO principle)
        current_row = possible_paths[0][0]
        current_col = possible_paths[0][1]

    draw_rect(current_row,current_col)

    return current_row,current_col


def check_end(current_row,current_col): # Goal function

    if map_colors[current_row][current_col] == 'red': # If the position was number 3 (or has the color red) - end of the maze
        return True
    else:
        return False


def execute_solution_maze(map_colors,current_row,current_col): # Execution of the search by itself

    list_directions = check_sucessor(current_row,current_col)

    update_possible_paths(list_possible_paths,list_directions,current_row,current_col)
    current_row,current_col = move(list_possible_paths,current_row,current_col)
    end = check_end(current_row,current_col)

    print("Caminhos possiveis : ",list_possible_paths)
    print("Posicoes ja percorridas : ",list_already_percurred)
    print("end : ",end)
    print("-----------------")

    t = threading.Timer(1,execute_solution_maze,args=(map_colors,current_row,current_col))
    t.daemon = True
    t.start()

    if end == True:
        t.cancel()


def close(event): # It allows the user to close the window by pressing 'esc'
    sys.exit()


## ------------------------------------------------------------------------------------------------------------------------------ ##
## ------------------------------------------------- Beggining of code execution ------------------------------------------------ ##

cell_size = 50 # number of pixels per square
ms = 10 # maze size (number of rows and columns of the maze)

# Row and column where the agent is - The values will be initialized in populate maze function
current_row = -1
current_col = -1

## Generates graphical window
window = Tk()
window.title('Maze solution with BFS algorithm')
canvas_side = ms*cell_size
ffs = Canvas(window, width = canvas_side, height = canvas_side, bg = 'grey')
ffs.pack()

# Lists that indicates the path already percorred and the next
list_already_percurred = []
list_possible_paths = []

directory = './maze_samples/'
maze_file = directory + 'maze_1.txt'

if len(sys.argv) > 1: # If there is an argument from the command line
    maze_file = directory + sys.argv[1]

## Alocates, read the maze file and populate the maze with the colors relatives to the possibilities (White - Free pathe, Grey - Wall, Green - Start, Red - Ending)
map_colors = alocate_map()
map_colors = read_maze_file(maze_file)
map_colors,current_row,current_col = populate_maze()
create()

# Searches the end of the maze with the breadth first search 
execute_solution_maze(map_colors,current_row,current_col)

# It monitors the pressed keys by the user - close the screen when the user presses 'esc'
window.bind('<Escape>',close)

# Executing the graphical interface
window.mainloop()