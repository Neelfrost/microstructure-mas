from math import log2

from alive_progress import alive_it
import numpy as np
from scipy.stats import qmc


class Matrix2D:

    seed_methods = ("pseudo", "sobol", "halton", "latin")

    def __init__(self, cols: int, rows: int, orientations: int, seed_method: str):
        self.cols = cols
        self.rows = rows
        self.orientations = orientations
        self.seed_method = seed_method if seed_method in Matrix2D.seed_methods else None
        self.grid = self.make_grid()
        self.create_grains()

    # Returns a 2d array initialized with zeros
    def make_grid(self) -> list[list[int]]:
        grid = []
        for i in range(self.cols):
            grid.append([])
            for _ in range(self.rows):
                grid[i].append(0)
        return grid

    # Prints 2d array
    def __str__(self):
        arr = []
        for col in self.grid:
            for cell in col:
                arr.append(str(cell) + ", ")
            arr.append("\n")
        return "".join(arr)

    # Calculates the distance between 2 cells
    def distance_between_cells(self, start, end):
        return (end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2

    # Creates seeds (grain centers)
    def create_seeds(self):
        # List of seed locations, tuple: (x, y)
        self.seed_loc = []
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
                self.seed_loc.append((seed_x, seed_y))

        # Low discrepancy seed selection
        else:
            # sobol's method
            if self.seed_method == "sobol":
                seed_generator = qmc.Sobol(d=1, scramble=True)
                seeds = seed_generator.random_base2(m=int(log2(self.orientations)))
            # halton's method
            if self.seed_method == "halton":
                seed_generator = qmc.Halton(d=1, scramble=True)
                seeds = seed_generator.random(n=self.orientations)
                np.random.shuffle(seeds)
            # latinhypercude method
            if self.seed_method == "latin":
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
                self.seed_loc.append((seed_x, seed_y))

    # Creates grains with specific orientations
    def create_zones(self):
        for i in alive_it(
            range(self.cols),
            title="\033[38;5;102mGenerating microstructure...",
            bar="blocks",
            spinner=None,
            stats=False,
            monitor=False,
        ):
            for j in range(self.rows):
                if self.grid[i][j] == 0:
                    pre_min_dist = min_dist = self.cols * self.rows
                    for seed in self.seed_loc:
                        distance_between_seed_cell = self.distance_between_cells(
                            (i, j), seed
                        )
                        if distance_between_seed_cell <= 128 ** 2:
                            pre_min_dist = min_dist
                            min_dist = min(pre_min_dist, distance_between_seed_cell)
                            if min_dist < pre_min_dist:
                                self.grid[i][j] = self.grid[seed[0]][seed[1]]
                        else:
                            continue

    def create_grains(self):
        self.create_seeds()
        self.create_zones()
