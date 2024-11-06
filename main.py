from graphics import Window, Line, Point, Cell
from maze import Maze


win = Window(800, 600)

p1 = Point(100, 100)
p2 = Point(200, 200)
line = Line(win, p1, p2)

top_left_1 = Point(300, 300)
bot_right_1 = Point(400, 400)
cell_1 = Cell(win, top_left_1, bot_right_1)
top_left_2 = Point(400, 400)
bot_right_2 = Point(500, 500)
cell_2 = Cell(win, top_left_2, bot_right_2)

origin = Point(0, 0)
maze = Maze(origin, 10, 10, 10, 10, win)


def main():
    win.draw_line(line)

    win.draw_cell(cell_1)
    win.draw_cell(cell_2)
    win.draw_move(cell_1, cell_2)

    maze._create_cells()
    maze._draw_maze()

    win.wait_for_close()


if __name__ == "__main__":
    main()