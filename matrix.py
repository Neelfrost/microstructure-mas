import json
import os
from math import log2
from random import randint
from time import time

import numpy as np
from alive_progress import alive_it
from scipy.stats import qmc

from simulation import Simulate

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"  # hide pygame startup banner

import pygame as pg
import pygame.gfxdraw as gfxdraw
from pygame.math import Vector2


class Matrix2D:
    def __init__(self, cols: int, rows: int, orientations: int, seed_method: str):
        """Discrete matrix constructor.

        Each cell of the grid belongs to a voronoi region i.e., a grain.

        Args:
            cols (int): Number of columns.
            rows (int): Number of rows.
            orientations (int): Total/maximum orientations possible within in the microstructure.
            seed_method (str): Method used to create voronoi seeds.
        """
        self.cols = cols
        self.rows = rows
        self.orientations = orientations
        self.seed_method = seed_method

        # List of seed locations, List[Vector2(x, y),].
        self.seeds = []

        # Create a 2D array of size cols x rows initialized with zeros.
        self.grid = [[0] * self.rows for _ in range(self.cols)]

        # Turn the empty grid into a voronoi diagram.
        self.create_microstructure()

        # Generate random/unique colors for each individual orientation.
        self.grain_colors = [
            (randint(0, 255), randint(0, 255), randint(0, 255))
            for _ in range(10 + max(map(max, self.grid)))
        ]

        # Create a simulator object to simulate grain growth/refinement.
        self.simulator = Simulate(self)

    def __str__(self):
        """Convert the matrix into a string so that 'print()' can be used.

        Returns:
            str: String representation of the matrix.

        """
        arr = []
        for col in self.grid:
            for cell in col:
                arr.append(str(cell) + ", ")
            arr.append("\n")
        return "".join(arr)

    def save_grid(self):
        """Save the attributes of the current matrix (microstructure) in a '.json' file."""
        file_name = f"{self.seed_method}:{self.orientations}_{str(int(time()))}.json"
        output_dict = {
            "cols": self.cols,
            "rows": self.rows,
            "orientations": self.orientations,
            "grid": self.grid,
        }
        with open(file_name, "w+") as file:
            json.dump(output_dict, file, separators=(",", ":"))
        print(f"Microstructure data saved as: {file_name}")

    def create_seeds(self):
        """Randomly distribute seeds within the matrix using various methods."""
        seeds = np.empty(1)
        # pseudo random seed selection
        if self.seed_method == "pseudo":
            seeds = np.random.randint(0, self.cols * self.rows, self.orientations)

            # Get an iterator for np array
            seeds_itr = np.nditer(seeds, flags=["f_index"])

            # Append seed locations
            for seed in seeds_itr:
                seed_x = int(seed / self.cols)
                seed_y = seed % self.rows
                self.grid[seed_x][seed_y] = seeds_itr.index + 1
                self.seeds.append(Vector2(seed_x, seed_y))

        # Low discrepancy seed selection
        else:
            # sobol's method
            if self.seed_method == "sobol":
                seed_generator = qmc.Sobol(d=1, scramble=True)
                seeds = seed_generator.random_base2(m=int(log2(self.orientations)))
            # halton's method
            elif self.seed_method == "halton":
                seed_generator = qmc.Halton(d=1, scramble=True)
                seeds = seed_generator.random(n=self.orientations)
                np.random.shuffle(seeds)
            # latin-hypercude method
            elif self.seed_method == "latin":
                seed_generator = qmc.LatinHypercube(d=1)
                seeds = seed_generator.random(n=self.orientations)
                np.random.shuffle(seeds)

            # Get an iterator for np array
            seeds_itr = np.nditer(seeds, flags=["f_index"])

            # Append seed locations
            for seed in seeds_itr:
                seed = int(seed * self.cols * self.rows)
                seed_x = int(seed / self.cols)
                seed_y = seed % self.rows
                self.grid[seed_x][seed_y] = seeds_itr.index + 1
                self.seeds.append(Vector2(seed_x, seed_y))

    def get_nearest_seed(self, x, y):
        """Calculates seed nearest to the current cell

        Args:
            x (int): x coordinate of current cell
            y (int): y coordinate of current cell

        Returns:
            Vector2: nearest seed

        """

        nearest_seed = Vector2()
        min_dist = self.cols * self.rows

        for seed in self.seeds:
            distance_between_seed_and_current_cell = Vector2(x, y).distance_squared_to(
                seed
            )

            if distance_between_seed_and_current_cell < min_dist:
                min_dist = distance_between_seed_and_current_cell
                nearest_seed = seed

        return nearest_seed

    def create_grains(self):
        """Create voronoi regions (grains) using the seed locations. Each region belongs to a specific crystallographic
        orientation."""
        for i in alive_it(
            range(self.cols),
            title="Generating microstructure...",
            bar="blocks",
            spinner=None,
            stats=False,
            monitor=False,
        ):
            for j in range(self.rows):
                if self.grid[i][j] != 0:
                    continue

                nearest_seed = self.get_nearest_seed(i, j)
                self.grid[i][j] = self.grid[int(nearest_seed.x)][int(nearest_seed.y)]

    def create_microstructure(self):
        self.create_seeds()
        self.create_grains()

    def get_grayscale(self, current_orientation):
        """Basically maps the range (1, self.orientations) to (0, 255).

        Args:
            current_orientation (int): Orientation value of current cell.

        Returns: Tuple(int, int, int): Grayscale color corresponding to orientation of the cell.

        """
        shade = ((current_orientation - 1) * 255) // (self.orientations - 1)
        return (shade, shade, shade)

    def render(self, canvas, cell_size, colored=False):
        """Draw the matrix (microstructure) with or without colored grains.

        Args:
            canvas (pygame.display): Pygame display.
            cell_size (int): Size of cells.
            colored (boolean): Should grains be colored? Default: grayscale grains.
        """
        if cell_size == 1:
            for i in range(self.cols):
                for j in range(self.rows):
                    gfxdraw.pixel(
                        canvas,
                        i,
                        j,
                        self.grain_colors[min(self.grid[i][j], self.orientations - 1)]
                        if colored
                        else self.get_grayscale(self.grid[i][j]),
                    )
            for seed in self.seeds:
                gfxdraw.pixel(canvas, int(seed.x), int(seed.y), (255, 0, 0))
        else:
            for i in range(self.cols):
                for j in range(self.rows):
                    pg.draw.rect(
                        canvas,
                        self.grain_colors[min(self.grid[i][j], self.orientations - 1)]
                        if colored
                        else self.get_grayscale(self.grid[i][j]),
                        (
                            i * cell_size,
                            j * cell_size,
                            cell_size,
                            cell_size,
                        ),
                    )

    def simulate(self, simulate=False):
        """Simulate Monte Carlo Grain Growth.

        Args:
            simulate (boolean): Run simulation?

        """
        if not simulate:
            return

        for i in range(1000):
            self.simulator.reorient(
                (
                    np.random.randint(0, self.cols - 1),
                    np.random.randint(0, self.rows - 1),
                )
            )


class Matrix2DFile(Matrix2D):
    def __init__(self, file_name):
        with open(file_name, "r") as file:
            input_dict = json.load(file)
        self.cols = input_dict["cols"]
        self.rows = input_dict["rows"]
        self.orientations = input_dict["orientations"]
        self.grid = input_dict["grid"]


# vim:foldnestmax=3
