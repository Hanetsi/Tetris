import pygame
from pygame.locals import *
from src.Assets.gamestate import GameState
from src.Assets.surfaces import Surface, ImageSurface
from src.Assets.colors import *
from src.Assets.texts import Text


class Splash:
    """Splash screen. Also the initial state."""
    def __init__(self, screen):
        self.screen = screen
        self.bg_img = pygame.image.load("src/Assets/splash.png")
        self.bg_img = pygame.transform.scale(self.bg_img, self.screen.get_size())
        self.surface = ImageSurface(self.screen, DARK_GRAY, self.screen.get_size(), (0, 0), self.bg_img)

    def loop(self):
        while True:
            self.surface.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return GameState.QUIT
                if event.type == pygame.KEYDOWN:
                    if event.key == K_SPACE:
                        return GameState.TETRIS
                    if event.key == K_ESCAPE:
                        return GameState.QUIT
            pygame.display.flip()
