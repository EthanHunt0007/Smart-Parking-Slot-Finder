
from collections import deque
from heapq import heappush, heappop
from itertools import count
from time import perf_counter

from parking import GRID, START, GOALS, get_neighbors


def prepare_search(grid, start, goals):
    if not grid or not grid[0]:
        return None

    rows = len(grid)
    cols = len(grid[0])

    sr, sc = start

    if not (0 <= sr < rows and 0 <= sc < cols):
        return None

    if grid[sr][sc] in ['#', 'X']:
        return None

    valid_goals = {
        (r, c) for r, c in goals
        if 0 <= r < rows
        and 0 <= c < cols
        and grid[r][c] not in ['#', 'X']
    }

    if not valid_goals:
        return None

    return valid_goals


def reconstruct_path(parent, goal):
    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()
    return path


def heuristic(position, goals):
    row, col = position

    return min(
        abs(row - goal_row) + abs(col - goal_col)
        for goal_row, goal_col in goals
    )


def bfs(on_expand=None, grid=GRID, start=START, goals=GOALS):
    goals = prepare_search(grid, start, goals)

    if goals is None:
        return None, 0

    queue = deque([start])
    visited = {start}
    parent = {start: None}
    explored = 0

    while queue:
        current = queue.popleft()
        explored += 1

        if on_expand:
            on_expand(current)

        if current in goals:
            return reconstruct_path(parent, current), explored

        for neighbor in get_neighbors(current, grid):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    return None, explored


def dfs(on_expand=None, grid=GRID, start=START, goals=GOALS):
    goals = prepare_search(grid, start, goals)

    if goals is None:
        return None, 0

    stack = [start]
    visited = {start}
    parent = {start: None}
    explored = 0

    while stack:
        current = stack.pop()
        explored += 1

        if on_expand:
            on_expand(current)

        if current in goals:
            return reconstruct_path(parent, current), explored

        for neighbor in get_neighbors(current, grid):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)

    return None, explored


def greedy_best_first(on_expand=None, grid=GRID, start=START, goals=GOALS):
    goals = prepare_search(grid, start, goals)

    if goals is None:
        return None, 0

    priority_queue = []
    tie_breaker = count()

    heappush(
        priority_queue,
        (heuristic(start, goals), next(tie_breaker), start)
    )

    visited = {start}
    parent = {start: None}
    explored = 0

    while priority_queue:
        _, _, current = heappop(priority_queue)
        explored += 1

        if on_expand:
            on_expand(current)

        if current in goals:
            return reconstruct_path(parent, current), explored

        for neighbor in get_neighbors(current, grid):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current

                heappush(
                    priority_queue,
                    (
                        heuristic(neighbor, goals),
                        next(tie_breaker),
                        neighbor
                    )
                )

    return None, explored


def astar(on_expand=None, grid=GRID, start=START, goals=GOALS):
    goals = prepare_search(grid, start, goals)

    if goals is None:
        return None, 0

    priority_queue = []
    tie_breaker = count()

    g_score = {start: 0}
    parent = {start: None}

    heappush(
        priority_queue,
        (heuristic(start, goals), next(tie_breaker), start)
    )

    explored = 0

    while priority_queue:
        f_score, _, current = heappop(priority_queue)

        if f_score != g_score[current] + heuristic(current, goals):
            continue

        explored += 1

        if on_expand:
            on_expand(current)

        if current in goals:
            return reconstruct_path(parent, current), explored

        for neighbor in get_neighbors(current, grid):
            new_cost = g_score[current] + 1

            if new_cost < g_score.get(neighbor, float('inf')):
                g_score[neighbor] = new_cost
                parent[neighbor] = current

                new_f_score = new_cost + heuristic(neighbor, goals)

                heappush(
                    priority_queue,
                    (new_f_score, next(tie_breaker), neighbor)
                )

    return None, explored


def display_grid(path):
    display = [row.copy() for row in GRID]

    if path:
        for row, col in path:
            if display[row][col] not in ['S', 'P']:
                display[row][col] = '*'

    print("\nParking Grid (* = selected route)")

    for row in display:
        print(" ".join(row))


def run_algorithm(name, algorithm):
    start_time = perf_counter()
    path, explored = algorithm()
    end_time = perf_counter()

    print("\n" + "=" * 45)
    print("Algorithm:", name)

    if path:
        print("Parking slot found:", path[-1])
        print("Path:", path)
        print("Path length:", len(path) - 1)
        display_grid(path)
    else:
        print("No reachable parking slot found.")

    print("Nodes explored:", explored)
    print(
        "Execution time:",
        round((end_time - start_time) * 1000, 4),
        "ms"
    )


if __name__ == "__main__":

    print("SMART PARKING SLOT FINDER")
    print("Starting position:", START)
    print("Available parking slots:", GOALS)

    run_algorithm("BFS", bfs)
    run_algorithm("DFS", dfs)
    run_algorithm("Greedy Best-First Search", greedy_best_first)
    run_algorithm("A* Search", astar)
