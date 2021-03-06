import pygame
from src.states import splash, tetris, gameover, settings
from src.Assets.gamestate import GameState


# DEFAULT CONFIG
WIDTH = 1440
HEIGHT = 1080
VOLUME = 100


class Game:
    """Root class of the game."""
    def __init__(self, path):
        pygame.init()
        pygame.font.init()
        self.path = path
        self.config = {
            "name": "hanezi",
            "resolution": (WIDTH, HEIGHT),
            "volume": VOLUME
        }

        self.load_config()
        self.initialize()

        self.splash = splash.Splash(self.screen)
        self.settings = settings.Settings(self.screen, self.config)
        self.tetris = tetris.Tetris(self.screen)
        self.gameover = gameover.Gameover(self.screen)

        self.game_loop()

    def initialize(self):
        self.screen = pygame.display.set_mode(self.config['resolution'])
        pygame.display.set_caption("Tetris")
        self.state = GameState.SPLASH

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
                values = []
                for line in lines:
                    if line[0] == "resolution":
                        resolution = (line[1]).strip("()").split(", ")
                        resolution = (int(resolution[0]), int(resolution[1]))
                        values.append(resolution)
                    elif line[0] == "name":
                        values.append(str(line[1]))
                    else:
                        values.append(int(line[1]))
                loaded = dict(zip(keys, values))

            for key in self.config.keys():
                if key not in loaded.keys():
                    with open(path, "a") as f:
                        line = key + "=" + str(self.config[key]) + "\n"
                        f.write(line)
            self.config = loaded
            return True

        except FileNotFoundError as e:
            print("Error while loading config.", e)
            if self.write_config():
                return True
            else:
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

    def game_loop(self):
        running = True
        while running:
            if self.state == GameState.SPLASH:
                self.splash = splash.Splash(self.screen)
                self.state = self.splash.loop()
            elif self.state == GameState.SETTINGS:
                self.settings = settings.Settings(self.screen, self.config)
                self.state = self.settings.loop()
                self.config = self.settings.get_config()
                self.write_config()
            elif self.state == GameState.TETRIS:
                self.tetris = tetris.Tetris(self.screen)
                self.state = self.tetris.loop()
                self.score = self.tetris.get_score()
            elif self.state == GameState.GAMEOVER:
                self.gameover = gameover.Gameover(self.screen, score=self.score)
                self.state = self.gameover.loop()
            elif self.state == GameState.RESTART:
                restart(self.path)
                break
            elif self.state == GameState.QUIT:
                running = False
                pygame.quit()


def restart(path):
    Game(path)



