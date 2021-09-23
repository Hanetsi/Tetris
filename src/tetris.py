from typing import Union
import random
import pygame
from pygame import Surface
from pygame.locals import *
from pygame.surface import SurfaceType

from src.colors import *
import src.pieces as pieces

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
LINE_WIDTH = 2
FALL_TIME = 250


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
        right = left + self.width
        for y in range(int(self.height / BLOCK_SIZE) + 1):
            row = WINDOW_HEIGHT - (y * LINE_WIDTH) - (y * (BLOCK_SIZE - LINE_WIDTH)) - (LINE_WIDTH / 2)
            pygame.draw.line(self.screen, color, (left, row), (right, row), width=LINE_WIDTH)

    def draw_vertical_lines(self, color: tuple) -> None:
        """Draws the lines from the bottom up."""
        top = WINDOW_HEIGHT - PLAY_HEIGHT - (LINE_WIDTH / 2)
        bottom = WINDOW_HEIGHT
        for x in range(int(self.width / BLOCK_SIZE) + 1):
            x_pos = x * float(BLOCK_SIZE) + self.pos[0] - (LINE_WIDTH / 2)# + (x * (LINE_WIDTH / 10))
            pygame.draw.line(self.screen, color, (x_pos, top), (x_pos, bottom), width=LINE_WIDTH)


class Tetris:
    screen: Union[Surface, SurfaceType]

    def __init__(self):
        self.initialise()
        self.play_bg_color = DARK_GRAY
        self.bg_color = BLACK
        self.info_bg_color = BLACK
        self.line_color = GRAY
        self.backgrounds = self.make_backgrounds()
        self.pieces = []

        self.piece = self.new_piece()
        self.grid = self.empty_grid()
        self.locked_positions = self.empty_grid()

        self.clock = pygame.time.Clock()


    def initialise(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tetris")

    def make_backgrounds(self):
        bgs = [Background(self.screen, self.bg_color, 0, 0, WINDOW_WIDTH, WINDOW_HEIGHT),
               Background(self.screen, self.play_bg_color, PLAY_LEFT, PLAY_TOP, PLAY_WIDTH, PLAY_HEIGHT),
               Background(self.screen, self.info_bg_color, INFO_LEFT, 0, INFO_WIDTH, INFO_HEIGHT)]
        return bgs

    def empty_grid(self):
        rows = int(PLAY_HEIGHT / BLOCK_SIZE)
        cols = int(PLAY_WIDTH / BLOCK_SIZE)

        return [[self.play_bg_color for _ in range(cols)] for _ in range(rows)]

    def empty_line(self):
        cols = int(PLAY_WIDTH / BLOCK_SIZE)
        return [self.play_bg_color for _ in range(cols)]

    def clean_grid(self):
        for x, row in enumerate(self.locked_positions):
            for y, color in enumerate(row):
                if color != self.play_bg_color:
                    self.grid[x][y] = color
                else:
                    self.grid[x][y] = self.play_bg_color


    def draw_blocks(self):
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                color = col
                x_pos = PLAY_LEFT + (x * BLOCK_SIZE)
                y_pos = PLAY_TOP + (y * BLOCK_SIZE)
                width = BLOCK_SIZE - LINE_WIDTH
                height = BLOCK_SIZE - LINE_WIDTH
                pygame.draw.rect(self.screen, color, (x_pos, y_pos, height, width))

    def display_piece(self, grid, piece):
        """Insert copies a pieces color into grid according to shape of piece."""
        for position in piece.block_positions:
            grid[piece.y + position[1]][piece.x + position[0]] = piece.color

    def new_piece(self):
        return random.choice(pieces.piece_types)()

    def lock_piece(self, piece):
        for position in piece.block_positions:
            self.locked_positions[piece.y + position[1]][piece.x + position[0]] = piece.color

    def check_down(self, grid, piece):
        for position in piece.block_positions:
            row = piece.y + position[1]
            col = piece.x + position[0]
            if row >= (len(grid) - 1):
                return False
            color_below = grid[row + 1][col]

            if color_below != self.play_bg_color:
                color_in_locked_pos = self.locked_positions[row + 1][col]
                if color_in_locked_pos != self.play_bg_color:
                    return False
        return True

    def check_right(self, grid, piece):
        """Checks if piece hasd space to move right"""
        is_valid = True
        for position in piece.block_positions:
            col = piece.x + position[0]
            print(col, (len(grid[0]) - 1))
            if col >= (len(grid[0]) - 1):
                is_valid = False
        return is_valid

    def check_lines(self):
        """Check if all elements in a row are not background. If so clear the line"""
        for i, row in enumerate(self.locked_positions):
            filled = 0
            for color in row:
                if color != self.play_bg_color:
                    filled += 1
            if filled == len(row):
                print("clearing lines", i)
                self.clear_line(i)

    def clear_line(self, row_n):
        """Clears the given line and shuffles all remaining lines down 1 step.
        Also adds an empty line up top."""
        while row_n > 0:
            self.locked_positions[row_n] = self.locked_positions[row_n - 1]
            row_n -= 1
        self.locked_positions[0] = self.empty_line()

    def draw_backgrounds(self):
        for bg in self.backgrounds:
            bg.draw()
        self.backgrounds[1].draw_grid(self.line_color)

    def handle_events(self) -> bool:
        """Returns a bool. True if should quit"""
        for event in pygame.event.get():
            if event.type == QUIT:
                return True
            if event.type == KEYDOWN:
                if event.key == K_a and 0 < self.piece.x:
                    self.piece.move_left()
                if event.key == K_d and self.check_right(self.grid, self.piece):
                    self.piece.move_right()
                if event.key == K_w:
                    self.piece.rotate()
                if event.key == K_s:
                    while self.check_down(self.grid, self.piece):
                        self.piece.move_down()
                    else:
                        self.lock_piece(self.piece)
                        self.piece = self.new_piece()
        return False

    def movement(self, time):
        time += self.clock.tick()
        if time > FALL_TIME:
            if self.check_down(self.grid, self.piece):
                self.piece.move_down()
                time = 0
            else:
                self.lock_piece(self.piece)
                self.piece = self.new_piece()
        return time

    def loop(self):
        time = 0
        while True:
            self.draw_backgrounds()
            if self.handle_events():
                return

            time = self.movement(time)

            self.clean_grid()
            self.display_piece(self.grid, self.piece)
            self.check_lines()
            self.draw_blocks()

            pygame.display.flip()


def main():
    tetris = Tetris()
    tetris.loop()


if __name__ == "__main__": main()
