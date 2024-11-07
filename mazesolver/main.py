from mazesolver.graphics import Window, Line, Point, Cell, Maze
import random


win = Window(1000, 1000)

p1 = Point(500, 100)
p2 = Point(500, 200)
line = Line(p1, p2)

top_left_1 = Point(300, 300)
bot_right_1 = Point(400, 400)
cell_1 = Cell(top_left_1, bot_right_1)
top_left_2 = Point(400, 400)
bot_right_2 = Point(500, 500)
cell_2 = Cell(top_left_2, bot_right_2)

seed = random.random()
maze = Maze(5, 5, seed)


def main():
    
    win.draw(maze)
    win.wait_for_close()


if __name__ == "__main__":
    main()