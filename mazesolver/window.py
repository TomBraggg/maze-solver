from tkinter import Tk, BOTH, Canvas
from drawable import Drawable


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

    def update(self, drawable: 'Drawable') -> None:
        if drawable is not None:
            drawable.update(self)

    def _redraw(self) -> None:
        self._root.update_idletasks()
        self._root.update()

    def _close(self) -> None:
        self._running = False
        self._root.destroy()