import argparse
import os
from random import randint
import sys

from alive_progress import alive_bar

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"  # hide pygame startup banner

import pygame as pg

from matrix import Matrix2D
from simulation import Simulate


RED = (224, 108, 117)
GREEN = (152, 195, 121)
BLUE = (96, 175, 238)
WHITE = (220, 223, 228)
BLACK = (40, 44, 52)


# Fix imports
# https://stackoverflow.com/questions/40716346/windows-pyinstaller-error-failed-to-execute-script-when-app-clicked
def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# Draws text 'text' with font 'font' on canvas centered at x,y
def draw_char(canvas, font, color, text, x, y):
    text = font.render(str(text), True, color)
    canvas.blit(text, text.get_rect(center=(x, y)))


# Get shade of gray
def get_shade(total_orientations, orientation):
    offset = 50
    shade = (255 - offset) / total_orientations
    return (
        offset + shade * orientation,
        offset + shade * orientation,
        offset + shade * orientation,
    )


# Setup cli
def parser():  # {{{
    # Init parser
    parser = argparse.ArgumentParser(
        description="Generate microstructures and simulate their grain growth."
    )

    # Add args
    parser.add_argument(
        "-w",
        dest="WIDTH",
        default=500,
        type=int,
        help="Window size. (default: 500)",
    )
    parser.add_argument(
        "-c",
        dest="CELL_SIZE",
        default=5,
        type=int,
        help="Cell size. Lower = more anti-aliased. (default: 5, recommended: 1-10)",
    )
    parser.add_argument(
        "-o",
        dest="ORIENTATIONS",
        default=100,
        type=int,
        help="Inital grain size. Higher = Smaller grains. (default: 100)",
    )
    parser.add_argument(
        "-m",
        dest="METHOD",
        default="sobol",
        choices=("pseudo", "sobol", "halton", "latin"),
        type=str,
        help="Seed generation algorithm. (default: sobol)",
    )
    parser.add_argument(
        "--simulate",
        dest="SIMULATE",
        default=False,
        type=bool,
        help="Simulate grain growth?",
        action=argparse.BooleanOptionalAction,
    )

    # Return args namespace
    return parser.parse_args()  # }}}


def main():
    # Process arguments
    args = parser()

    # Window size
    WIDTH = HEIGHT = args.WIDTH

    # Size of a cell (i.e., resolution), lower = more anti-aliased
    GRID_CELL_SIZE = min(WIDTH, max(args.CELL_SIZE, 1))

    # Number of cols, rows
    SIZE = WIDTH // GRID_CELL_SIZE

    # Seed generation algorithm
    METHOD = args.METHOD

    # Grain size
    ORIENTATIONS = args.ORIENTATIONS

    # Bools
    simulate = args.SIMULATE
    draw_grid_lines = False
    draw_grid_seeds = False

    # Init microstructure
    grid = Matrix2D(SIZE, SIZE, ORIENTATIONS, METHOD)

    # Init simulator
    simulator = Simulate(grid)

    # Init pygame
    pg.init()
    pg.display.set_caption("Grain Simulation")

    # Set window icon
    icon = pg.image.load(resource_path("icon.png"))
    pg.display.set_icon(icon)

    # Set font
    font = pg.font.SysFont("arial", 8)

    canvas = pg.display.set_mode((WIDTH, HEIGHT))

    clock = pg.time.Clock()

    with alive_bar(
        title="Running...", bar=None, monitor=None, stats=None, spinner="radioactive"
    ):
        while True:
            # Clear canvas
            canvas.fill(WHITE)

            # Draw matrix with numbers{{{
            # for i in range(grid.cols):
            #     for j in range(grid.rows):
            #         draw_char(
            #             canvas,
            #             font,
            #             BLACK,
            #             grid.grid[i][j],
            #             i * grid_cell_size + grid_cell_size / 2,
            #             j * grid_cell_size + grid_cell_size / 2,
            #         )}}}

            # Draw matrix
            for i in range(grid.cols):
                for j in range(grid.rows):
                    pg.draw.rect(
                        canvas,
                        get_shade(ORIENTATIONS, grid.grid[i][j]),
                        (
                            i * GRID_CELL_SIZE,
                            j * GRID_CELL_SIZE,
                            GRID_CELL_SIZE,
                            GRID_CELL_SIZE,
                        ),
                    )

            # Draw grain centers
            if draw_grid_seeds:
                for seed in grid.seed_loc:
                    pg.draw.rect(
                        canvas,
                        (255, 0, 0),
                        (
                            seed[0] * GRID_CELL_SIZE,
                            seed[1] * GRID_CELL_SIZE,
                            GRID_CELL_SIZE,
                            GRID_CELL_SIZE,
                        ),
                    )

            # Draw gridlines
            if draw_grid_lines:
                for i in range(grid.cols):
                    pg.draw.rect(canvas, BLACK, (0, GRID_CELL_SIZE * i, WIDTH, 1))
                    pg.draw.rect(canvas, BLACK, (GRID_CELL_SIZE * i, 0, 1, HEIGHT))

            # Simulate
            if simulate:
                simulator.reorient(
                    (randint(0, grid.cols - 2), randint(0, grid.rows - 2))
                )

            # Handle pygame events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()

            pg.display.update()
            clock.tick(1024)


if __name__ == "__main__":
    main()
