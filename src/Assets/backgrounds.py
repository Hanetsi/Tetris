import pygame


class Background:
    def __init__(self, screen, color: tuple, x: float, y: float, width: float, height: float):
        self.screen = screen
        self.color = color
        self.pos = x, y
        self.width = width
        self.height = height

        self.bg = pygame.Surface((width, height))
        self.bg = self.bg.convert()
        self.bg.fill(self.color)

    def draw(self):
        self.screen.blit(self.bg, self.pos)


class TetrisBackground(Background):
    def __init__(self, screen, color: tuple, x: float, y: float, width: float, height: float, line_width: float,
                 block_size: float, window_height: float, play_height: float):
        super().__init__(screen, color, x, y, width, height)
        self.line_width = line_width
        self.block_size = block_size
        self.window_height = window_height
        self.play_height = play_height

    # TODO fix the upper corners
    def draw_grid(self, color: tuple):
        """Draws the lines from the bottom up."""
        self.draw_horizontal_lines(color)
        self.draw_vertical_lines(color)

    def draw_horizontal_lines(self, color: tuple) -> None:
        """Draws the horizontal lines from the bottom up."""
        left = self.pos[0] - (self.line_width / 2)
        right = left + self.width
        for y in range(int(self.height / self.block_size) + 1):
            row = self.window_height - (y * self.line_width) - (y * (self.block_size - self.line_width)) - (self.line_width / 2)
            pygame.draw.line(self.screen, color, (left, row), (right, row), width=self.line_width)

    def draw_vertical_lines(self, color: tuple) -> None:
        """Draws the vertical lines from the bottom up."""
        top = self.window_height - self.play_height - (self.line_width / 2)
        bottom = self.window_height
        for x in range(int(self.width / self.block_size) + 1):
            x_pos = x * float(self.block_size) + self.pos[0] - (self.line_width / 2)
            pygame.draw.line(self.screen, color, (x_pos, top), (x_pos, bottom), width=self.line_width)
