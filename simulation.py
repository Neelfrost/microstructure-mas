class Simulate:
    def __init__(self, grid):
        self.grid = grid
        self.grain_boundary_energy = 1
        self.temperature = 0
        self.boltz_const = 1
        self.nearest_neighbors = 8

    # Calculate neighbors with different lattice orientation of given lattice site
    def different_neighbors(self, lattice_site, orientation=None):
        total_different_neighbors = 0  # Number of different neighbors
        orientations = []  # List of orientation of neighbors
        # Iterate over neighbors
        for i in range(
            max(0, lattice_site[0] - 1), min(lattice_site[0] + 1, self.grid.cols) + 1
        ):
            for j in range(
                max(0, lattice_site[1] - 1),
                min(lattice_site[1] + 1, self.grid.rows) + 1,
            ):
                if i != lattice_site[0] or j != lattice_site[1]:
                    # If orientation is provided
                    if orientation is not None:
                        # Check with orientation
                        if self.grid.grid[i][j] != orientation:
                            total_different_neighbors += 1
                    else:
                        # Else check with given lattice site
                        if (
                            self.grid.grid[i][j]
                            != self.grid.grid[lattice_site[0]][lattice_site[1]]
                        ):
                            total_different_neighbors += 1
                            orientations.append(self.grid.grid[i][j])
        orientations = list(set(orientations))
        return [total_different_neighbors, orientations]

    # Calculate free energy of given lattice site or with given orientation
    def calculate_free_energy(self, lattice_site, orientation=None):
        # Calculate current free energy
        free_energy = (
            self.grain_boundary_energy * self.nearest_neighbors
            - self.grain_boundary_energy
            * self.different_neighbors(lattice_site, orientation)[0]
        )
        return free_energy

    # Reorient given lattice site if feasible
    def reorient(self, lattice_site):
        # Calculate current free energy
        current_free_energy = self.calculate_free_energy(lattice_site)

        # Try to assign new orientation
        orientations = self.different_neighbors(lattice_site)[1]
        if orientations:
            for orientation in orientations:
                # Calculate free energy with orientation
                possible_free_energy = self.calculate_free_energy(
                    lattice_site, orientation
                )

                # Calculate change in free energy
                delta_free_energy = possible_free_energy - current_free_energy

                # TODO: implement transition probability
                # self.transition_probability

                # Assign orientation if free energy is lower
                if delta_free_energy <= 0:
                    # print(f"{delta_free_energy=}, {orientations=}, {orientation=}")
                    self.grid.grid[lattice_site[0]][lattice_site[1]] = orientation
