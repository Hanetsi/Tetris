import pygame
from src.Assets.colors import *


class Text:
    pygame.font.init()
    font = pygame.font.Font("C:/Users/Eelis/OneDrive/Koulu/Python/Tetris/src/tetris_block.ttf", 30)

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
