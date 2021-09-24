import pygame
from enum import Enum, auto

pygame.init()


class GameState(Enum):
    SPLASH = auto()
    SETTINGS = auto()
    PLAYING = auto()
    GAMEOVER = auto()


class Game:
    def __init__(self):
        self.settings = {
            "width": 1000,
            "height": 1000,
            "volume": 1.0
        }

        self.initialize()
        self.loop()

    def initialize(self):
        self.screen = pygame.display.set_mode((self.settings["width"], self.settings["height"]))
        pygame.display.set_caption("Tetris")
        self.running = True

    def load_config(self):
        pass

    def write_config(self):
        pass

    def loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False

