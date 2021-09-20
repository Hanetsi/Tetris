from typing import Union

import pygame
from pygame import Surface
from pygame.locals import *
from pygame.surface import SurfaceType

from src.colors import *

# GLOBAL CONSTANTS
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
PLAY_WIDTH = WINDOW_WIDTH / 2
PLAY_HEIGHT = WINDOW_HEIGHT
PLAY_LEFT = (WINDOW_WIDTH / 2) - (PLAY_WIDTH / 2)
INFO_WIDTH = WINDOW_WIDTH / 4
INFO_HEIGHT = WINDOW_HEIGHT
INFO_LEFT = WINDOW_WIDTH - INFO_WIDTH

BLOCK_SIZE = WINDOW_WIDTH / 20


class Background:
    def __init__(self, screen, color: tuple, x: float, y: float, width: float, height: float):
        self.screen = screen
        self.color = color
        self.pos = x, y
        self.width = width
        self.height = height

        self.bg = pygame.Surface((width, height))
        self.bg = self.bg.convert()
        self.bg.fill(self.color)

    def draw(self):
        self.screen.blit(self.bg, self.pos)

    def drawGrid(self):
        # Horizontal lines
        size = float(BLOCK_SIZE)
        for y in range(int(self.height / BLOCK_SIZE) + 1):
            row = (y * size)
            print(self.pos[0])
            pygame.draw.line(self.screen, RED, (self.pos[0], row), (self.pos[0] + self.width, row), width=2)

        for x in range(int(self.width / BLOCK_SIZE) + 1):
            col = (x * size) + self.pos[0]
            pygame.draw.line(self.screen, RED, (col, 0), (col, self.height), width=2)


class Tetris:
    screen: Union[Surface, SurfaceType]

    def __init__(self):
        self.initialise()

        self.backgrounds = self.make_backgrounds()
        self.pieces = []
        self.locked_positions = []

    def initialise(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tetris")

    def make_backgrounds(self):
        bgs = [Background(self.screen, BLACK, 0, 0, WINDOW_WIDTH, WINDOW_HEIGHT),
               Background(self.screen, WHITE, PLAY_LEFT, 0, PLAY_WIDTH, PLAY_HEIGHT),
               Background(self.screen, BLACK, INFO_LEFT, 0, INFO_WIDTH, INFO_HEIGHT)]
        return bgs

    def loop(self):
        while True:
            for bg in self.backgrounds:
                bg.draw()
            self.backgrounds[1].drawGrid()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == QUIT:
                    return


def main():
    tetris = Tetris()
    tetris.loop()


if __name__ == "__main__": main()
