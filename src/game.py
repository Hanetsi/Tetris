import pygame
from enum import Enum, auto

pygame.init()

# DEFAULT CONFIG
WIDTH = 1000
HEIGHT = 1000
VOLUME = 100


class GameState(Enum):
    SPLASH = auto()
    SETTINGS = auto()
    PLAYING = auto()
    GAMEOVER = auto()


class Game:
    def __init__(self, path):
        self.path = path
        self.config = {
            "width": WIDTH,
            "height": HEIGHT,
            "volume": VOLUME
        }

        self.load_config()
        self.initialize()
        self.loop()

    def initialize(self):
        self.screen = pygame.display.set_mode((self.config["width"], self.config["height"]))
        pygame.display.set_caption("Tetris")
        self.running = True

    def load_config(self) -> bool:
        """Try to load settings from config file into config. If file is not found, make it with default values.
        If some of the values are missing (eg. in case of more settings added), append them to the config file."""
        try:
            path = self.path + "/config.cfg"
            with open(path, "r") as f:
                lines = f.readlines()
                lines = [line.split("=") for line in lines]
                lines = [[elem.strip("\n") for elem in line] for line in lines]
                keys = [line[0] for line in lines]
                values = [int(line[1]) for line in lines]
                loaded = dict(zip(keys, values))

            for key in self.config.keys():
                if key not in loaded.keys():
                    with open(path, "a") as f:
                        line = key + "=" + str(self.config[key] + "\n")
                        f.write(line)
            return True

        except FileNotFoundError:
            if self.write_config():
                return True
            else:
                return False

        except Exception as e:
            print(e)
            return False

    def write_config(self) -> bool:
        """Write the current config to cfg file. When changing config within program, changed should first
        first be saved into self.cfg and then call write_config."""
        path = self.path + "/config.cfg"
        try:
            with open(path, "w") as f:
                lines = []
                for key in self.config.keys():
                    lines.append(key + "=" + str(self.config[key]) + "\n")
                f.writelines(lines)
            return True

        except Exception as e:
            print(e)
            return False

    def loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False
