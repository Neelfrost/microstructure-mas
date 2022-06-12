# Author: Neel Basak
# Github: https://github.com/Neelfrost
# File: simulation.py
# License: GPL-3

from math import exp

import numpy as np


class Simulate:
    def __init__(self, matrix, temperature, grain_boundary_energy, boltz_const):
        """Simulate grain growth using Monte Carlo method.
        Assumption: Uniform mobilities and energies.
        Neighborhood: Moore

        Args:
            matrix (Matrix2D): Discrete matrix mapped to a microstructure.
            temperature (float): Simulation temperature.
            grain_boundary_energy (float): Grain boundary energy.
            boltz_const (float): Boltzmann constant.
        """
        self.matrix = matrix

        self.temperature = temperature
        self.grain_boundary_energy = grain_boundary_energy
        self.boltz_const = boltz_const

        self.nearest_neighbors = 8

        self.reorientation_attempts = 0
        self.mcs = 0

    def different_neighbors(self, lattice_site, orientation=None):
        """Calculate different neighbors (lattice sites with different orientation) of lattice site, or different
        neighbors of given lattice site with given orientation.

        Args:
            lattice_site (Tuple(int, int)): Coordinates of lattice site.
            orientation (int, optional): Use this orientation for calculation instead.

        Returns:
            List(int, List(int)): Number of different neighbors, list of orientations of different neighbors.

        """
        # Number of different neighbors
        total_different_neighbors = 0

        # Orientation of neighbors
        orientations = []

        # Iterate over neighbors (Moore configuration)
        for i in range(
            max(0, lattice_site[0] - 1),
            min(lattice_site[0] + 1, self.matrix.cols - 1) + 1,
        ):
            for j in range(
                max(0, lattice_site[1] - 1),
                min(lattice_site[1] + 1, self.matrix.rows - 1) + 1,
            ):
                if i != lattice_site[0] or j != lattice_site[1]:
                    if orientation is not None:
                        if self.matrix.grid[i][j] != orientation:
                            total_different_neighbors += 1
                    else:
                        if (
                            self.matrix.grid[i][j]
                            != self.matrix.grid[lattice_site[0]][lattice_site[1]]
                        ):
                            total_different_neighbors += 1
                            orientations.append(self.matrix.grid[i][j])
        # Remove duplicates
        orientations = list(set(orientations))

        return [total_different_neighbors, orientations]

    def calculate_free_energy(self, lattice_site, orientation=None):
        """Calculate free energy of given lattice site, or free energy of given lattice site with given
        orientation.

        Args:
            lattice_site (Tuple(int, int)): Coordinates of lattice site.
            orientation (int, optional): Use this orientation for calculation instead.

        Returns:
            float: Free energy of the given lattice site.

        """
        # Calculate current free energy
        free_energy = (
            self.grain_boundary_energy
            * self.different_neighbors(lattice_site, orientation)[0]
            - self.grain_boundary_energy * self.nearest_neighbors
        )
        return free_energy

    def transition_probability(self, delta_free_energy):
        """Calculate transition probability of reorientation attempt.

        Reorientation is always accepted when delta_free_energy <= 0.
        When temperature > 0, and delta_free_energy > 0 reorientation is accepted according to transition function.

        Args:
            delta_free_energy (int): Difference in free energy between current and new orientation.

        Returns:
            bool: True if reorientation is favorable.

        """
        if self.temperature != 0:
            return delta_free_energy <= 0 or np.random.uniform(0, 1) < exp(
                (-delta_free_energy / (self.boltz_const * self.temperature))
            )
        return delta_free_energy <= 0

    def reorient(self, lattice_site):
        """Using Monte Carlo method, assign new orientation (reorientation) to the given lattice site and thereby
        simulate grain growth.

        Args:
            lattice_site (Tuple(int, int)): Coordinates of lattice site.

        Returns:
            None
        """
        # Calculate current free energy
        current_free_energy = self.calculate_free_energy(lattice_site)

        # Get neighboring orientations
        orientations = self.different_neighbors(lattice_site)[1]

        if not orientations:
            return

        # Select a random orientation out of the orientations of the current neighbors
        new_orientation = np.random.choice(orientations)

        # Calculate free energy with orientation
        new_free_energy = self.calculate_free_energy(lattice_site, new_orientation)

        # Calculate change in free energy
        delta_free_energy = new_free_energy - current_free_energy

        # Assign new orientation if free energy is lower or transition probability is favorable
        # Increase reorientation attempts for each attempt, and calculate Monte Carlo steps
        if self.transition_probability(delta_free_energy):
            self.matrix.grid[lattice_site[0]][lattice_site[1]] = new_orientation
            self.reorientation_attempts += 1

        self.mcs = self.reorientation_attempts // (self.matrix.rows * self.matrix.cols)


