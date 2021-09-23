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
FALL_TIME = 500


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
        self.game_running = False
        self.initialise()
        self.play_bg_color = DARK_GRAY
        self.bg_color = BLACK
        self.info_bg_color = BLACK
        self.line_color = GRAY
        self.backgrounds = self.make_backgrounds()
        self.pieces = []
        self.score_for_cleared_lines = [40, 100, 300, 1200]
        self.font = pygame.font.SysFont("Comic Sans MS", 30)
        self.text_color = WHITE

        self.title_text = self.score_surface = self.font.render("TETRIS", False, WHITE)
        self.title_text_x = (PLAY_LEFT + PLAY_WIDTH/2) - (self.title_text.get_size()[0] / 2)
        self.title_text_y = self.title_text.get_size()[1]/2

        self.game_over_text = self.score_surface = self.font.render("GAME OVER", False, WHITE)
        self.game_over_text_x = (PLAY_LEFT + PLAY_WIDTH/2) - (self.game_over_text.get_size()[0] / 2)
        self.game_over_text_y = PLAY_TOP - self.game_over_text.get_size()[1]

        self.reset()

        self.clock = pygame.time.Clock()


    def initialise(self):
        pygame.init()
        pygame.font.init()
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

    def reset(self):
        self.score = 0
        self.score_surface = self.font.render("Score: " + str(self.score), False, WHITE)

        self.next_piece = self.new_piece()
        self.piece = self.get_next_piece()
        self.grid = self.empty_grid()
        self.next_piece_grid = [[self.bg_color for _ in range(5)] for _ in range(5)]
        self.locked_positions = self.empty_grid()

        self.game_running = True

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

    def display_next_piece(self):
        self.next_piece_grid = [[self.bg_color for _ in range(5)] for _ in range(5)]
        for position in self.next_piece.block_positions:
            self.next_piece_grid[position[0]][position[1]] = self.next_piece.color

    def draw_next_piece(self):
        for y, row in enumerate(self.next_piece_grid):
            for x, col in enumerate(row):
                color = col
                x_pos = (x * BLOCK_SIZE) + BLOCK_SIZE/2
                y_pos = (y * BLOCK_SIZE) + BLOCK_SIZE/2
                width = BLOCK_SIZE - LINE_WIDTH
                height = BLOCK_SIZE - LINE_WIDTH
                pygame.draw.rect(self.screen, color, (x_pos, y_pos, height, width))

    def new_piece(self):
        return random.choice(pieces.piece_types)()

    def get_next_piece(self):
        piece = self.next_piece
        self.next_piece = self.new_piece()
        return piece

    def lock_piece(self, piece):
        for position in piece.block_positions:
            self.locked_positions[piece.y + position[1]][piece.x + position[0]] = piece.color

    def game_over(self):
        self.game_running = False
        self.screen.blit(self.game_over_text, (self.game_over_text_x, self.game_over_text_y))

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
                    if piece.y == 0:
                        self.game_over()
                    return False
        return True

    def check_right(self, grid, piece):
        """Checks if piece hasd space to move right"""
        is_valid = True
        for position in piece.block_positions:
            col = piece.x + position[0]
            if col >= (len(grid[0]) - 1):
                is_valid = False
        return is_valid

    def check_lines(self):
        """Check if all elements in a row are not background. If so clear the line"""
        cleared = 0
        for i, row in enumerate(self.locked_positions):
            filled = 0
            for color in row:
                if color != self.play_bg_color:
                    filled += 1
            if filled == len(row):
                cleared += 1
                self.clear_line(i)
        if not cleared:
            return
        self.score += self.score_for_cleared_lines[cleared - 1]
        global FALL_TIME
        FALL_TIME -= (cleared * 10)
        self.score_surface = self.font.render("Score: " + str(self.score), False, WHITE)

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
        self.display_next_piece()
        self.draw_next_piece()
        self.draw_score()
        self.draw_title()
        self.backgrounds[1].draw_grid(self.line_color)

    def draw_title(self):
        self.screen.blit(self.title_text, (self.title_text_x, self.title_text_y))

    def draw_score(self):
        """Draws score on screen. Gets size again to count for different lengths of scores."""
        score_width = self.score_surface.get_size()[0]
        score_left = WINDOW_WIDTH - (INFO_WIDTH / 2) - (score_width / 2)
        self.screen.blit(self.score_surface, (score_left, score_width))

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
                    while not self.check_right(self.grid, self.piece):
                        self.piece.x -= 1
                if event.key == K_s:
                    while self.check_down(self.grid, self.piece):
                        self.piece.move_down()
                    else:
                        self.lock_piece(self.piece)
                        self.piece = self.get_next_piece()
                if event.key == K_r:
                    self.reset()
        return False

    def fall(self, time):
        time += self.clock.tick()
        if time > FALL_TIME:
            if self.check_down(self.grid, self.piece):
                self.piece.move_down()
                time = 0
            else:
                self.lock_piece(self.piece)
                self.piece = self.get_next_piece()
        return time

    def loop(self):
        time = 0
        while True:
            if self.game_running:
                self.draw_backgrounds()
            if self.handle_events():
                return

            if self.game_running:
                time = self.fall(time)
                self.clean_grid()
                self.display_piece(self.grid, self.piece)
                self.check_lines()
                self.draw_blocks()

            pygame.display.flip()


def main():
    tetris = Tetris()
    tetris.loop()


if __name__ == "__main__": main()
