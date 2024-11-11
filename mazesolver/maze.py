import time
import random
from window import Window
from drawable import Drawable
from point import Point
from cell import Cell


class Maze(Drawable):
    def __init__(
        self,
        num_rows: int,
        num_cols: int,
        seed: int = None
    ) -> None:
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._num_cells = num_rows * num_cols
        self.cells = []
        for col in range(self.num_cols):
            _row = []
            for row in range(self.num_rows):
                _row.append(None)
            self.cells.append(_row)
        if seed == None:
            random.seed(0)
        else:
            random.seed(seed)

    def update(self, win: Window):
        self._create_cells(win.height, win.width)
        for row in self.cells:
            for cell in row:
                win.update(cell)
                self._animate(win)

    def _create_cells(self, win_height: int, win_width: int):
        border_thickness = 50
        top_left = Point(border_thickness, border_thickness) 
        cell_height = (win_height - 2 * border_thickness) / self.num_rows
        cell_width = (win_width - 2 * border_thickness) / self.num_cols
        cells_created_counter = 0
        for row_index in range(self.num_rows):
            for col_index in range(self.num_cols):
                cell = self._get_cell_from_corner_and_size(top_left, cell_height, cell_width)
                cell.row_index = row_index
                cell.col_index = col_index
                self._assign_cell_neighbours(cell)
                self._get_cell_position(cell, cells_created_counter)
                self._build_walls(cell)
                self.cells[row_index][col_index] = cell
                cells_created_counter += 1
                top_left.x += cell_width
            top_left.x -= cell_width * self.num_rows
            top_left.y += cell_height

    def _get_cell_from_corner_and_size(self, top_left: Point, cell_height: int, cell_width: int) -> Cell:
        top_left_copy = top_left.clone()
        bot_right_x = top_left_copy.x + cell_width
        bot_right_y = top_left_copy.y + cell_height
        bot_right = Point(bot_right_x, bot_right_y)
        cell = Cell(top_left_copy, bot_right)
        return cell
    
    def _get_cell_position(self, cell: Cell, cells_created_counter: int) -> None:
        left_cell = (cells_created_counter + self.num_cols) % self.num_cols == 0
        right_cell = (cells_created_counter + 1) % self.num_cols == 0
        top_cell = 0 <= cells_created_counter < self.num_cols
        bot_cell = (self._num_cells - self.num_cols) <= cells_created_counter <= self._num_cells 
        top_left_cell = left_cell and top_cell
        top_right_cell = right_cell and top_cell
        bot_left_cell = left_cell and bot_cell
        bot_right_cell = right_cell and bot_cell
        if left_cell:
            cell.position = Cell.Position.LEFT
        if right_cell:
            cell.position = Cell.Position.RIGHT
        if top_cell:
            cell.position = Cell.Position.TOP
        if bot_cell:
            cell.position = Cell.Position.BOT
        if top_left_cell:
            cell.position = Cell.Position.TOP_LEFT
        if top_right_cell:
            cell.position = Cell.Position.TOP_RIGHT
        if bot_left_cell:
            cell.position = Cell.Position.BOT_LEFT
        if bot_right_cell:
            cell.position = Cell.Position.BOT_RIGHT
    
    def _assign_cell_neighbours(self, cell) -> None:
        if cell.col_index - 1 >= 0:
            left_neighbour = self.cells[cell.row_index][cell.col_index - 1]
            if left_neighbour != None:
                cell.neighbours[Cell.Position.LEFT] = left_neighbour
                left_neighbour.neighbours[Cell.Position.RIGHT] = cell
        if cell.col_index + 1 < self.num_cols:
            right_neighbour = self.cells[cell.row_index][cell.col_index + 1]
            if right_neighbour != None:
                cell.neighbours[Cell.Position.RIGHT] = right_neighbour
                right_neighbour.neighbours[Cell.Position.LEFT] = cell
        if cell.row_index - 1 >= 0:
            top_neighbour = self.cells[cell.row_index - 1][cell.col_index]
            if top_neighbour != None:
                cell.neighbours[Cell.Position.TOP] = top_neighbour
                top_neighbour.neighbours[Cell.Position.BOT] = cell
        if cell.row_index + 1 < self.num_rows:
            bot_neighbour = self.cells[cell.row_index + 1][cell.col_index]
            if bot_neighbour != None:
                cell.neighbours[Cell.Position.BOT] = bot_neighbour
                bot_neighbour.neighbours[Cell.Position.TOP] = cell
        
    def _build_walls(self, cell: Cell) -> None:
        build_chance = 0.25
        cell.build_walls(
            left=random.random() <= build_chance,
            right=random.random() <= build_chance,
            top=random.random() <= build_chance,
            bot=random.random() <= build_chance
            )
        self._maintain_edges(cell)

    def _maintain_edges(self, cell: Cell) -> None:
        if cell.position == Cell.Position.TOP_LEFT:
            cell.build_walls(left=True)
            cell.break_walls(top=True)
        elif cell.position == Cell.Position.TOP_RIGHT:
            cell.build_walls(right=True,top=True)
        elif cell.position == Cell.Position.BOT_LEFT:
            cell.build_walls(left=True, bot=True)
        elif cell.position == Cell.Position.BOT_RIGHT:
            cell.build_walls(right=True)
            cell.break_walls(bot=True)
        elif cell.position == Cell.Position.LEFT:
            cell.build_walls(left=True)
        elif cell.position == Cell.Position.RIGHT:
            cell.build_walls(right=True)
        elif cell.position == Cell.Position.TOP:
            cell.build_walls(top=True)
        elif cell.position == Cell.Position.BOT:
            cell.build_walls(bot=True)

    def _animate(self, win: Window) -> None:
        cell_draw_time = 1
        delay = cell_draw_time / self._num_cells
        win._redraw()
        time.sleep(delay)
    