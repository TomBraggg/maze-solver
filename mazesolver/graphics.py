from tkinter import Tk, BOTH, Canvas
from graph import Graph
import time
import random


class Window:
    def __init__(self, width: int, height: int) -> None:
        self._root = Tk()
        self._root.title("Maze Solver")
        self.canvas = Canvas(self._root, bg="white", height=height, width=width)
        self.canvas.pack(fill=BOTH, expand=1)
        self.height = height
        self.width = width
        self._running = False
        self._root.protocol("WM_DELETE_WINDOW", self._close)
        
    def wait_for_close(self) -> None:
        self._running = True
        while self._running:
            self._redraw()

    def draw(self, drawable: 'Drawable') -> None:
        drawable.draw(self)

    def _redraw(self) -> None:
        self._root.update_idletasks()
        self._root.update()

    def _close(self) -> None:
        self._running = False
        self._root.destroy()


class Drawable:
    def __init__(self) -> None:
        raise NotImplementedError
    
    def draw(self) -> None:
        raise NotImplementedError


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        
    def clone(self) -> 'Point':
        point = Point(self.x, self.y)
        return point

    def __repr__(self) -> str:
        return f"Point: {self.x=}, {self.y=}"


class Line(Drawable):
    def __init__(self, point1: Point, point2: Point) -> None:
        self.point1 = point1
        self.point2 = point2

    def draw(self, win: Window, fill_colour: str = "black", width: int = 5) -> None:
        win.canvas.create_line(
            self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_colour, width=width
        )

    def __repr__(self) -> str:
        return f"\nLine: {self.point1=}, {self.point2=}"


