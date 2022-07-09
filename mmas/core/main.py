# Author: Neel Basak
# Github: https://github.com/Neelfrost
# File: main.py
# License: GPL-3

import os
import sys

from mmas.core.matrix import Matrix2D
from mmas.utils.parser import argparser
from pkg_resources import resource_filename
from tqdm import tqdm

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"  # hide pygame startup banner

import pygame as pg


def pad_left(content, amount):
    """Add leading zeros to given content.

    Args:
        content (any): Content to be left padded with zeros.
        amount (int): Final length of content (amount + len(content)).

    Returns:
        str: Left padded content.
    """
    if isinstance(content, str):
        return content.zfill(amount)

    return str(content).zfill(amount)


def unique_name(options, time, extension):
    """Generate a unique name.

    Args:
        options (list): options used to generate the microstructure.
        time (int): time passed since the start of the program.
        extension (str): file extension of the image.

    Returns:
        str: Unique filename.
    """
    return (
        f"micro_{'_'.join(f'{str(option)}{str(options.get(option))}' for option in options)}"
        f"_t{str(time)}.{extension}"
    )


def save_snapshot(canvas, width, cell_size, method, orientations, time, mcs):
    """Pygame pygame.image.save wrapper.

    Args:
        canvas (Surface): Pygame surface object.
        width (int): Window width in pixels.
        cell_size (int): Cell size.
        method (str): Total/maximum orientations possible within in the microstructure.
        orientations (int): Method used to create voronoi seeds.
        time (int): Time elapsed since start.
    """
    pg.image.save(
        canvas,
        os.path.join(
            os.path.abspath("."),
            unique_name(
                {
                    "w": width,
                    "c": cell_size,
                    "m": method,
                    "o": orientations,
                    "mcs": pad_left(mcs, 4),
                },
                pad_left(time, 6),
                "png",
            ),
        ),
    )


def main():
    # Parse arguments
    args = argparser()
    args_dict = vars(args)

    # Framerate
    FRAMERATE = 60

    if args.load:
        data = Matrix2D.load(args.load)
        # Override simulation parameters if provided
        data.update(
            {
                "temperature": args.temperature,
                "grain_boundary_energy": args.grain_boundary_energy,
                "boltz_const": args.boltz_const,
            }
        )
        WIDTH = data.get("rows") * data.get("grid_cell_size")
        GRID_CELL_SIZE = min(WIDTH, max(data.get("grid_cell_size"), 1))
    else:
        # Window size
        WIDTH = args.width

        # Size of a cell, lower = sharper edges
        GRID_CELL_SIZE = min(WIDTH, max(args.grid_cell_size, 1))

        # Number of cols, rows
        SIZE = WIDTH // GRID_CELL_SIZE

        data = args_dict.copy()
        data.update(
            {
                "rows": SIZE,
                "cols": SIZE,
                "grid_cell_size": GRID_CELL_SIZE,
            }
        )

    # Create microstructure
    grid = Matrix2D(data)

    if args.save:
        grid.save()

    # Setup pygame
    pg.init()
    pg.display.set_caption("Microstructure Modeling & Simulation")

    # Set application window icon
    pg.display.set_icon(
        pg.image.load(resource_filename(__name__, "../assets/icon.png"))
    )

    # Create canvas
    canvas = pg.display.set_mode((WIDTH, WIDTH))

    # Create clock
    clock = pg.time.Clock()

    # Draw matrix (microstructure) once to capture an image
    grid.render(canvas, colored=args.color)

    # Save the image of microstructure at current time
    if args.snapshot != 0:
        # Capture microstructures every _ seconds
        time_in_seconds = args.snapshot
        pg.time.set_timer(pg.USEREVENT, time_in_seconds * 1000)

        save_snapshot(
            canvas,
            WIDTH,
            GRID_CELL_SIZE,
            data.get("seed_method"),
            data.get("orientations"),
            0,
            grid.simulator.mcs,
        )

    with tqdm(
        bar_format="{desc} {elapsed}",
        desc="\N{ESC}[38;5;93;1mRunning...\N{ESC}[0m",
    ) as pbar:
        while True:
            # Simulate grain growth
            grid.simulate(simulate=args.simulate)

            # Draw matrix (microstructure)
            grid.render(canvas, colored=args.color)

            # Handle pygame events
            for event in pg.event.get():
                if event.type == pg.USEREVENT and (
                    args.snapshot != 0 and args.simulate
                ):
                    # Save the image of microstructure at current time
                    save_snapshot(
                        canvas,
                        WIDTH,
                        GRID_CELL_SIZE,
                        data.get("seed_method"),
                        data.get("orientations"),
                        pg.time.get_ticks() // 1000,
                        grid.simulator.mcs,
                    )
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    # Close window when 'Esc' is pressed
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()

            pg.display.update()
            clock.tick(FRAMERATE)
            pbar.update()


