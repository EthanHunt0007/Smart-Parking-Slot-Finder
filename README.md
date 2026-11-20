# Smart Parking Slot Finder

An AI-based parking navigation system that uses classical search algorithms to find available parking slots in a grid-based parking environment.

## Project Overview

The Smart Parking Slot Finder simulates a parking lot as a 2D grid. A vehicle starts at a designated entrance and searches for an available parking slot while avoiding obstacles and occupied spaces.

The project implements and compares four AI search algorithms through an interactive visualization.

## Algorithms Implemented

- **Breadth-First Search (BFS):** Explores nodes level by level to find the shortest path in an unweighted grid.
- **Depth-First Search (DFS):** Explores one path as deeply as possible before backtracking.
- **Greedy Best-First Search:** Uses a heuristic to prioritize nodes that appear closer to the destination.
- **A* Search:** Combines the path cost and heuristic estimate to find an optimal path in the grid.

## Features

- Interactive Pygame-based visualization.
- Four implemented AI search algorithms.
- Three predefined parking layouts: Default, Easy and Crowded.
- Animated visualization of the search process.
- Highlights the final path to the selected parking slot.
- Displays execution time, nodes explored and path length.
- Automated correctness testing.
- Edge-case testing and algorithm benchmarking.
- Exports benchmark results to CSV.

## Technologies Used

- Python
- Pygame
- AI Search Algorithms
- Data Structures and Algorithms

## Project Structure

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
├── README.md
└── .gitignore
```

## Installation and Execution

### 1. Clone the repository

```bash
git clone <YOUR-REPOSITORY-URL>
```

### 2. Navigate to the project directory

```bash
cd Smart-Parking-Slot-Finder
```

### 3. Install dependencies

```bash
pip install pygame
```

### 4. Run the visualizer

```bash
python visualizer.py
```

## Testing

Run automated correctness tests:

```bash
python test_algorithms.py
```

Run algorithm benchmarks:

```bash
python benchmark.py
```

Benchmark results are saved in `benchmark_results.csv`.

## Performance Evaluation

The algorithms are evaluated across different parking layouts using:

- Execution time
- Number of nodes explored
- Path length

The implementation also checks path validity, obstacle avoidance, unreachable destinations and invalid starting positions.

## Team

**Department:** Information Technology  
**Institution:** Netaji Subhas University of Technology (NSUT)

## Project Purpose

This project demonstrates the practical application of classical Artificial Intelligence search techniques to a real-world navigation problem.
