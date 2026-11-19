
import csv
from time import perf_counter

from parking import LAYOUTS, START, get_goals
from main import bfs, dfs, greedy_best_first, astar


ALGORITHMS = {
    "BFS": bfs,
    "DFS": dfs,
    "Greedy": greedy_best_first,
    "A*": astar
}

REPETITIONS = 100


def validate_path(path, grid, goals):

    if not path:
        return False

    if path[0] != START or path[-1] not in goals:
        return False

    for row, col in path:

        if not (0 <= row < len(grid) and
                0 <= col < len(grid[0])):
            return False

        if grid[row][col] in ['#', 'X']:
            return False

    for i in range(1, len(path)):

        previous = path[i - 1]
        current = path[i]

        distance = (
            abs(previous[0] - current[0]) +
            abs(previous[1] - current[1])
        )

        if distance != 1:
            return False

    return True


def run_benchmarks():

    results = []

    print("\nSMART PARKING PERFORMANCE BENCHMARK")
    print("=" * 75)

    for layout_name, grid in LAYOUTS.items():

        goals = get_goals(grid)
        layout_results = {}

        print(f"\nLAYOUT: {layout_name}")
        print("-" * 75)

        for name, algorithm in ALGORITHMS.items():

            total_time = 0
            path = None
            explored = 0

            for _ in range(REPETITIONS):

                start_time = perf_counter()

                path, explored = algorithm(
                    grid=grid,
                    start=START,
                    goals=goals
                )

                end_time = perf_counter()

                total_time += (end_time - start_time) * 1000

            average_time = total_time / REPETITIONS

            valid = validate_path(path, grid, goals)

            path_length = len(path) - 1 if valid else -1

            layout_results[name] = path_length

            status = "PASS" if valid else "FAIL"

            print(
                f"{name:10} | {status:4} | "
                f"Path: {path_length:3} | "
                f"Explored: {explored:3} | "
                f"Average time: {average_time:.5f} ms"
            )

            results.append([
                layout_name,
                name,
                status,
                path_length,
                explored,
                round(average_time, 6)
            ])

        # BFS and A* should find optimal paths
        if (
            layout_results["BFS"] >= 0
            and layout_results["A*"] >= 0
        ):
            if layout_results["BFS"] == layout_results["A*"]:
                print("BFS/A* optimal path check: PASS")
            else:
                print("BFS/A* optimal path check: FAIL")

    with open("benchmark_results.csv", "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Layout",
            "Algorithm",
            "Status",
            "Path Length",
            "Nodes Explored",
            "Average Time (ms)"
        ])

        writer.writerows(results)

    print("\nBenchmark results saved to benchmark_results.csv")


def run_edge_case_tests():

    print("\nEDGE CASE TESTING")
    print("=" * 75)

    edge_cases = [
        (
            "No available parking slots",
            [
                ['S', '.'],
                ['.', '#']
            ],
            (0, 0),
            set()
        ),

        (
            "Unreachable parking slot",
            [
                ['S', '#', 'P'],
                ['#', '#', '#'],
                ['.', '.', '.']
            ],
            (0, 0),
            {(0, 2)}
        ),

        (
            "Blocked starting position",
            [
                ['#', 'P'],
                ['.', '.']
            ],
            (0, 0),
            {(0, 1)}
        )
    ]

    for case_name, grid, start, goals in edge_cases:

        print(f"\n{case_name}:")

        for name, algorithm in ALGORITHMS.items():

            path, explored = algorithm(
                grid=grid,
                start=start,
                goals=goals
            )

            if path is None:
                print(f"[PASS] {name}: Handled correctly")
            else:
                print(f"[FAIL] {name}: Unexpected path found")


if __name__ == "__main__":

    run_benchmarks()
    run_edge_case_tests()
