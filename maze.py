from graphics import Window, Point, Cell


class Maze:
    def __init__(
        self,
        origin: Point,
        num_rows: int,
        num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
        win: Window
    ) -> None:
        self.origin = origin
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._win = win
        self._cells = []

    def _create_cells(self):
        for row in range(self.num_rows):
            row = []
            for cell in range(self.num_cols):
                bot_right_x = self.origin.x + self.cell_size_x
                bot_right_y = self.origin.y + self.cell_size_y
                bot_right = Point(bot_right_x, bot_right_y)
                cell = Cell(self._win, self.origin, bot_right)
                row.append(cell)
                self.origin.x += self.cell_size_x
            self.origin.x -= self.cell_size_x * self.num_rows
            self.origin.y += self.cell_size_y
            self._cells.append(row)

    def _draw_maze(self):
        for row in self._cells:
            for cell in row:
                self._win.draw_cell(cell)
                print(cell)




    def _animate(self):
        pass

