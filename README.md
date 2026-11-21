# Smart Parking Slot Finder

An AI-based parking navigation system that uses classical search algorithms to find available parking slots in a grid-based parking environment.

## 1. Project Overview

The Smart Parking Slot Finder simulates a parking lot as a 2D grid. A vehicle starts at a designated entrance and searches for an available parking slot while avoiding obstacles and occupied spaces.

The project implements and compares four classical Artificial Intelligence search algorithms through an interactive visualization.

## 2. Algorithms Implemented

- **Breadth-First Search (BFS):** Explores nodes level by level and guarantees the shortest path in an unweighted grid.
- **Depth-First Search (DFS):** Explores one path as deeply as possible before backtracking.
- **Greedy Best-First Search:** Uses a heuristic to prioritize nodes that appear closer to the destination.
- **A* Search:** Combines the actual path cost and heuristic estimate to find an optimal path.

## 3. Features

- Interactive Pygame-based visualization.
- Four implemented AI search algorithms.
- Three predefined parking layouts: Default, Easy and Crowded.
- Animated visualization of the search process.
- Highlights the final path to the selected parking slot.
- Displays execution time, nodes explored and path length.
- Automated correctness testing.
- Edge-case testing and algorithm benchmarking.
- Exports benchmark results to CSV.

## 4. Technologies Used

- Python
- Pygame
- Artificial Intelligence Search Algorithms
- Data Structures and Algorithms

## 5. Project Structure

```text
Smart-Parking-Slot-Finder/
│
├── parking.py
├── main.py
├── visualizer.py
├── test_algorithms.py
├── benchmark.py
├── benchmark_results.csv
├── requirements.txt
└── README.md
```

## 6. Installation and Execution

### Step 1: Clone the repository

```bash
git clone https://github.com/EthanHunt0007/Smart-Parking-Slot-Finder.git
```

### Step 2: Navigate to the project directory

```bash
cd Smart-Parking-Slot-Finder
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the application

```bash
python visualizer.py
```

## 7. Testing

Run automated correctness tests:

```bash
python test_algorithms.py
```

The test suite evaluates all four algorithms across the three parking layouts and checks path validity, obstacle avoidance and valid movement.

The implementation also handles important edge cases, including:

- No available parking slots.
- Unreachable parking slots.
- Blocked starting positions.

## 8. Benchmarking and Performance Evaluation

Run the benchmarking script:

```bash
python benchmark.py
```

The benchmarking process evaluates all four algorithms across the three predefined parking layouts using repeated executions.

The following performance metrics are recorded:

- **Execution Time:** Time taken by an algorithm to complete the search.
- **Nodes Explored:** Number of nodes visited during the search.
- **Path Length:** Length of the resulting path to the parking slot.

The benchmark results are exported to `benchmark_results.csv` for further analysis.

## 9. Results and Analysis

The four algorithms demonstrate different search strategies and performance characteristics.

- **BFS:** Guarantees the shortest path in an unweighted grid but may explore a large number of nodes.
- **DFS:** Can reach a destination without exploring the entire search space, but does not guarantee the shortest path.
- **Greedy Best-First Search:** Prioritizes nodes based on heuristic estimates and can reach promising destinations quickly, but does not guarantee an optimal path.
- **A* Search:** Considers both the cost already incurred and the estimated remaining cost, providing optimal paths when the heuristic is admissible and the algorithm is implemented correctly.

The benchmark results allow the algorithms to be compared across different parking configurations in terms of execution time, nodes explored and path length.

No single algorithm is universally best for every performance metric. The results depend on the parking layout and the search strategy used.

## 10. Team

**Institution:** Netaji Subhas University of Technology (NSUT)

**Department:** Information Technology

## 11. Project Objective

This project demonstrates the practical application of classical Artificial Intelligence search techniques to a real-world navigation problem. It also provides a comparative study of different search strategies through interactive visualization, automated testing and performance benchmarking.
