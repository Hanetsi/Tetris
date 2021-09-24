import random
import pygame
from pygame.locals import *
from enum import Enum, auto

try:
    from src.colors import *
    import src.pieces as pieces
except ModuleNotFoundError:
    from colors import *
    import pieces

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
PLAY_WIDTH = 300
PLAY_HEIGHT = PLAY_WIDTH * 2
PLAY_TOP = WINDOW_HEIGHT - PLAY_HEIGHT
PLAY_LEFT = (WINDOW_WIDTH / 2) - (PLAY_WIDTH / 2)
INFO_WIDTH = WINDOW_WIDTH / 4
INFO_HEIGHT = WINDOW_HEIGHT
INFO_LEFT = WINDOW_WIDTH - INFO_WIDTH

BLOCK_SIZE = PLAY_WIDTH / 10
LINE_WIDTH = 2
FALL_TIME = 500


class GameState(Enum):
    SPLASH = auto()
    SETTINGS = auto()
    PLAYING = auto()
    GAMEOVER = auto()


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
        """Draws the horizontal lines from the bottom up."""
        left = self.pos[0] - (LINE_WIDTH / 2)
        right = left + self.width
        for y in range(int(self.height / BLOCK_SIZE) + 1):
            row = WINDOW_HEIGHT - (y * LINE_WIDTH) - (y * (BLOCK_SIZE - LINE_WIDTH)) - (LINE_WIDTH / 2)
            pygame.draw.line(self.screen, color, (left, row), (right, row), width=LINE_WIDTH)

    def draw_vertical_lines(self, color: tuple) -> None:
        """Draws the vertical lines from the bottom up."""
        top = WINDOW_HEIGHT - PLAY_HEIGHT - (LINE_WIDTH / 2)
        bottom = WINDOW_HEIGHT
        for x in range(int(self.width / BLOCK_SIZE) + 1):
            x_pos = x * float(BLOCK_SIZE) + self.pos[0] - (LINE_WIDTH / 2)
            pygame.draw.line(self.screen, color, (x_pos, top), (x_pos, bottom), width=LINE_WIDTH)


# TODO implement
class Text:
    pygame.font.init()
    font = pygame.font.Font("../tetris_block.ttf", 30)

    def __init__(self, screen, text: str, color: tuple, topleft: tuple, downright: tuple):
        self.screen = screen
        self.text = text
        self.color = color
        self.topleft = topleft
        self.downright = downright
        # Initial value for x and y
        self.x, y = self.topleft[0], self.topleft[1]
        self.surface = self.font.render(text, False, WHITE)
        self.center()

    def draw(self):
        """Draws the text onto screen."""
        self.screen.blit(self.surface, (self.x, self.y))

    def center(self):
        """Center the text into the are given for it."""
        width, height = self.surface.get_size()
        self.x = self.topleft[0] + (self.downright[0] - self.topleft[0]) / 2 - width / 2
        self.y = self.topleft[1] + (self.downright[1] - self.topleft[1]) / 2 - height / 2


class Score(Text):
    def __init__(self, screen, text: str, color: tuple, topleft: tuple, downright: tuple):
        super().__init__(screen, text, color, topleft, downright)

    def draw(self, score):
        """Override the draw method to allow displaying different scores."""
        self.surface = self.font.render(str(score), False, WHITE)
        self.center()
        self.screen.blit(self.surface, (self.x, self.y))


# TODO implement?
class Grid:
    def __init__(self):
        pass


