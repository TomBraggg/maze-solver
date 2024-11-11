from window import Window
from wall import Wall
from point import Point
from cell import Cell
from maze import Maze
import random


win = Window(1000, 1000)
seed = random.random()
maze = Maze(5, 5, seed)

def main():
    win.update(maze)
    win.wait_for_close()


if __name__ == "__main__":
    main()