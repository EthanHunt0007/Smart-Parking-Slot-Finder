
from parking import LAYOUTS, START, get_goals, get_neighbors
from main import bfs, dfs, greedy_best_first, astar


ALGORITHMS = {
    "BFS": bfs,
    "DFS": dfs,
    "Greedy": greedy_best_first,
    "A*": astar
}


def validate_path(path, grid, goals):

    if not path:
        return False, "No path returned"

    if path[0] != START:
        return False, "Path does not start at entrance"

    if path[-1] not in goals:
        return False, "Path does not end at an available slot"

    for row, col in path:

        if not (0 <= row < len(grid) and
                0 <= col < len(grid[0])):
            return False, "Path goes outside grid"

        if grid[row][col] in ['#', 'X']:
            return False, "Path crosses obstacle or occupied slot"

    for i in range(1, len(path)):

        previous = path[i - 1]
        current = path[i]

        distance = (
            abs(previous[0] - current[0]) +
            abs(previous[1] - current[1])
        )

        if distance != 1:
            return False, "Invalid movement detected"

    return True, "Valid path"


def run_tests():

    passed = 0
    failed = 0
    total = 0

    print("\nSMART PARKING - AUTOMATED TESTING")
    print("=" * 55)

    for layout_name, grid in LAYOUTS.items():

        goals = get_goals(grid)

        print(f"\nLAYOUT: {layout_name}")
        print("-" * 55)

        for algorithm_name, algorithm in ALGORITHMS.items():

            total += 1

            path, explored = algorithm(
                grid=grid,
                start=START,
                goals=goals
            )

            valid, message = validate_path(path, grid, goals)

            if valid:
                passed += 1
                print(
                    f"[PASS] {algorithm_name}: "
                    f"Path length = {len(path)-1}, "
                    f"Explored = {explored}"
                )

            else:
                failed += 1
                print(f"[FAIL] {algorithm_name}: {message}")

    print("\n" + "=" * 55)
    print("TEST SUMMARY")
    print("=" * 55)
    print("Total tests:", total)
    print("Passed:", passed)
    print("Failed:", failed)

    if failed == 0:
        print("\nAll tests passed successfully!")
    else:
        print("\nSome tests failed. Check the output above.")


if __name__ == "__main__":
    run_tests()
