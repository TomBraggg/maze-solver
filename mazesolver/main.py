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
    mapper.get_weighted_graph_of_maze(win, maze)
    win.wait_for_close()

if __name__ == "__main__":
    main()