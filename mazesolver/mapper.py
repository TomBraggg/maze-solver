from graph import Graph
from window import Window
from drawable import Drawable
from cell import Cell
from maze import Maze


class Mapper():
    def __init__(self):
        self._x_pos = 0
        self._y_pos = 0
        self.graph = Graph()

    def get_weighted_graph_of_maze(self, win: Window, maze: Maze):
        for row in maze.cells:
            for cell in row:
                if cell.neighbours[Cell.Position.LEFT] != None and cell.walls[Cell.Position.LEFT] == None:
                    self.graph.add_edge(cell, cell.neighbours[Cell.Position.LEFT])
                    self.update(win, cell, cell.neighbours[Cell.Position.LEFT])
                if cell.neighbours[Cell.Position.RIGHT] != None and cell.walls[Cell.Position.RIGHT] == None:
                    self.graph.add_edge(cell, cell.neighbours[Cell.Position.RIGHT])
                    self.update(win, cell, cell.neighbours[Cell.Position.RIGHT])
                if cell.neighbours[Cell.Position.TOP] != None and cell.walls[Cell.Position.TOP] == None:
                    self.graph.add_edge(cell, cell.neighbours[Cell.Position.TOP])
                    self.update(win, cell, cell.neighbours[Cell.Position.TOP])
                if cell.neighbours[Cell.Position.BOT] != None and cell.walls[Cell.Position.BOT] == None:
                    self.graph.add_edge(cell, cell.neighbours[Cell.Position.BOT])
                    self.update(win, cell, cell.neighbours[Cell.Position.BOT])


    def update(self, win: Window, cell1: Cell, cell2: Cell) -> None:
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