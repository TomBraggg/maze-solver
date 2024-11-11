import pytest
from mazesolver.window import Window
from mazesolver.maze import Maze


win = Window(1000, 1000)

def test_maze():
    num_rows = 10
    num_cols = 10
    maze = Maze(num_rows, num_cols)
    assert maze._num_cells == num_rows * num_cols
    assert len(maze._cells) == 10
    assert len(maze._cells[0]) == 10