class Cell(Drawable):
    def __init__(
        self,
        top_left_corner: Point,
        bottom_right_corner: Point,
        has_left_wall: bool = True,
        has_right_wall: bool = True,
        has_top_wall: bool = True,
        has_bot_wall: bool = True
    ) -> None:
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bot_wall = has_bot_wall
        self._top_left_corner = top_left_corner
        self._bottom_right_corner = bottom_right_corner
        self._visited = False

    def draw(self, win: Window, fill_colour: str = "black", width: int = 5) -> None:
        left = self._top_left_corner.x
        right = self._bottom_right_corner.x
        top = self._top_left_corner.y
        bottom = self._bottom_right_corner.y
        if self.has_left_wall:
            line = Line(Point(left, top), Point(left, bottom))
            win.draw(line)
        if self.has_right_wall:
            line = Line(Point(right, top), Point(right, bottom))
            win.draw(line)
        if self.has_top_wall:
            line = Line(Point(left, top), Point(right, top))
            win.draw(line)
        if self.has_bot_wall:
            line = Line(Point(left, bottom), Point(right, bottom))
            win.draw(line)
    
    def break_walls(self, left: bool = False, right: bool = False, top: bool = False, bot: bool = False) -> None:
        self.has_left_wall = not left
        self.has_right_wall = not right
        self.has_top_wall = not top
        self.has_bot_wall = not bot

    def clone(self):
        new_instance = Cell(self._win, self._top_left_corner, self._bottom_right_corner, self.has_left_wall, self.has_right_wall, self.has_top_wall, self.has_bot_wall)
        return new_instance

    def _get_cell_midpoint(self) -> Point:
        left = self._top_left_corner.x
        right = self._bottom_right_corner.x
        top = self._top_left_corner.y
        bottom = self._bottom_right_corner.y
        mid_x = (left + right) // 2
        mid_y = (top + bottom) // 2
        mid_point = Point(mid_x, mid_y)
        return mid_point

    def __repr__(self) -> str:
        return f"\nCell: {self._top_left_corner=}, {self._bottom_right_corner=}"


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
        self._cells = []
        if seed == None:
            random.seed(0)
        else:
            random.seed(seed)

    def draw(self, win: Window):
        self._create_cells(win.height, win.width)
        for row in self._cells:
            for cell in row:
                win.draw(cell)
                self._animate(win)

    def _create_cells(self, win_height: int, win_width: int):
        border_thickness = 50
        top_left = Point(border_thickness, border_thickness) 
        cell_height = (win_height - 2 * border_thickness) / self.num_rows
        cell_width = (win_width - 2 * border_thickness) / self.num_cols
        cells_created_counter = 0
        for row in range(self.num_rows):
            row = []
            for cell in range(self.num_cols):
                cell = self._get_cell_from_corner_and_size(top_left, cell_height, cell_width)
                cell_type = self._get_cell_type(cells_created_counter)
                self._break_walls(cell, cell_type)
                row.append(cell)
                cells_created_counter += 1
                top_left.x += cell_width
            top_left.x -= cell_width * self.num_rows
            top_left.y += cell_height
            self._cells.append(row)

    def _get_cell_from_corner_and_size(self, top_left: Point, cell_height: int, cell_width: int) -> Cell:
        top_left_copy = top_left.clone()
        bot_right_x = top_left_copy.x + cell_width
        bot_right_y = top_left_copy.y + cell_height
        bot_right = Point(bot_right_x, bot_right_y)
        cell = Cell(top_left_copy, bot_right)
        return cell
    
    def _get_cell_type(self, cells_created_counter) -> dict:
        left_cell = (cells_created_counter + self.num_cols) % self.num_cols == 0
        right_cell = (cells_created_counter + 1) % self.num_cols == 0
        top_cell = 0 <= cells_created_counter <= self.num_cols
        bot_cell = (self._num_cells - self.num_cols) <= cells_created_counter <= self._num_cells 
        top_left_cell = left_cell and top_cell
        top_right_cell = right_cell and top_cell
        bot_left_cell = left_cell and bot_cell
        bot_right_cell = right_cell and bot_cell
        cell_type = {
            "left_cell": left_cell,
            "right_cell": right_cell,
            "top_cell": top_cell,
            "bot_cell": bot_cell,
            "top_left_cell": top_left_cell,
            "top_right_cell": top_right_cell,
            "bot_left_cell": bot_left_cell,
            "bot_right_cell": bot_right_cell
        }
        return cell_type
        
    def _break_walls(self, cell: Cell, cell_type: dict) -> None:
        break_chance = 0.8
        cell.break_walls(
            left=random.random() <= break_chance,
            right=random.random() <= break_chance,
            top=random.random() <= break_chance,
            bot=random.random() <= break_chance
            )
        self._maintain_edges(cell, cell_type)

    def _maintain_edges(self, cell: Cell, cell_type: dict) -> None:
        if cell_type["top_left_cell"]:
            cell.break_walls(left=False, right=not cell.has_right_wall, top=True, bot=not cell.has_bot_wall)
        elif cell_type["bot_right_cell"]:
            cell.break_walls(left=not cell.has_left_wall, right=False, top=not cell.has_top_wall, bot=True)
        elif cell_type["top_right_cell"]:
            cell.break_walls(left=not cell.has_left_wall, right=False, top=False, bot=not cell.has_bot_wall)
        elif cell_type["bot_left_cell"]:
            cell.break_walls(left=False, right=not cell.has_right_wall, top=not cell.has_top_wall, bot=False)
        elif cell_type["left_cell"]:
            cell.break_walls(left=False, right=not cell.has_right_wall, top=not cell.has_top_wall, bot=not cell.has_bot_wall)
        elif cell_type["right_cell"]:
            cell.break_walls(left=not cell.has_left_wall, right=False, top=not cell.has_top_wall, bot=not cell.has_bot_wall)
        elif cell_type["top_cell"]:
            cell.break_walls(left=not cell.has_left_wall, right=not cell.has_right_wall, top=False, bot=not cell.has_bot_wall)
        elif cell_type["bot_cell"]:
            cell.break_walls(left=not cell.has_left_wall, right=not cell.has_right_wall, top=not cell.has_top_wall, bot=False)

    def _animate(self, win: Window) -> None:
        cell_draw_time = 1
        delay = cell_draw_time / self._num_cells
        win._redraw()
        time.sleep(delay)

class Solver(Drawable):
    def __init__(self):
        self._x_pos = 0
        self._y_pos = 0
        self.graph = Graph()

    def solve(self):
        pass

    def _move(self):
        pass

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
