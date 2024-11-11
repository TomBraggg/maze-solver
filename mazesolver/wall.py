from window import Window
from drawable import Drawable
from point import Point


class Wall(Drawable):
    def __init__(self, point1: Point, point2: Point) -> None:
        self.point1 = point1
        self.point2 = point2
        self.erased = False
        self.id = None

    def update(self, win: Window, fill_colour: str = "black", width: int = 2) -> None:
        if self.erased == True:
            win.canvas.delete(self.id)
            return
        self.id = win.canvas.create_line(
            self.point1.x,
            self.point1.y,
            self.point2.x,
            self.point2.y,
            fill=fill_colour,
            width=width
        )

    def __repr__(self) -> str:
        return f"Wall: id={id(self)} P1={self.point1}, P2={self.point2}, {self.erased=}"
