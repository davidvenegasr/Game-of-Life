################################################################################################
# Conway's  Game of Life - Using python3 standard library and Numpy
#
# Rules:
# 1-Any live cell with two or three neighbors survives.
# 2-Any dead cell with three live neighbors becomes a live cell.
# 3-All other live cells die in the next generation. Similarly, all other dead cells stay dead.
#
# Author: David Venegas - Email: venegasr.david@gmail.com  
################################################################################################

import tkinter as tk
import numpy as np
from random import randint

class Cells: 

    def __init__(self, arraySize):

        """Se inicializa la matrix cuyos elementos son celulas vivas o muertas al azar"""

        self.cells = np.array([[randint(0, 1) for x in range(arraySize)] for y in range(arraySize)])
        self.size = arraySize

    def get_array(self):
        
        return self.cells  
    
    #Used for testing
    def kill_cells(self): 
        
        """Sets all cells to zero"""
        
        self.cells = np.zeros(self.cells.shape, dtype=int)

    #Used for testing, could be improved inthe future to start with a specific pattern
    def choose_cells(self, matrix):

        """Sets cells to a specific array"""

        self.cells = np.array(matrix)

    def live_or_die(self):
        
        """Conway's Game Rules are applied to check if a cell lives or dies"""

        #    cell        adj_sum     cell
        #    ---------   --------    -----------------
        # 1. live        2           lives
        # 2. live/dead   3           lives
        # 3. Otherwise   x           dies

        adj_cells = self.calculate_adj_sum()

        # Alive if it was alive and has 2 neighbors or alive if it has 3 neighbors
        self.cells = ((self.cells == 1) & (adj_cells == 2) | (adj_cells == 3))

    def calculate_adj_sum(self):
        # Here we take advantage of numpy vectorization 
        # This is way much faster than a for cycle
        
        adj_cells = np.zeros(self.cells.shape, dtype=int)
        adj_cells[1:] += self.cells[:-1]  # North
        adj_cells[:-1] += self.cells[1:]  # South
        adj_cells[:,1:] += self.cells[:,:-1]  # West
        adj_cells[:,:-1] += self.cells[:,1:]  # East
        adj_cells[1:,1:] += self.cells[:-1,:-1]  # NW
        adj_cells[1:,:-1] += self.cells[:-1,1:]   # NE
        adj_cells[:-1,1:] += self.cells[1:,:-1]  # SW
        adj_cells[:-1,:-1] += self.cells[1:,1:]  # SE
        
        return adj_cells


class Game():

    def __init__(self, length = 80, cell_size=8, timelapse = 400, dead_color='black', alive_color ='yellow', grid_color = 'black'):
        
        """
        Initializes the game with the lenght of each row for the grid, the size of each cell for the GUI,
        the refresh time, and the color or the grid and cells (alive or dead).
        """
        
        self.cells = Cells(length)
        self.window = tk.Tk()
        self.window.title('Conway\'s Game of Life')
        self.size = length* cell_size
        self.cell_size = cell_size
        self.canvas = tk.Canvas(self.window, bg="black", height=self.size, width=self.size)  
        self.canvas.pack()
        
        self.rectangles = {}

        #Rectangles are created and stored so it's faster to change the item color later
        for x in range(length):
            for y in range(length):
                self.rectangles[(x,y)] = self.canvas.create_rectangle(self.cell_size * x, self.cell_size * y, \
                                                                self.cell_size * x + self.cell_size, self.cell_size * y + self.cell_size, outline='gray', fill='black')

        self.coordinates = list(self.rectangles.keys())
        self.window.after(200, self.update_cells, timelapse, dead_color, alive_color, grid_color)
        self.window.mainloop()

    def update_cells(self, timelapse, dead_color, alive_color, grid_color):

        """Updates the cell array and renders new colors for each cell according to their new state"""

        for x, y in self.coordinates:
                if self.cells.get_array()[x][y]==1:
                    self.canvas.itemconfigure(self.rectangles[(x,y)], outline= grid_color, fill=alive_color)
                else:
                    self.canvas.itemconfigure(self.rectangles[(x,y)], outline= grid_color, fill=dead_color)
        
        self.cells.live_or_die()
        self.window.after(timelapse, self.update_cells, timelapse, dead_color, alive_color, grid_color)

if __name__ == '__main__':
    
    game = Game()