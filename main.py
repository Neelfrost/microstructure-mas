import argparse
import os
import sys

from alive_progress import alive_bar

from matrix import Matrix2D, Matrix2DFile

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"  # hide pygame startup banner

import pygame as pg


# ------------------------------------ CLI ----------------------------------- #
def parser():
    # Init parser
    parser = argparse.ArgumentParser(
        description="Generate microstructures and simulate their grain growth.",
    )
    # Add args
    parser.add_argument(
        "-w",
        "--width",
        dest="width",
        default=500,
        type=int,
        help="Window size. (default: 500)",
    )
    parser.add_argument(
        "-c",
        "--cell-size",
        dest="cell_size",
        default=5,
        type=int,
        help="Cell size. Lower = more anti-aliased. (default: 5, recommended: 1-10)",
    )
    parser.add_argument(
        "-o",
        "--orientations",
        dest="orientations",
        default=100,
        type=int,
        help="Inital grain size. Higher = Smaller grains. (default: 100)",
    )
    parser.add_argument(
        "-m",
        "--method",
        # dest="method",
        default="sobol",
        choices=("pseudo", "sobol", "halton", "latin"),
        type=str,
        help="Seed generation algorithm. (default: sobol)",
    )
    parser.add_argument(
        "--simulate",
        # dest="simulate",
        default=False,
        help="Simulate grain growth?",
        action="store_true",
    )
    parser.add_argument(
        "--color",
        # dest="color",
        default=False,
        help="Show colored grains instead of gray scale",
        action="store_true",
    )
    parser.add_argument(
        "--save",
        # dest="dump",
        default=False,
        help="Output generated microstructure to a file?",
        action="store_true",
    )
    parser.add_argument(
        "--load",
        # dest="read",
        help="Load microstructure data from a .json file",
    )

    # Return args namespace
    return parser.parse_args()


# ----------------------------------- Main ----------------------------------- #
def main():
    # Process arguments
    args = parser()

    # Window size
    WIDTH = HEIGHT = args.width

    # Size of a cell (i.e., resolution), lower = more anti-aliased
    GRID_CELL_SIZE = min(WIDTH, max(args.cell_size, 1))

    # Number of cols, rows
    SIZE = WIDTH // GRID_CELL_SIZE

    # Seed generation algorithm
    METHOD = args.method

    # Grain size
    ORIENTATIONS = args.orientations

    # Framerate
    FRAMERATE = 30

    # Init microstructure
    if args.load is None:
        grid = Matrix2D(SIZE, SIZE, ORIENTATIONS, METHOD)
    else:
        grid = Matrix2DFile(args.load)
        GRID_CELL_SIZE = WIDTH // grid.cols
        ORIENTATIONS = grid.orientations

    # Save grid if "--save"
    if args.save:
        grid.save_grid()

    # Setup pygame
    pg.init()
    pg.display.set_caption("Microstructure Simulation")

    # Set application window icon
    icon = pg.image.load(os.path.join(os.path.abspath("."), "icon.png"))
    pg.display.set_icon(icon)

    # Create canvas
    canvas = pg.display.set_mode((WIDTH, HEIGHT))

    # Create clock
    clock = pg.time.Clock()

    # Clear canvas
    canvas.fill((220, 223, 228))

    with alive_bar(
        title="Running...", bar=None, monitor=None, stats=None, spinner=None
    ):
        while True:
            # Simulate grain growth
            grid.simulate(simulate=args.simulate)

            # Draw matrix (microstructure)
            grid.render(canvas, GRID_CELL_SIZE, colored=args.color)

            # Handle pygame events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    # Close window when 'Esc' is pressed
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()
                    # Save grid when 's' is pressed
                    elif event.key == pg.K_s:
                        grid.save_grid()

            pg.display.update()
            clock.tick(FRAMERATE)


if __name__ == "__main__":
    main()
