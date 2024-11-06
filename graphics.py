from tkinter import Tk, BOTH, Canvas


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

    def draw_line(self, line: 'Line', fill_colour: str = "blue", width: int = 5):
        line.draw(fill_colour, width)

    def draw_cell(self, cell: 'Cell', fill_colour: str = "blue", width: int = 5):
        cell.draw(fill_colour, width)

    def draw_move(self, from_cell: 'Cell', to_cell: 'Cell'):
        from_cell.draw_move(to_cell)

    def _redraw(self) -> None:
        self._root.update_idletasks()
        self._root.update()

    def _close(self) -> None:
        self._running = False
        self._root.destroy()

    
class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        
    def __repr__(self) -> str:
        return f"Point: {self.x=}, {self.y=}"


class Line:
    def __init__(self, win: Window, point1: Point, point2: Point) -> None:
        self.point1 = point1
        self.point2 = point2
        self._win = win

    def __repr__(self) -> str:
        return f"Line: {self.point1=}, {self.point2=}"

    def draw(self, fill_colour: str = "black", width: int = 5) -> None:
        self._win.canvas.create_line(
            self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_colour, width=width
        )


class Cell:
    def __init__(
        self,
        win: Window,
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
        self._win = win
        self._top_left_corner = top_left_corner
        self._bottom_right_corner = bottom_right_corner

    def __repr__(self) -> str:
        return f"Cell: {self._top_left_corner=}, {self._bottom_right_corner=}"

    def draw(self, fill_colour: str = "black", width: int = 5) -> None:
        left = self._top_left_corner.x
        right = self._bottom_right_corner.x
        top = self._top_left_corner.y
        bottom = self._bottom_right_corner.y
        if self.has_left_wall:
            line = Line(self._win, Point(left, top), Point(left, bottom))
            line.draw(fill_colour, width)
        if self.has_right_wall:
            line = Line(self._win, Point(right, top), Point(right, bottom))
            line.draw(fill_colour, width)
        if self.has_top_wall:
            line = Line(self._win, Point(left, top), Point(right, top))
            line.draw(fill_colour, width)
        if self.has_bottom_wall:
            line = Line(self._win, Point(left, bottom), Point(right, bottom))
            line.draw(fill_colour, width)
    
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
