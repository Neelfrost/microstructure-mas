from random import randint
import sys

import pygame as pg

from grid import Matrix2D
from iteration import Iter


RED = (224, 108, 117)
GREEN = (152, 195, 121)
BLUE = (96, 175, 238)
WHITE = (220, 223, 228)
BLACK = (40, 44, 52)


# Draws text 'comp' with font 'font' on canvas centered at x,y
def draw_char(canvas, font, color, text, x, y):
    text = font.render(str(text), True, color)
    canvas.blit(text, text.get_rect(center=(x, y)))


def get_shade(value, index):
    offset = 100
    shade = (255 - offset) / value
    return (offset + shade * index, offset + shade * index, offset + shade * index)


def main():
    pg.init()
    pg.display.set_caption("Grain Simulation")
    # icon = pg.image.load(resource_path("icon.png"))
    # pg.display.set_icon(icon)

    # font = pg.font.SysFont("arial", 8)
    # big_font = pg.font.SysFont("arial", 16)

    # Window size
    WIDTH = HEIGHT = 600
    SIZE = 600
    ORIENTATIONS = 300

    grid = Matrix2D(SIZE, SIZE, ORIENTATIONS, "sobol")
    growth = Iter(grid)

    grid_cell_size = int(WIDTH / SIZE)
    draw_grid_lines = False
    draw_grid_seeds = False

    canvas = pg.display.set_mode((WIDTH, HEIGHT))

    clock = pg.time.Clock()

    while True:
        # Clear canvas
        canvas.fill(WHITE)

        # Draw matrix
        for i in range(grid.cols):
            for j in range(grid.rows):
                # draw_char(
                #     canvas,
                #     font,
                #     BLACK,
                #     grid.grid[i][j],
                #     i * grid_cell_size + grid_cell_size / 2,
                #     j * grid_cell_size + grid_cell_size / 2,
                # )
                pg.draw.rect(
                    canvas,
                    get_shade(ORIENTATIONS, grid.grid[i][j]),
                    (i * grid_cell_size, j * grid_cell_size, grid_cell_size, grid_cell_size),
                )

        if draw_grid_seeds:
            for seed in grid.seed_loc:
                pg.draw.rect(
                    canvas,
                    (255, 0, 0),
                    (seed[0] * grid_cell_size, seed[1] * grid_cell_size, grid_cell_size, grid_cell_size),
                )

        # Draw gridlines
        if draw_grid_lines:
            for i in range(grid.cols):
                pg.draw.rect(canvas, BLACK, (0, grid_cell_size * i, WIDTH, 1))
                pg.draw.rect(canvas, BLACK, (grid_cell_size * i, 0, 1, HEIGHT))

        rand_x, rand_y = randint(0, grid.cols - 2), randint(0, grid.rows - 2)
        # growth.reorient((rand_x, rand_y))

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
