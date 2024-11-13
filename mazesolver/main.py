from window import Window
from maze import Maze
from mapper import Mapper
from pathfinder import a_star_search
import random
import time


win = Window(1000, 1000)
seed = random.random()
maze = Maze(80, 80, seed)
mapper = Mapper()

def main():
    win.update(maze)
    mapper.get_weighted_graph_of_maze(win, maze)
    a_star_search(win, mapper.graph)
    win.wait_for_close()

if __name__ == "__main__":
    main()