# TODO clean up init, some comes with text class
class Tetris:
    score_for_cleared_lines = [40, 100, 300, 1200]
    play_bg_color = DARK_GRAY
    bg_color = BLACK
    info_bg_color = BLACK
    line_color = GRAY

    def __init__(self):
        self.game_running = False
        self.screen = self.initialise()

        self.backgrounds = self.make_backgrounds()
        self.pieces = []
        self.text_color = WHITE

        self.texts = self.make_texts()
        self.game_over_text = Text(self.screen, "GAME OVER", self.text_color, (PLAY_LEFT, PLAY_TOP-100), (INFO_LEFT, PLAY_TOP))
        self.score_text = Score(self.screen, "0", self.text_color, (INFO_LEFT, PLAY_TOP + 100), (WINDOW_WIDTH, PLAY_TOP + 200))

        self.reset()

        self.state = GameState.PLAYING

        self.clock = pygame.time.Clock()

    def initialise(self):
        """Initial state of the game and pygame inits."""
        pygame.init()
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tetris")
        return screen

    def make_backgrounds(self):
        """Creates all the backgrounds."""
        bgs = [Background(self.screen, self.bg_color, 0, 0, WINDOW_WIDTH, WINDOW_HEIGHT),
               Background(self.screen, self.play_bg_color, PLAY_LEFT, PLAY_TOP, PLAY_WIDTH, PLAY_HEIGHT),
               Background(self.screen, self.info_bg_color, INFO_LEFT, 0, INFO_WIDTH, INFO_HEIGHT)]
        return bgs

    def make_texts(self):
        """Creates all text objects. Maybe change to dict later ?"""
        texts = [
            Text(self.screen, "TETRIS", self.text_color, (PLAY_LEFT, 0), (PLAY_LEFT + PLAY_WIDTH, PLAY_TOP)),
            Text(self.screen, "Score", self.text_color, (INFO_LEFT, PLAY_TOP), (WINDOW_WIDTH, PLAY_TOP + 100)),
        ]
        return texts

    def empty_grid(self):
        """Returns a grid full of play areas background color."""
        rows = int(PLAY_HEIGHT / BLOCK_SIZE)
        cols = int(PLAY_WIDTH / BLOCK_SIZE)

        return [[self.play_bg_color for _ in range(cols)] for _ in range(rows)]

    def empty_line(self):
        """Returns a line filled with play areas background color."""
        cols = int(PLAY_WIDTH / BLOCK_SIZE)
        return [self.play_bg_color for _ in range(cols)]

    def clean_grid(self):
        """Removes all non-locked positions from grid. Make sure current piece is locked before calling."""
        for x, row in enumerate(self.locked_positions):
            for y, color in enumerate(row):
                if color != self.play_bg_color:
                    self.grid[x][y] = color
                else:
                    self.grid[x][y] = self.play_bg_color

    def reset(self):
        """Resets game state."""
        self.score = 0
        self.next_piece = self.new_piece()
        self.piece = self.get_next_piece()
        self.grid = self.empty_grid()
        self.next_piece_grid = [[self.bg_color for _ in range(5)] for _ in range(5)]
        self.locked_positions = self.empty_grid()
        self.game_running = True

    def draw_blocks(self):
        """Draws all the blocks in grid. Accounts for line widths etc."""
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                color = col
                x_pos = PLAY_LEFT + (x * BLOCK_SIZE)
                y_pos = PLAY_TOP + (y * BLOCK_SIZE)
                width = BLOCK_SIZE - LINE_WIDTH
                height = BLOCK_SIZE - LINE_WIDTH
                pygame.draw.rect(self.screen, color, (x_pos, y_pos, height, width))

    def display_piece(self, grid, piece):
        """Copies pieces color into grid according to shape of piece."""
        for position in piece.block_positions:
            grid[piece.y + position[1]][piece.x + position[0]] = piece.color

    def display_next_piece(self):
        """Places next piece on to it's grid"""
        self.next_piece_grid = [[self.bg_color for _ in range(5)] for _ in range(5)]
        for position in self.next_piece.block_positions:
            self.next_piece_grid[position[0]][position[1]] = self.next_piece.color

    def draw_next_piece(self):
        """Draws next piece in the up left corner."""
        for y, row in enumerate(self.next_piece_grid):
            for x, col in enumerate(row):
                color = col
                x_pos = (x * BLOCK_SIZE) + PLAY_LEFT / 4
                y_pos = (y * BLOCK_SIZE) + PLAY_TOP
                width = BLOCK_SIZE - LINE_WIDTH
                height = BLOCK_SIZE - LINE_WIDTH
                pygame.draw.rect(self.screen, color, (x_pos, y_pos, height, width))

    def new_piece(self):
        return random.choice(pieces.piece_types)()

    def get_next_piece(self):
        """Returns the next piece and gets a random in queue."""
        piece = self.next_piece
        self.next_piece = self.new_piece()
        return piece

    def lock_piece(self, piece):
        """Copies a pieces block positions into locked positions."""
        for position in piece.block_positions:
            self.locked_positions[piece.y + position[1]][piece.x + position[0]] = piece.color

    def game_over(self):
        self.game_running = False
        self.game_over_text.draw()

    def check_down(self, grid, piece):
        """Return true if piece can move down"""
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
        """Return true if piece can move right."""
        for position in piece.block_positions:
            row = piece.y + position[1]
            col = piece.x + position[0]
            if col >= (len(grid[0]) - 1):
                return False
            color_right = grid[row][col + 1]
            if color_right != self.play_bg_color:
                color_in_locked_pos = self.locked_positions[row][col + 1]
                if color_in_locked_pos != self.play_bg_color:
                    return False
        return True

    def check_left(self, grid, piece):
        for position in piece.block_positions:
            row = piece.y + position[1]
            col = piece.x + position[0]
            if col == 0:
                return False
            color_right = grid[row][col - 1]
            if color_right != self.play_bg_color:
                color_in_locked_pos = self.locked_positions[row][col - 1]
                if color_in_locked_pos != self.play_bg_color:
                    return False
        return True

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

    def clear_line(self, row_n):
        """Clears the given line and shuffles all remaining lines down 1 step.
        Also adds an empty line up top."""
        while row_n > 0:
            self.locked_positions[row_n] = self.locked_positions[row_n - 1]
            row_n -= 1
        self.locked_positions[0] = self.empty_line()

    def draw_backgrounds(self):
        """Draws all the backgrounds."""
        for bg in self.backgrounds:
            bg.draw()
        self.display_next_piece()
        self.draw_next_piece()
        self.backgrounds[1].draw_grid(self.line_color)

    def draw_texts(self):
        for text in self.texts:
            text.draw()
        self.score_text.draw(self.score)

    def handle_events(self) -> bool:
        """Returns a bool. True if should quit"""
        for event in pygame.event.get():
            if event.type == QUIT:
                return True
            if event.type == KEYDOWN:
                if self.state == GameState.PLAYING:
                    if event.key == K_a and self.check_left(self.grid, self.piece):
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
        """Piece will fall if enough time has passed."""
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
        """Game loop."""
        time = 0
        while True:
            if self.game_running:
                self.draw_backgrounds()
                self.draw_texts()
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
