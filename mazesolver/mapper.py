from graph import Graph
from window import Window
from drawable import Drawable
from cell import Cell


class Mapper():
    def __init__(self):
        self._x_pos = 0
        self._y_pos = 0
        self.graph = Graph()

    def get_weighted_graph_of_maze(self):
        pass

    def update(self, win: Window, cell1: Cell, cell2: Cell) -> None:
        undo = False
        if undo:
            fill_colour = "red"
        else:
            fill_colour = "green"
        cell1_midpoint = cell1.get_cell_midpoint()
        cell2_midpoint = cell2.get_cell_midpoint()
        self.id = win.canvas.create_line(
            cell1_midpoint.x,
            cell1_midpoint.y,
            cell2_midpoint.x,
            cell2_midpoint.y,
            fill=fill_colour,
            width=2
        )
        

    # def solve(self, win:Window):
    #     path_exists = True
    #     current_cell = self._cells[0][0]
    #     while path_exists:
    #         if current_cell.has_path():
    #             self._move()
    
    # def draw(self, to_cell: 'Cell', undo: bool = False) -> None:
    #     if undo:
    #         fill_colour = "red"
    #     else:
    #         fill_colour = "green"
    #     line = Line(self._win, self._get_cell_midpoint(), to_cell._get_cell_midpoint())
    #     line.draw(fill_colour)