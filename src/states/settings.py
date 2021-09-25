import pygame
from pygame.locals import *
from src.Assets.gamestate import GameState
from src.Assets.surfaces import Surface
from src.Assets.colors import *
from src.Assets.texts import Text


class Settings:
    """Splash screen. Also the initial state."""
    def __init__(self, screen):
        self.screen = screen
        self.surface = Surface(self.screen, DARK_GRAY, self.screen.get_size(), (0, 0))

    def loop(self):
        while True:
            self.surface.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return GameState.QUIT
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        return GameState.SPLASH
            pygame.display.flip()
