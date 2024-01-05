import pygame
from car import Car
from utils import (
    get_mask_outline,
    make_outline_loops,
    tranform_points_to_lines,
    euchlidean_distance,
)
import numpy as np

FPS = 60


class Game:
    def __init__(self, local=False) -> None:
        pygame.init()
        self.local = local
        self.running = True

        self.track = open("track").read().splitlines()
        self.cell_size = 50
        self.height = len(self.track) * self.cell_size
        self.width = len(self.track[0]) * self.cell_size

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

    def draw_track(self):
        for y in range(self.height):
            for x in range(self.width):
                cell = self.track[y][x]
                if cell == "1":
                    pygame.draw.rect(
                        self.screen,
                        "gray",
                        (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size),
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        "darkgreen",
                        (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size),
                        
                    )
                pygame.draw.rect(
                    self.screen,
                    "white",
                    (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size),
                    1
                )
    def draw(self):
        self.draw_track()

    def run(self):
        self.draw()

    def flip(self):
        pygame.display.flip()
        dt = self.clock.tick(FPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        if not self.running:
            pygame.quit()


if __name__ == "__main__":
    game = Game(local=True)
    while game.running:
        game.run()
        game.flip()
