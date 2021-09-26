import pygame
from src.Assets.colors import *


class Text:
    pygame.font.init()
    font = pygame.font.SysFont("Monotxt", 50)

    def __init__(self, screen, text: str, color: tuple, size: int, topleft: tuple, downright: tuple):
        self.screen = screen
        self.size = size
        self.text = text
        self.color = color
        self.topleft = topleft
        self.downright = downright
        # Initial value for x and y
        self.x, y = self.topleft[0], self.topleft[1]
        self.surface = self.font.render(text, False, self.color)
        self.center()

    def draw(self):
        """Draws the text onto screen."""
        self.screen.blit(self.surface, (self.x, self.y))

    def center(self):
        """Center the text into the are given for it."""
        width, height = self.surface.get_size()
        self.x = self.topleft[0] + (self.downright[0] - self.topleft[0]) / 2 - width / 2
        self.y = self.topleft[1] + (self.downright[1] - self.topleft[1]) / 2 - height / 2

    def get_text(self):
        return self.text


class Score(Text):
    def __init__(self, screen, text: str, color: tuple, size: int, topleft: tuple, downright: tuple):
        super().__init__(screen, text, color, size, topleft, downright)

    def draw(self, score):
        """Override the draw method to allow displaying different scores."""
        self.surface = self.font.render(str(score), False, self.color)
        self.center()
        self.screen.blit(self.surface, (self.x, self.y))


class Option(Text):
    def __init__(self, screen, text: str, color: tuple, size: int, topleft: tuple, downright: tuple):
        self.text = "< " + text + " >"
        super().__init__(screen, self.text, color, size, topleft, downright)

    def draw(self):
        """Draws the text onto screen with normal color"""
        self.surface = self.font.render(self.text, False, self.color)
        self.center()
        self.screen.blit(self.surface, (self.x, self.y))

    def draw_as_selected(self):
        """Draws the text onto screen with inverted color"""
        inverted_r, inverted_g, inverted_b = 255 - self.color[0], 255 - self.color[1], 255 - self.color[2]
        self.surface = self.font.render(self.text, False, (inverted_r, inverted_g, inverted_b))
        self.center()
        self.screen.blit(self.surface, (self.x, self.y))

    def update_text(self, text: str):
        self.text = "< " + text + " >"

    def get_option_value(self):
        return self.text.strip("< >")
