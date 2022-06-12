# Author: Neel Basak
# Github: https://github.com/Neelfrost
# File: matrix.py
# License: GPL-3

import os
from math import ceil, log2

import numpy as np
from alive_progress import alive_it
from scipy.stats import qmc

from mmas.core.simulation import Simulate

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"  # hide pygame startup banner

import pygame as pg
import pygame.gfxdraw as gfxdraw
from pygame.math import Vector2


class Matrix2D:
    def __init__(
        self,
        cols: int,
        rows: int,
        orientations: int,
        seed_method: str,
        temperature: float,
        grain_boundary_energy: float,
        boltz_const: float,
    ):
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
        self.grain_colors = np.random.randint(
            0, 256, size=(max(map(max, self.grid)), 3)
        )

        # Create a simulator object to simulate grain growth/refinement.
        self.simulator = Simulate(self, temperature, grain_boundary_energy, boltz_const)

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
                seeds = seed_generator.random_base2(m=ceil(log2(self.orientations)))
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
        # Work around for sobol sequence:
        if self.seed_method == "sobol":
            max_orientations = len(self.seeds)
        else:
            max_orientations = self.orientations

        shade = ((current_orientation - 1) * 255) // (max_orientations - 1)
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

        pg.display.set_caption(
            f"Microstructure Modeling & Simulation MCS: {self.simulator.mcs}"
        )
        for _ in range(1000):
            self.simulator.reorient(
                (
                    np.random.randint(0, self.cols),
                    np.random.randint(0, self.rows),
                )
            )


