import argparse
import os
import sys

from alive_progress import alive_bar
from numpy import random

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"  # hide pygame startup banner

import pygame as pg

from matrix import Matrix2D
from matrix import Matrix2DFile
from simulation import Simulate


RED = (224, 108, 117)
GREEN = (152, 195, 121)
BLUE = (96, 175, 238)
WHITE = (220, 223, 228)
BLACK = (40, 44, 52)


# Fix file paths
def resource_path(relative_path):
    return os.path.join(os.path.abspath("."), relative_path)


# Get shade of gray
def get_shade(total_orientations, orientation):
    offset = 50
    shade = (255 - offset) / total_orientations
    return (
        offset + shade * orientation,
        offset + shade * orientation,
        offset + shade * orientation,
    )


# ------------------------------------ CLI ----------------------------------- #
def parser():  # {{{
    # Init parser
    parser = argparse.ArgumentParser(
        description="Generate microstructures and simulate their grain growth.",
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
        help="Simulate grain growth?",
        action="store_true",
    )
    parser.add_argument(
        "--save",
        dest="DUMP",
        default=False,
        help="Output generated microstructure to a file?",
        action="store_true",
    )
    parser.add_argument(
        "--load",
        dest="READ",
        help="Load microstructure data from a .json file",
    )

    # Return args namespace
    return parser.parse_args()  # }}}


# ----------------------------------- Main ----------------------------------- #
def main():  # {{{
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

    # Frame rate
    FRAMERATE = 12 if not simulate else 1024

    # Init microstructure
    if args.READ is None:
        grid = Matrix2D(SIZE, SIZE, ORIENTATIONS, METHOD)
    else:
        grid = Matrix2DFile(args.READ)
        GRID_CELL_SIZE = WIDTH // grid.cols
        ORIENTATIONS = grid.orientations

    # Save grid if "--save"
    if args.DUMP:
        grid.save_grid()

    # Init simulator
    simulator = Simulate(grid)

    # Setup pygame
    pg.init()
    pg.display.set_caption("Grain Simulation")
    # Set window icon
    icon = pg.image.load(resource_path("icon.png"))
    pg.display.set_icon(icon)
    # Create canvas
    canvas = pg.display.set_mode((WIDTH, HEIGHT))
    # Create clock
    clock = pg.time.Clock()

    with alive_bar(
        title="Running...", bar=None, monitor=None, stats=None, spinner="radioactive"
    ):
        while True:
            # Clear canvas
            canvas.fill(WHITE)

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

            # Simulate
            if simulate:
                simulator.reorient(
                    (
                        random.randint(0, grid.cols - 2),
                        random.randint(0, grid.rows - 2),
                    )
                )

            # Handle pygame events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    # Close window
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()
                    # Save grid
                    elif event.key == pg.K_s:
                        grid.save_grid()

            pg.display.update()
            clock.tick(FRAMERATE)  # }}}


if __name__ == "__main__":
    main()
