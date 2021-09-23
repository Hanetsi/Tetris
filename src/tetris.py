from typing import Union

import pygame
import random
from pygame import Surface
from pygame.locals import *
from pygame.surface import SurfaceType

from src.colors import *

# GLOBAL CONSTANTS
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 1000
PLAY_WIDTH = WINDOW_WIDTH / 2
PLAY_HEIGHT = PLAY_WIDTH * 2
PLAY_TOP = WINDOW_HEIGHT - PLAY_HEIGHT
PLAY_LEFT = (WINDOW_WIDTH / 2) - (PLAY_WIDTH / 2)
INFO_WIDTH = WINDOW_WIDTH / 4
INFO_HEIGHT = WINDOW_HEIGHT
INFO_LEFT = WINDOW_WIDTH - INFO_WIDTH

BLOCK_SIZE = PLAY_WIDTH / 10
LINE_WIDTH = 5


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

    # TODO fix the upper corners
    def draw_grid(self, color: tuple):
        """Draws the lines from the bottom up."""
        self.draw_horizontal_lines(color)
        self.draw_vertical_lines(color)

    def draw_horizontal_lines(self, color: tuple) -> None:
        """Draws the lines from the bottom up."""
        left = self.pos[0] - (LINE_WIDTH / 2)
        right = left + LINE_WIDTH + self.width
        for y in range(int(self.height / BLOCK_SIZE) + 1):
            row = WINDOW_HEIGHT - (y * LINE_WIDTH) - (y * (BLOCK_SIZE - LINE_WIDTH)) - (LINE_WIDTH / 2)
            pygame.draw.line(self.screen, color, (left, row), (right, row), width=LINE_WIDTH)

    def draw_vertical_lines(self, color: tuple) -> None:
        """Draws the lines from the bottom up."""
        top = WINDOW_HEIGHT - PLAY_HEIGHT - (LINE_WIDTH / 2)
        bottom = WINDOW_HEIGHT
        for x in range(int(self.width / BLOCK_SIZE) + 1):
            x_pos = x * float(BLOCK_SIZE) + self.pos[0] - (LINE_WIDTH / 2) + (x * (LINE_WIDTH / 10))
            pygame.draw.line(self.screen, color, (x_pos, top), (x_pos, bottom), width=LINE_WIDTH)


class Tetris:
    screen: Union[Surface, SurfaceType]

    def __init__(self):
        self.initialise()

        self.backgrounds = self.make_backgrounds()
        self.pieces = []
        self.locked_positions = []

        self.grid = self.empty_grid()

    def initialise(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tetris")

    def make_backgrounds(self):
        bgs = [Background(self.screen, BLACK, 0, 0, WINDOW_WIDTH, WINDOW_HEIGHT),
               Background(self.screen, GRAY, PLAY_LEFT, PLAY_TOP, PLAY_WIDTH, PLAY_HEIGHT),
               Background(self.screen, BLACK, INFO_LEFT, 0, INFO_WIDTH, INFO_HEIGHT)]
        return bgs

    @staticmethod
    def empty_grid():
        rows = int(PLAY_HEIGHT / BLOCK_SIZE)
        cols = int(PLAY_WIDTH / BLOCK_SIZE)
        return [[(random.randint(0,255),random.randint(0,255),random.randint(0,255)) for _ in range(cols)] for _ in range(rows)]

    def draw_blocks(self):
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                color = col
                x_pos = PLAY_LEFT + (x * BLOCK_SIZE) + (x + LINE_WIDTH)
                y_pos = PLAY_TOP + (y * BLOCK_SIZE) + (y + LINE_WIDTH)
                width = BLOCK_SIZE - LINE_WIDTH
                height = BLOCK_SIZE - LINE_WIDTH
                pygame.draw.rect(self.screen, color, (x_pos, y_pos, height, width))

    def loop(self):
        while True:
            for bg in self.backgrounds:
                bg.draw()
            self.backgrounds[1].draw_grid(WHITE)
            # self.draw_blocks()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == QUIT:
                    return


def main():
    tetris = Tetris()
    tetris.loop()


if __name__ == "__main__": main()
