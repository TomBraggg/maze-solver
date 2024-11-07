from tkinter import Tk, BOTH, Canvas
import time


class Window:
    CELL_DRAW_SPEED: int = 0.8

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
        if type(drawable) == Cell:
            self._animate()

    def _animate(self) -> None:
        self._redraw()
        time.sleep(0.1 * ((1 / self.CELL_DRAW_SPEED) - 1))

    def _redraw(self) -> None:
        self._root.update_idletasks()
        self._root.update()

    def _close(self) -> None:
        self._running = False
        self._root.destroy()


class Drawable:
    def __init__(self) -> None:
        raise NotImplementedError
    
    def draw(self, win:Window) -> None:
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
        has_bottom_wall: bool = True
    ) -> None:
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self._top_left_corner = top_left_corner
        self._bottom_right_corner = bottom_right_corner

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
        if self.has_bottom_wall:
            line = Line(Point(left, bottom), Point(right, bottom))
            win.draw(line)
    
    def draw_move(self, to_cell: 'Cell', undo: bool = False) -> None:
        if undo:
            fill_colour = "red"
        else:
            fill_colour = "green"
        line = Line(self._win, self._get_cell_midpoint(), to_cell._get_cell_midpoint())
        line.draw(fill_colour)

    def _get_cell_midpoint(self) -> Point:
        left = self._top_left_corner.x
        right = self._bottom_right_corner.x
        top = self._top_left_corner.y
        bottom = self._bottom_right_corner.y
        mid_x = (left + right) // 2
        mid_y = (top + bottom) // 2
        mid_point = Point(mid_x, mid_y)
        return mid_point

    def clone(self):
        new_instance = Cell(self._win, self._top_left_corner, self._bottom_right_corner, self.has_left_wall, self.has_right_wall, self.has_top_wall, self.has_bottom_wall)
        return new_instance

    def __repr__(self) -> str:
        return f"\nCell: {self._top_left_corner=}, {self._bottom_right_corner=}"


class Maze(Drawable):
    def __init__(
        self,
        origin: Point,
        num_rows: int,
        num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
    ) -> None:
        self.origin = origin
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._cells = []

    def draw(self, win: Window):
        self._create_cells()
        for row in self._cells:
            for cell in row:
                win.draw(cell)

    def _create_cells(self):
        top_left = self.origin
        for row in range(self.num_rows):
            row = []
            for cell in range(self.num_cols):
                cell = self._get_cell_from_corner_and_size(top_left)
                row.append(cell)
                top_left.x += self.cell_size_x
            top_left.x -= self.cell_size_x * self.num_rows
            top_left.y += self.cell_size_y
            self._cells.append(row)

    def _get_cell_from_corner_and_size(self, top_left: Point) -> Cell:
        top_left_copy = top_left.clone()
        bot_right_x = top_left_copy.x + self.cell_size_x
        bot_right_y = top_left_copy.y + self.cell_size_y
        bot_right = Point(bot_right_x, bot_right_y)
        cell = Cell(top_left_copy, bot_right)
        return cell
