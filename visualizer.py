
import pygame
import sys
from time import perf_counter

from parking import LAYOUTS, START, get_goals
from main import bfs, dfs, greedy_best_first, astar

pygame.init()

# Window settings
WIDTH = 600
HEIGHT = 710

ROWS = 10
COLS = 10
CELL_SIZE = 44

GRID_LEFT = (WIDTH - COLS * CELL_SIZE) // 2
GRID_TOP = 40

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart Parking Slot Finder")

clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
GREY = (180, 180, 180)
GREEN = (50, 180, 80)
RED = (220, 60, 60)
BLUE = (60, 120, 220)
YELLOW = (255, 210, 50)
LIGHT_BLUE = (150, 210, 255)
DARK_BLUE = (35, 75, 130)
BUTTON_HOVER = (65, 110, 175)

font = pygame.font.SysFont(None, 19)
button_font = pygame.font.SysFont(None, 23)
heading_font = pygame.font.SysFont(None, 30)

# Active layout
current_layout = "Default"
active_grid = LAYOUTS[current_layout]
active_goals = get_goals(active_grid)

# Search results
path = None
explored = 0
algorithm_name = ""
execution_time = 0

# Animation
explored_order = []
animation_index = 0
animating = False
animation_delay = 30
last_animation_time = 0

# Algorithm buttons
buttons = [
    (pygame.Rect(10, 530, 135, 36), "BFS", bfs),
    (pygame.Rect(154, 530, 135, 36), "DFS", dfs),
    (pygame.Rect(298, 530, 135, 36), "Greedy", greedy_best_first),
    (pygame.Rect(442, 530, 135, 36), "A*", astar)
]

# Layout buttons
layout_buttons = [
    (pygame.Rect(30, 600, 165, 36), "Default"),
    (pygame.Rect(217, 600, 165, 36), "Easy"),
    (pygame.Rect(404, 600, 165, 36), "Crowded")
]

# Reset button
reset_button = pygame.Rect(220, 650, 160, 32)


def run_search(algorithm, name):
    global path, explored, algorithm_name
    global explored_order, animation_index
    global animating, last_animation_time, execution_time

    explored_order = []

    start_time = perf_counter()

    path, explored = algorithm(
        on_expand=explored_order.append,
        grid=active_grid,
        start=START,
        goals=active_goals
    )

    execution_time = (perf_counter() - start_time) * 1000

    algorithm_name = name
    animation_index = 0
    animating = True
    last_animation_time = pygame.time.get_ticks()


def reset_search():
    global path, explored, algorithm_name
    global explored_order, animation_index, animating
    global execution_time

    path = None
    explored = 0
    algorithm_name = ""
    execution_time = 0

    explored_order = []
    animation_index = 0
    animating = False


def change_layout(layout_name):
    global current_layout, active_grid, active_goals

    current_layout = layout_name
    active_grid = LAYOUTS[current_layout]
    active_goals = get_goals(active_grid)

    reset_search()


def draw_grid():

    visible_explored = set(explored_order[:animation_index])

    for row in range(ROWS):
        for col in range(COLS):

            cell = active_grid[row][col]
            position = (row, col)

            x = GRID_LEFT + col * CELL_SIZE
            y = GRID_TOP + row * CELL_SIZE

            color = WHITE

            if cell == "#":
                color = BLACK
            elif cell == "S":
                color = BLUE
            elif cell == "P":
                color = GREEN
            elif cell == "X":
                color = RED

            if position in visible_explored:
                if cell not in ["S", "P", "X", "#"]:
                    color = LIGHT_BLUE

            if path and not animating and position in path:
                if cell not in ["S", "P"]:
                    color = YELLOW

            pygame.draw.rect(
                screen, color,
                (x, y, CELL_SIZE, CELL_SIZE)
            )

            pygame.draw.rect(
                screen, GREY,
                (x, y, CELL_SIZE, CELL_SIZE), 1
            )


def draw_button(rect, label, selected=False):

    mouse_position = pygame.mouse.get_pos()

    if selected:
        color = GREEN
    elif rect.collidepoint(mouse_position):
        color = BUTTON_HOVER
    else:
        color = DARK_BLUE

    pygame.draw.rect(
        screen, color, rect,
        border_radius=8
    )

    text = button_font.render(label, True, WHITE)
    screen.blit(text, text.get_rect(center=rect.center))


def draw_legend():

    legend_items = [
        (BLUE, "Start"),
        (GREEN, "Available"),
        (RED, "Occupied"),
        (BLACK, "Obstacle"),
        (LIGHT_BLUE, "Explored"),
        (YELLOW, "Path")
    ]

    positions = [
        (12, 480), (110, 480), (225, 480),
        (330, 480), (425, 480), (520, 480)
    ]

    for (color, label), (x, y) in zip(legend_items, positions):

        pygame.draw.rect(screen, color, (x, y, 13, 13))

        text = font.render(label, True, BLACK)
        screen.blit(text, (x + 17, y - 2))


def draw_interface():

    screen.fill(WHITE)

    # Title
    title = heading_font.render(
        "SMART PARKING SLOT FINDER",
        True, DARK_BLUE
    )

    screen.blit(title, title.get_rect(center=(WIDTH // 2, 17)))

    # Parking grid
    draw_grid()

    # Legend
    draw_legend()

    # Algorithm selection
    label = font.render("SELECT SEARCH ALGORITHM", True, BLACK)
    screen.blit(label, (10, 510))

    for rect, name, algorithm in buttons:
        draw_button(rect, name)

    # Layout selection
    label = font.render("SELECT PARKING LAYOUT", True, BLACK)
    screen.blit(label, (10, 580))

    for rect, name in layout_buttons:
        draw_button(
            rect, name,
            selected=(current_layout == name)
        )

    # Reset
    draw_button(reset_button, "RESET")

    # Status
    if animating:
        message = f"{algorithm_name}: Exploring..."

    elif path:
        message = (
            f"{algorithm_name} | Path: {len(path)-1} | "
            f"Explored: {explored} | Time: {execution_time:.3f} ms"
        )

    elif algorithm_name:
        message = f"{algorithm_name}: No reachable parking slot"

    else:
        message = (
            f"Layout: {current_layout} | "
            f"Available slots: {len(active_goals)}"
        )

    text = font.render(message, True, BLACK)
    screen.blit(text, text.get_rect(center=(WIDTH // 2, 696)))

    # Destination information
    if path and not animating:
        destination = font.render(
            f"Destination: {path[-1]}",
            True, DARK_BLUE
        )
        screen.blit(
            destination,
            destination.get_rect(center=(WIDTH // 2, 682))
        )

    pygame.display.flip()


running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                for rect, name, algorithm in buttons:
                    if rect.collidepoint(event.pos):
                        run_search(algorithm, name)

                for rect, name in layout_buttons:
                    if rect.collidepoint(event.pos):
                        change_layout(name)

                if reset_button.collidepoint(event.pos):
                    reset_search()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_1:
                run_search(bfs, "BFS")

            elif event.key == pygame.K_2:
                run_search(dfs, "DFS")

            elif event.key == pygame.K_3:
                run_search(greedy_best_first, "Greedy")

            elif event.key == pygame.K_4:
                run_search(astar, "A*")

            elif event.key == pygame.K_r:
                reset_search()

    # Animate exploration
    if animating:

        current_time = pygame.time.get_ticks()

        if current_time - last_animation_time >= animation_delay:

            if animation_index < len(explored_order):
                animation_index += 1
                last_animation_time = current_time

            if animation_index >= len(explored_order):
                animating = False

    draw_interface()
    clock.tick(60)


pygame.quit()
sys.exit()
