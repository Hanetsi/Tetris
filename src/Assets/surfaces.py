import pygame


class Surface(pygame.Surface):
    def __init__(self, screen, color: tuple, size: tuple, pos: tuple):
        self.screen = screen
        self.color = color
        super().__init__(size)
        self.area = self.get_rect()
        self.x, self.y = pos[0], pos[1]
        self.area.move_ip(pos)
        self.fill(self.color)

    def draw(self):
        self.screen.blit(self, self.area)


class TetrisSurface(Surface):
    def __init__(self, screen, color: tuple, line_color: tuple, size: tuple, pos: tuple, line_width: float,
                 block_size: float):
        super().__init__(screen, color, size, pos)
        self.line_width = line_width
        self.line_color = line_color
        self.block_size = block_size
        self.window_height = self.screen.get_size()[1]
        self.play_height = size[1]

    def draw(self):
        self.screen.blit(self, self.area)
        self.draw_horizontal_lines()
        self.draw_vertical_lines()

    def draw_horizontal_lines(self) -> None:
        """Draws the horizontal lines from the bottom up."""
        for y in range(int(self.get_height() / self.block_size) + 1):
            row = (y * self.block_size)
            pygame.draw.line(self, self.line_color, (0, row), (self.get_width(), row), width=int(self.line_width))

    def draw_vertical_lines(self) -> None:
        """Draws the vertical lines from the bottom up."""
        for x in range(int(self.get_width() / self.block_size) + 1):
            col = (x * self.block_size)
            pygame.draw.line(self, self.line_color, (col, 0), (col, self.get_height()), width=int(self.line_width))

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
    def __init__(self, screen, color: tuple, size: tuple, pos: tuple, line_width: float, block_size: float):
        super().__init__(screen, color, size, pos)
        self.line_width = line_width
        self.block_size = block_size

    def draw_next_piece(self, grid):
        """Draws next piece in the up left corner."""
        width = self.block_size - self.line_width
        height = self.block_size - self.line_width
        for y, row in enumerate(grid):
            for x, col in enumerate(row):
                color = col
                x_pos = x * (self.block_size + self.line_width) + (self.get_width() * 0.25)
                y_pos = y * (self.block_size + self.line_width)
                if color == self.color:
                    pygame.draw.rect(self, self.color, (x_pos, y_pos, height, width))
                else:
                    pygame.draw.rect(self, color, (x_pos, y_pos, height, width))


class ImageSurface(Surface):
    def __init__(self, screen, color: tuple, size: tuple, pos: tuple, img):
        super().__init__(screen, color, size, pos)
        self.image = img

    def draw(self):
        self.screen.blit(self.image, self.area)
