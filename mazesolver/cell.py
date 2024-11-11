from enum import Enum
from window import Window
from drawable import Drawable
from point import Point
from wall import Wall


class Cell(Drawable):

    class Position(Enum):
        LEFT = "left"
        RIGHT = "right"
        TOP =  "top"
        BOT = "bot"
        TOP_LEFT = "top_left"
        TOP_RIGHT = "top_right"
        BOT_LEFT = "bot_left"
        BOT_RIGHT = "bot_right"

    def __init__(
        self,
        top_left_corner: Point,
        bottom_right_corner: Point,
    ) -> None:
        self.walls = {
            Cell.Position.LEFT: None,
            Cell.Position.RIGHT: None,
            Cell.Position.TOP: None,
            Cell.Position.BOT: None
        }
        self.neighbours = {
            Cell.Position.LEFT: None,
            Cell.Position.RIGHT: None,
            Cell.Position.TOP: None,
            Cell.Position.BOT: None
        }
        self.position = None
        self.col_index = None
        self.row_index = None
        self._top_left_corner = top_left_corner
        self._bottom_right_corner = bottom_right_corner
        self._visited = False

    def update(self, win: Window) -> None:
        for key, wall in self.walls.items():
            win.update(wall)

    def build_walls(self, left: bool = False, right: bool = False, top: bool = False, bot: bool = False) -> None:
        left_x = self._top_left_corner.x
        right_x = self._bottom_right_corner.x
        top_y = self._top_left_corner.y
        bot_y = self._bottom_right_corner.y
        if self.neighbours[Cell.Position.LEFT] != None:
            left_neighbour = self.neighbours[Cell.Position.LEFT]
            self.walls[Cell.Position.LEFT] = left_neighbour.walls[Cell.Position.RIGHT]
        elif left and self.walls[Cell.Position.LEFT] == None:
            self.walls[Cell.Position.LEFT] = Wall(Point(left_x, top_y), Point(left_x, bot_y))
        if self.neighbours[Cell.Position.RIGHT] != None:
            right_neighbour = self.neighbours[Cell.Position.RIGHT]
            self.walls[Cell.Position.RIGHT] = right_neighbour.walls[Cell.Position.LEFT]
        elif right and self.walls[Cell.Position.RIGHT] == None:
            self.walls[Cell.Position.RIGHT] = Wall(Point(right_x, top_y), Point(right_x, bot_y))
        if self.neighbours[Cell.Position.TOP] != None:
            top_neighbour = self.neighbours[Cell.Position.TOP]
            self.walls[Cell.Position.TOP] = top_neighbour.walls[Cell.Position.BOT]
        elif top and self.walls[Cell.Position.TOP] == None:
            self.walls[Cell.Position.TOP] = Wall(Point(left_x, top_y), Point(right_x, top_y))
        if self.neighbours[Cell.Position.BOT] != None:
            bot_neighbour = self.neighbours[Cell.Position.BOT]
            self.walls[Cell.Position.BOT] = bot_neighbour.walls[Cell.Position.TOP]
        elif bot and self.walls[Cell.Position.BOT] == None:
            self.walls[Cell.Position.BOT] = Wall(Point(left_x, bot_y), Point(right_x, bot_y))
    
    def break_walls(self, left: bool = False, right: bool = False, top: bool = False, bot: bool = False) -> None:
        if left and self.walls[Cell.Position.LEFT] != None:
            self.walls[Cell.Position.LEFT].erased = True
        if right and self.walls[Cell.Position.RIGHT] != None:
            self.walls[Cell.Position.RIGHT].erased = True
        if top and self.walls[Cell.Position.TOP] != None:
            self.walls[Cell.Position.TOP].erased = True
        if bot and self.walls[Cell.Position.BOT] != None:
            self.walls[Cell.Position.BOT].erased = True

    def get_cell_midpoint(self) -> Point:
        left = self._top_left_corner.x
        right = self._bottom_right_corner.x
        top = self._top_left_corner.y
        bottom = self._bottom_right_corner.y
        mid_x = (left + right) // 2
        mid_y = (top + bottom) // 2
        mid_point = Point(mid_x, mid_y)
        return mid_point
