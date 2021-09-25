import pygame
from pygame.locals import *
from src.Assets.gamestate import GameState


class Splash:
    """Splash screen. Also the initial state."""
    def __init__(self):
        pass

    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0

                if event.type == pygame.KEYDOWN:
                    if event.key == K_SPACE:
                        return GameState.TETRIS
