from window import Window
from maze import Maze
from mapper import Mapper
import random


win = Window(1000, 1000)
seed = random.random()
maze = Maze(5, 5, seed)
mapper = Mapper()

def main():
    win.update(maze)
    cell1 = maze.cells[0][0]
    cell2 = maze.cells[0][1]
    mapper.update(win, cell1, cell2)
    win.wait_for_close()

if __name__ == "__main__":
    main()