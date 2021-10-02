import pygame


class Surface(pygame.Surface):
    """Base class for surfaces. Acts as an interface between specific surfaces and pygame surface."""
    tetris_surface_percentage = 0.30

    def __init__(self, size: tuple, pos: tuple):
        super().__init__(size)
        self.area = self.get_rect()
        self.area.move_ip(pos)

    def draw(self):
        """Each sublcass should implement their own."""


class TetrisSurface(Surface):
    """Games play area."""
    def __init__(self, screen, color: tuple, line_color: tuple, line_width: int):
        self.screen = screen
        self.line_color = line_color
        self.color = color
        self.line_width = line_width
        self.width = (self.screen.get_width() * self.tetris_surface_percentage) + self.line_width
        self.height = (self.screen.get_width() * self.tetris_surface_percentage * 2) + self.line_width
        self.left = (self.screen.get_width() / 2) - (self.width / 2) + self.line_width
        self.top = self.screen.get_height() - self.height - self.line_width
        self.block_size = self.screen.get_width() * self.tetris_surface_percentage / 10
        super().__init__((self.width, self.height), (self.left, self.top))
        self.fill(self.color)

    def draw(self):
        self.screen.blit(self, self.area)
        self.draw_horizontal_lines()
        self.draw_vertical_lines()

    def draw_horizontal_lines(self) -> None:
        """Draws the horizontal lines from the bottom up."""
        for y in range(int(self.height / self.block_size) + 1):
            row = (y * self.block_size)
            pygame.draw.line(self, self.line_color, (0, row), (self.width, row), width=int(self.line_width))

    def draw_vertical_lines(self) -> None:
        """Draws the vertical lines from the bottom up."""
        for x in range(int(self.width / self.block_size) + 1):
            col = (x * self.block_size)
            pygame.draw.line(self, self.line_color, (col, 0), (col, self.height), width=int(self.line_width))

    def draw_grid(self, grid):
        """Draws all the blocks in grid. Accounts for line widths etc."""
        width = self.block_size - self.line_width
        height = self.block_size - self.line_width
        for y, row in enumerate(grid):
            for x, col in enumerate(row):
                color = col
                x_pos = x * self.block_size + self.line_width
                y_pos = y * self.block_size + self.line_width
                pygame.draw.rect(self, color, (x_pos, y_pos, height, width))


class NextPieceSurface(Surface):
    def __init__(self, screen, color: tuple, line_width: float):
        self.screen = screen
        self.bg_color = color
        self.line_width = line_width
        self.width = self.screen.get_width() * ((1.0 - self.tetris_surface_percentage) / 2)
        self.height = (self.screen.get_width() * self.tetris_surface_percentage * 2) + self.line_width
        self.left = 0
        self.top = self.screen.get_height() - self.height - self.line_width
        self.block_size = self.screen.get_width() * self.tetris_surface_percentage / 10
        super().__init__((self.width, self.height), (self.left, self.top))

    def draw(self):
        self.screen.blit(self, self.area)

    def draw_next_piece(self, grid):
        """Draws next piece in the up left corner."""
        width = self.block_size - self.line_width
        height = self.block_size - self.line_width
        for y, row in enumerate(grid):
            for x, col in enumerate(row):
                color = col
                x_pos = x * (self.block_size + self.line_width) + (self.width * 0.3)
                y_pos = y * (self.block_size + self.line_width)
                if color == self.bg_color:
                    pygame.draw.rect(self, self.bg_color, (x_pos, y_pos, height, width))
                else:
                    pygame.draw.rect(self, color, (x_pos, y_pos, height, width))


class BackgroundSurface(Surface):
    """A background that fills the whole screen."""
    def __init__(self, screen, color: tuple = (0, 0, 0)):
        self.screen = screen
        self.size = self.screen.get_size()
        self.left, self.top = 0, 0
        self.color = color
        super().__init__(self.size, (self.left, self.top))

    def draw(self):
        self.screen.blit(self, self.area)


class ImageBackgroundSurface(BackgroundSurface):
    """Background with an image."""
    def __init__(self, screen, img):
        super().__init__(screen)
        self.image = img

    def draw(self):
        self.screen.blit(self.image, self.area)
