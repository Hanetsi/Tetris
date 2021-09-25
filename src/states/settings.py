import pygame
from pygame.locals import *
from src.Assets.gamestate import GameState
from src.Assets.surfaces import Surface, ImageSurface
from src.Assets.colors import *
from src.Assets.texts import Text, Option


class Settings:
    resolutions = [
        (640, 480),
        (800, 600),
        (1024, 768),
        (1280, 960),
        (1440, 1080)
    ]
    """Splash screen. Also the initial state."""
    def __init__(self, screen, config):
        self.screen = screen
        self.config = config
        self.text_size = self.screen.get_width() / 10
        self.text_color = PURPLE
        self.bg_img = pygame.image.load("src/Assets/splash.png").convert()
        self.bg_img = pygame.transform.scale(self.bg_img, self.screen.get_size())
        self.surface = ImageSurface(self.screen, DARK_GRAY, self.screen.get_size(), (0, 0), self.bg_img)
        self.selected = 0
        self.static_texts = [
            Text(self.screen, "Name", self.text_color, self.text_size, (0, self.screen.get_height() * 0.1),
                 (self.screen.get_width() * 0.5, self.screen.get_height() * 0.2)),
            Text(self.screen, "Resolution", self.text_color, self.text_size, (0, self.screen.get_height() * 0.3),
                 (self.screen.get_width() * 0.5, self.screen.get_height() * 0.4)),
            Text(self.screen, "Volume", self.text_color, self.text_size, (0, self.screen.get_height() * 0.5),
                 (self.screen.get_width() * 0.5, self.screen.get_height() * 0.6)),
            Text(self.screen, "MENU (ESC)", self.text_color, self.text_size, (0, self.screen.get_height() * 0.9),
                 (self.screen.get_width() * 0.5, self.screen.get_height() * 1.0))
        ]
        self.options = [
            Option(self.screen, self.config["name"], self.text_color, self.text_size, (0, self.screen.get_height() * 0.2),
                 (self.screen.get_width() * 0.5, self.screen.get_height() * 0.3)),
            Option(self.screen, str(self.config["resolution"]), self.text_color, self.text_size, (0, self.screen.get_height() * 0.4),
                 (self.screen.get_width() * 0.5, self.screen.get_height() * 0.5)),
            Option(self.screen, str(self.config["volume"]), self.text_color, self.text_size, (0, self.screen.get_height() * 0.6),
                 (self.screen.get_width() * 0.5, self.screen.get_height() * 0.7))
        ]

    def loop(self):
        while True:
            self.surface.draw()
            for text in self.static_texts:
                text.draw()
            for i, option in enumerate(self.options):
                if i == self.selected:
                    option.draw_as_selected()
                else:
                    option.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return GameState.QUIT
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        return GameState.SPLASH
                    if event.key == K_DOWN:
                        if self.selected < 2:
                            self.selected += 1
                        else:
                            self.selected = 0
                    if event.key == K_UP:
                        if self.selected > 0:
                            self.selected -= 1
                        else:
                            self.selected = 2
            pygame.display.flip()
