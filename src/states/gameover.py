import pygame
from pygame.locals import *
from src.Assets.gamestate import GameState
from src.Assets.surfaces import Surface, ImageSurface
from src.Assets.colors import *
from src.Assets.texts import Text, Title


def get_hiscore():
    """Dummy method for now. Implement functionality to get hiscore from database."""
    return 1000


class Gameover:
    """Splash screen. Also the initial state."""
    def __init__(self, screen, score: int = 0):
        self.screen = screen
        self.score = score
        self.hiscore = get_hiscore()
        self.text_size = self.screen.get_width() / 10
        self.text_size = self.screen.get_width() / 10
        self.text_color = PURPLE
        self.bg_img = pygame.image.load("src/Assets/splash.png").convert()
        self.bg_img = pygame.transform.scale(self.bg_img, self.screen.get_size())
        self.surface = ImageSurface(self.screen, DARK_GRAY, self.screen.get_size(), (0, 0), self.bg_img)
        self.texts = self.create_texts()

    def create_texts(self):
        texts = [
            Title(self.screen, "GAME OVER", self.text_color, (0, 0),
                  (self.screen.get_width() / 2, self.screen.get_height() * 0.4)),
            Text(self.screen, str(self.score), self.text_color,
                 (0, self.screen.get_height() * 0.5),
                 (self.screen.get_width() * 0.5, self.screen.get_height() * 0.6)),
            Text(self.screen, "RESTART (R)", self.text_color,
                 (0, self.screen.get_height() * 0.7),
                 (self.screen.get_width() * 0.5, self.screen.get_height() * 0.8)),
            Text(self.screen, "MENU (ESC)", self.text_color, (0, self.screen.get_height() * 0.8),
                 (self.screen.get_width() * 0.5, self.screen.get_height() * 0.9))
        ]
        if self.score > self.hiscore:
            texts.append(Text(self.screen, "NEW HISCORE!", self.text_color,
                                 (0, self.screen.get_height() * 0.4),
                                 (self.screen.get_width() * 0.5, self.screen.get_height() * 0.5)))
        else:
            texts.append(Text(self.screen, "SCORE", self.text_color,
                                 (0, self.screen.get_height() * 0.4),
                                 (self.screen.get_width() * 0.5, self.screen.get_height() * 0.5)))
        return texts

    def loop(self):
        while True:
            self.surface.draw()
            for text in self.texts:
                text.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return GameState.QUIT
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        return GameState.SPLASH
                    if event.key == K_r:
                        return GameState.TETRIS
            pygame.display.flip()
