from graphics import Window, Line, Point, Cell, Maze


win = Window(800, 600)

p1 = Point(500, 100)
p2 = Point(500, 200)
line = Line(p1, p2)

top_left_1 = Point(300, 300)
bot_right_1 = Point(400, 400)
cell_1 = Cell(top_left_1, bot_right_1)
top_left_2 = Point(400, 400)
bot_right_2 = Point(500, 500)
cell_2 = Cell(top_left_2, bot_right_2)

origin = Point(0, 0)
maze = Maze(origin, 10, 10, 50, 50)


def main():
    
    win.draw(maze)
    win.wait_for_close()


if __name__ == "__main__":
    main()