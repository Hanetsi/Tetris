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
        self.text_size = self.screen.get_width() / 10
        self.text_color = PURPLE
        # A bit rough
        self.static_texts = [
            Text(self.screen, "TETRIS", self.text_color, self.text_size*2, (0, 0),
                 (self.screen.get_width() * 0.5, self.screen.get_height() * 0.2)),
            Text(self.screen, "PLAY (space)", self.text_color, self.text_size, (0, self.screen.get_height() * 0.35),
                 (self.screen.get_width() * 0.5, self.screen.get_height() * 0.45)),
            Text(self.screen, "OPTIONS (F1)", self.text_color, self.text_size, (0, self.screen.get_height() * 0.45),
                 (self.screen.get_width() * 0.5, self.screen.get_height() * 0.55)),
            Text(self.screen, "QUIT (ESC)", self.text_color, self.text_size, (0, self.screen.get_height() * 0.55),
                 (self.screen.get_width() * 0.5, self.screen.get_height() * 0.65))
        ]
        self.bg_img = pygame.image.load("src/Assets/splash.png").convert()
        self.bg_img = pygame.transform.scale(self.bg_img, self.screen.get_size())
        self.surface = ImageSurface(self.screen, DARK_GRAY, self.screen.get_size(), (0, 0), self.bg_img)

    def loop(self):
        while True:
            self.surface.draw()
            for text in self.static_texts:
                text.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return GameState.QUIT
                if event.type == pygame.KEYDOWN:
                    if event.key == K_SPACE:
                        return GameState.TETRIS
                    if event.key == K_F1:
                        return GameState.SETTINGS
                    if event.key == K_ESCAPE:
                        return GameState.QUIT
            pygame.display.flip()
