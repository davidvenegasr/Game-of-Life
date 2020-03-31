################################################################################################
# Conway's  Game of Life - Test Suites 
#
# Rules:
# 1-Any live cell with two or three neighbors survives.
# 2-Any dead cell with three live neighbors becomes a live cell.
# 3-All other live cells die in the next generation. Similarly, all other dead cells stay dead.
#
# Author: David Venegas - Email: venegasr.david@gmail.com  
################################################################################################

import unittest
import numpy as np
from gol import Cells, Game

class TestGameOfLife(unittest.TestCase):
    
    def test_choose_cells(self):
        
        colony = Cells(0)
        colony.choose_cells([[0,0,0],[0,1,0],[0,0,0]])
        expected = np.array([[0,0,0],[0,1,0],[0,0,0]])
        actual = colony.cells
        self.assertTrue((expected == actual).all())

    def test_get_array(self):

        colony = Cells(0)
        colony.choose_cells([[0,0,0],[0,1,0],[0,0,0]])
        expected = np.array([[0,0,0],[0,1,0],[0,0,0]])
        actual = colony.get_array()
        self.assertTrue((expected == actual).all())

    def test_kill_cells(self):

        colony = Cells(0)
        colony.choose_cells([[0,0,0],[0,1,0],[0,0,0]])
        colony.kill_cells()
        expected = np.array([[0,0,0],[0,0,0],[0,0,0]])
        actual = colony.get_array()
        self.assertTrue((expected == actual).all())

    def test_cell_size(self):
        
        colony = Cells(50)
        expected = 50
        actual = colony.get_array().shape[0]
        self.assertEqual(expected, actual)
    
    def test_adj_sum(self):

        colony = Cells(0)
        colony.choose_cells([[0,0,0],[0,1,0],[0,0,0]])
        expected = np.array([[1,1,1],[1,0,1],[1,1,1]])
        actual = colony.calculate_adj_sum()
        self.assertTrue((expected == actual).all())

        colony.choose_cells([[1,1,1],[1,1,1],[1,1,1]])
        expected = np.array([[3,5,3],[5,8,5],[3,5,3]])
        actual = colony.calculate_adj_sum()
        self.assertTrue((expected == actual).all())

        colony.choose_cells([[1,0,0,1],[0,1,1,0],[0,1,1,0],[1,0,0,1]])
        expected = np.array([[1,3,3,1],[3,4,4,3],[3,4,4,3],[1,3,3,1]])
        actual = colony.calculate_adj_sum()
        self.assertTrue((expected == actual).all())
    
    #live_or_die function
    def test_update_cells_basic(self):

        colony = Cells(50)
        colony.kill_cells()
        expected = np.zeros((50,50))
        colony.live_or_die()
        actual = colony.get_array()
        self.assertTrue((expected == actual).all())

        colony.choose_cells([[1,1],[0,0]])
        colony.live_or_die()
        actual = colony.get_array()
        expected = np.array([[0,0],[0,0]])
        self.assertTrue((expected == actual).all())

        colony.choose_cells([[1,1,1],[1,1,1],[1,1,1]])
        colony.live_or_die()
        actual = colony.get_array()
        expected = np.array([[1,0,1],[0,0,0],[1,0,1]])
        self.assertTrue((expected == actual).all())

    #perpetual
    def test_update_cells_square(self):

        colony = Cells(50)
        colony.choose_cells([[1,0,0,1],[0,1,1,0],[0,1,1,0],[1,0,0,1]])
        colony.live_or_die()
        actual = colony.get_array()
        expected = np.array([[0,1,1,0],[1,0,0,1],[1,0,0,1],[0,1,1,0]])
        self.assertTrue((expected == actual).all())

        colony.live_or_die()
        self.assertTrue((expected == actual).all())
        colony.live_or_die()
        self.assertTrue((expected == actual).all())
        colony.live_or_die()
        self.assertTrue((expected == actual).all())

    #loop rotation stick
    def test_update_cells_line(self):

        colony = Cells(50)    
        colony.choose_cells([[0,1,0],[0,1,0],[0,1,0]])
        expected = np.array([[0,0,0],[1,1,1],[0,0,0]])
        colony.live_or_die()
        actual = colony.get_array()
        self.assertTrue((expected == actual).all())

        colony.live_or_die()
        expected = np.array([[0,1,0],[0,1,0],[0,1,0]])
        actual = colony.get_array()
        self.assertTrue((expected == actual).all())

    #edge cases 
    def test_update_cells_edge_cases(self):
        colony = Cells(50)    
        colony.choose_cells([[1,1,1],[1,0,1],[1,1,1]])
        colony.live_or_die()
        expected = np.array([[1,0,1],[0,0,0],[1,0,1]])
        actual = colony.get_array()
        self.assertTrue((expected == actual).all())

        colony.choose_cells([[1,0,1],[0,0,0],[1,0,1]])
        expected = np.array([[0,0,0],[0,0,0],[0,0,0]])
        colony.live_or_die()
        actual = colony.get_array()
        self.assertTrue((expected == actual).all())

        colony.choose_cells([[0,0,0],[1,1,1],[0,0,0]])
        expected = np.array([[0,1,0],[0,1,0],[0,1,0]])
        colony.live_or_die()
        actual = colony.get_array()
        self.assertTrue((expected == actual).all())


if __name__ == '__main__':
    unittest.main()