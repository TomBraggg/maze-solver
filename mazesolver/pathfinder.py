import time
from graph import Graph
from priorityqueue import PriorityQueue
from cell import Cell
from window import Window


def a_star_search(win: Window, maze: Graph):
    start = next(iter(maze.graph))
    end = max(maze.graph.keys(), key=lambda k: (k.col_index, k.row_index))
    print(maze.graph)
    print(start)
    print(end)
    p_queue = PriorityQueue()
    p_queue.push(0, start)
    predecessors = {start: None}
    costs = {start: 0}
    visited = set()
    while p_queue:
        current_cell: Cell = p_queue.pop()
        if current_cell != start:
            draw(win, predecessors[current_cell], current_cell, len(maze.graph), 2)
        if current_cell.position == Cell.Position.BOT_RIGHT:
            break
        if current_cell in visited:
            continue
        visited.add(current_cell)
        for neighbour in maze.graph[current_cell]:
            cost_to_neighbour = costs[current_cell] + 1
            if neighbour != None and (neighbour not in costs or cost_to_neighbour < costs[neighbour]):
                costs[neighbour] = cost_to_neighbour
                neighbour_prio = costs[neighbour] + heuristic(neighbour, end)
                p_queue.push(neighbour_prio, neighbour)
                predecessors[neighbour] = current_cell
    path = []
    pred = current_cell
    while pred != None:
        path.append(pred)
        pred = predecessors[pred]
    path = path[::-1]
    prev_node = None
    for node in path:
        if prev_node != None:
            draw(win, prev_node, node, len(maze.graph), 5)
        prev_node = node
    return len(path)
            
def heuristic(neighbour, end):
    return (abs(neighbour.col_index - end.col_index) + abs(neighbour.row_index - end.row_index))

def draw(win: Window, cell1: Cell, cell2: Cell, size: int, line_width: int) -> id:
    fill_colour = "red"
    cell1_midpoint = cell1.get_cell_midpoint()
    cell2_midpoint = cell2.get_cell_midpoint()
    _animate(win, size)
    if abs(cell1_midpoint.x - cell2_midpoint.x) > abs(cell1_midpoint.y - cell2_midpoint.y):
        if cell1_midpoint.x < cell2_midpoint.x:
            cell1_midpoint.x -= line_width / 2
            cell2_midpoint.x += line_width / 2
    else:
        if cell1_midpoint.y < cell2_midpoint.y:
            cell1_midpoint.y -= line_width / 2
            cell2_midpoint.y += line_width / 2 
    return win.canvas.create_line(
        cell1_midpoint.x,
        cell1_midpoint.y,
        cell2_midpoint.x,
        cell2_midpoint.y,
        fill=fill_colour,
        width=line_width
    )

def _animate(win: Window, size: int) -> None:
    cell_draw_time = 2
    delay = cell_draw_time / size
    win._redraw()
    time.sleep(delay)
