# Author: Neel Basak
# Github: https://github.com/Neelfrost
# File: matrix.py
# License: GPL-3

import json
import os
from math import ceil, log2
from uuid import uuid4

import numpy as np
from mmas.core.simulation import Simulate
from scipy.stats import qmc
from tqdm import trange

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"  # hide pygame startup banner

import pygame as pg
import pygame.gfxdraw as gfxdraw
from pygame.math import Vector2


class Matrix2D:
    def __init__(self, data):
        """Discrete matrix constructor.

        Each cell of the grid belongs to a voronoi region i.e., a grain.

        Args:
            data (Dict): Dictionary containing the following data:
                cols, rows, cell_size, orientations, seed_method, temperature, grain_boundary_energy, boltz_const
                optionally: seeds, grid, grain_colors

        """
        self.cols = data.get("cols")
        self.rows = data.get("rows")
        self.cell_size = data.get("grid_cell_size")
        self.orientations = data.get("orientations")
        self.seed_method = data.get("seed_method")
        self.temperature = data.get("temperature")
        self.grain_boundary_energy = data.get("grain_boundary_energy")
        self.boltz_const = data.get("boltz_const")

        # List of seed locations, List[Vector2(x, y),].
        self.seeds = data.get("seeds", [])

        # Create a 2D array of size cols x rows initialized with zeros.
        self.grid = data.get("grid", [[0] * self.rows for _ in range(self.cols)])

        # Turn the empty grid into a voronoi diagram.
        if not data.get("grid"):
            self.create_microstructure()

        # Generate random/unique colors for each individual orientation.
        self.grain_colors = data.get(
            "grain_colors",
            np.random.randint(0, 256, size=(max(map(max, self.grid)), 3)),
        )

        # Create a simulator object to simulate grain growth/refinement.
        self.simulator = Simulate(
            self, self.temperature, self.grain_boundary_energy, self.boltz_const
        )

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
        for i in trange(
            self.cols,
            ascii=" ∙□■",
            bar_format="{desc} |{bar:50}| {elapsed}",
            desc="\N{ESC}[38;5;93;1m" + "Generating microstructure..." + "\N{ESC}[0m",
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

    def render(self, canvas, colored=False):
        """Draw the matrix (microstructure) with or without colored grains.

        Args:
            canvas (pygame.display): Pygame display.
            cell_size (int): Size of cells.
            colored (boolean): Should grains be colored? Default: grayscale grains.
        """
        if self.cell_size == 1:
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
                            i * self.cell_size,
                            j * self.cell_size,
                            self.cell_size,
                            self.cell_size,
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

    def save(self):
        """Save the attributes of the matrix/microstructure as a json file in the current working directory."""
        file_name = f"mmas_{uuid4().hex}.json"

        output = {
            "cols": self.cols,
            "rows": self.rows,
            "grid_cell_size": self.cell_size,
            "orientations": self.orientations,
            "seed_method": self.seed_method,
            "grid": self.grid,
            # Convert to list of list since Vector2 is not serializable
            "seeds": list(map(list, self.seeds)),
            # Convert to list since ndarray is not serializable
            "grain_colors": self.grain_colors.tolist(),
            "temperature": self.temperature,
            "grain_boundary_energy": self.grain_boundary_energy,
            "boltz_const": self.boltz_const,
        }

        with open(file_name, "w+") as file:
            json.dump(output, file, separators=(",", ":"))

        print(
            "\N{ESC}[38;5;93;1m"
            + "Microstructure data saved as: "
            + "\N{ESC}[0m"
            + f"{os.path.relpath(file_name)}"
        )

    @staticmethod
    def load(file_name):
        """Load the attributes of the matrix/microstructure from a json file in the current working directory."""
        with open(file_name, "r") as file:
            print(
                "\N{ESC}[38;5;93;1m"
                + "Microstructure data loaded from: "
                + "\N{ESC}[0m"
                + f"{os.path.relpath(file_name)}"
            )
            return json.load(file)
