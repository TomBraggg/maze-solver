import pytest
from mazesolver.graphics import Maze, Window

win = Window(1000, 1000)

def test_maze():
    num_rows = 10
    num_cols = 10
    maze = Maze(num_rows, num_cols)
    maze._create_cells(win.width, win.height)
    assert len(maze._cells) == 10
    assert len(maze._cells[0]) == 10
