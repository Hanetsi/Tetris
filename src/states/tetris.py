import pygame
from pygame.locals import *

try:
    from src.Assets.colors import *
    from src.Assets.texts import Text, Score, Title
    from src.Assets.gamestate import GameState
    from src.Assets.surfaces import Surface, TetrisSurface, NextPieceSurface
    from src.Assets.grid import Grid, NextPieceGrid
except ModuleNotFoundError:
    from src.Assets.colors import *


class Tetris:
    play_bg_color = DARK_GRAY
    bg_color = BLACK
    line_color = GRAY
    play_area_percentage = 0.30  # Percentage of window width that play are will occupy
    line_width = 2
    fall_time = 500

    def __init__(self, screen):
        self.game_running = False
        self.screen = screen
        self.x, self.y = self.screen.get_rect()[0], self.screen.get_rect()[1]
        self.width, self.height = self.screen.get_width(), self.screen.get_height()
        self.dimensions = {
            "play_width": (self.width * self.play_area_percentage) + self.line_width,
            "play_height": (self.width * self.play_area_percentage * 2) + self.line_width,
            "play_left": (self.width / 2) - (self.width * self.play_area_percentage / 2) + self.line_width,
            "play_top": self.height - (self.width * self.play_area_percentage * 2) - self.line_width,
            "info_width": self.width * self.play_area_percentage / 2,
            "info_height": (self.width * self.play_area_percentage * 2) + self.line_width,
            "info_left": (self.width * self.play_area_percentage) + (self.width / 2) - (self.width * self.play_area_percentage / 2) + (self.line_width / 2),
            "info_top": self.height - self.width * self.play_area_percentage * 2 - self.line_width,
            "block_size": self.width * self.play_area_percentage / 10,
        }
        self.rows = int(self.dimensions["play_height"] / self.dimensions["block_size"])
        self.cols = int((self.dimensions["play_width"] / self.dimensions["block_size"]))
        self.surfaces = self.create_surfaces()
        self.grid = Grid(bg_color=self.play_bg_color, rows=self.rows, cols=self.cols)
        self.next_grid = NextPieceGrid(bg_color=self.bg_color, rows=5, cols=5)

        self.grid.piece = self.next_grid.piece
        self.next_grid.next_piece()
        self.grid.piece_to_grid()
        self.next_grid.piece_to_grid()

        self.text_color = PURPLE
        self.text_size = self.width/10
        self.static_texts = self.create_static_texts()
        self.game_over_text = Text(self.screen, "GAME OVER", self.text_color,
                                   (self.dimensions["play_left"], self.dimensions["play_top"] - 100),
                                   (self.dimensions["info_left"], self.dimensions["play_top"]))
        self.score_text = Score(self.screen, "0", self.text_color,
                                (self.dimensions["info_left"], self.dimensions["play_top"] + 100),
                                (self.width, self.dimensions["play_top"] + 200))

        self.state = GameState.TETRIS
        self.clock = pygame.time.Clock()
        self.score = 0
        self.game_running = True
        self.game_over = False

    def create_surfaces(self):
        surfaces = [
            Surface(self.screen, self.bg_color, (self.width, self.height),
                    (self.x, self.y)),
            TetrisSurface(self.screen, self.play_bg_color, self.line_color,
                          (self.dimensions["play_width"], self.dimensions["play_height"]),
                          (self.dimensions["play_left"], self.dimensions["play_top"]),
                          self.line_width, self.dimensions["block_size"]),
            NextPieceSurface(self.screen, self.bg_color, (self.dimensions["play_left"], 200),
                             (0, self.dimensions["play_top"]),
                             self.line_width, self.dimensions["block_size"])
        ]
        return surfaces

    def create_static_texts(self):
        text = [
            Title(self.screen, "TETRIS", self.text_color,
                  (self.dimensions["play_left"], 0),
                  (self.dimensions["play_left"] + self.dimensions["play_width"], self.dimensions["play_top"])),
            Text(self.screen, "Score", self.text_color, (self.dimensions["info_left"], self.dimensions["play_top"]),
                 (self.width, self.dimensions["play_top"] + 100)),
            Text(self.screen, "MENU (ESC)", self.text_color,
                 (0, self.width * 0.7),
                 (self.dimensions["play_left"], self.height)),
            Text(self.screen, "RESTART (R)", self.text_color,
                 (self.dimensions["info_left"], self.width * 0.7),
                 (self.width, self.height))
        ]
        return text

    def check_game_over(self):
        if self.grid.piece.y == 0:
            self.game_over = True

    def get_score(self):
        return self.score

    def draw_surfaces(self):
        """Draws all the backgrounds."""
        for surface in self.surfaces:
            surface.draw()

    def draw_texts(self):
        for text in self.static_texts:
            text.draw()
        self.score_text.draw(self.score)

    def handle_events(self) -> bool:
        """Returns a bool. False if state has not changed."""
        for event in pygame.event.get():
            if event.type == QUIT:
                return GameState.QUIT
            if event.type == KEYDOWN:
                if self.state == GameState.TETRIS:
                    if event.key == K_a and self.grid.check_left():
                        self.grid.piece.move_left()
                    if event.key == K_d and self.grid.check_right():
                        self.grid.piece.move_right()
                    if event.key == K_w:
                        self.grid.piece.rotate()
                        while not self.grid.check_right():
                            self.grid.piece.x -= 1
                    if event.key == K_s:
                        while self.grid.check_down():
                            self.grid.piece.move_down()
                        else:
                            if self.check_game_over():
                                return
                            self.grid.lock_piece()
                            self.grid.piece = self.next_grid.piece
                            self.next_grid.next_piece()
                            self.next_grid.piece_to_grid()
                    if event.key == K_ESCAPE:
                        return GameState.SPLASH
                    if event.key == K_r:
                        return GameState.TETRIS
        return False

    # TODO gameover doesn't work
    def fall(self, time):
        """Piece will fall if enough time has passed."""
        time += self.clock.tick()
        if time > self.fall_time:
            if self.grid.check_down():
                self.grid.piece.move_down()
                time = 0
            else:
                if self.check_game_over():
                    return
                self.grid.lock_piece()
                self.grid.piece = self.next_grid.piece
                self.next_grid.next_piece()
                self.next_grid.piece_to_grid()
        return time

    def loop(self):
        """Game loop."""
        time = 0
        while True:
            if self.game_running:
                self.draw_surfaces()
                self.draw_texts()
                self.surfaces[1].draw_grid(self.grid.grid)
                self.surfaces[2].draw_next_piece(self.next_grid.grid)

                state_change = self.handle_events()
                if state_change:
                    return state_change
                if self.game_over:
                    return GameState.GAMEOVER
                time = self.fall(time)
                self.grid.clean_grid()
                self.grid.piece_to_grid()
                self.score += self.grid.check_lines()
                self.score_text.draw(self.score)

            pygame.display.flip()
