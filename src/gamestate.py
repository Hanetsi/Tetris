from enum import Enum, auto


class GameState(Enum):
    SPLASH = auto()
    SETTINGS = auto()
    TETRIS = auto()
    GAMEOVER = auto()
