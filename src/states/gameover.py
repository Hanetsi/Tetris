import pygame


class Gameover:
    """Splash screen. Also the initial state."""
    def __init__(self):
        pass

    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0
