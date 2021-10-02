import src.Assets.pieces as pieces
import random


def random_piece():
    return random.choice(pieces.piece_types)()


def empty_grid(color: tuple, rows: int, cols: int):
    return [[color for _ in range(cols)] for _ in range(rows)]


class Grid:
    def __init__(self, bg_color, rows: int = 20, cols: int = 10):
        self.bg_color = bg_color
        self.rows = rows
        self.cols = cols
        self.grid = empty_grid(self.bg_color, self.rows, self.cols)
        self.locked_grid = empty_grid(self.bg_color, self.rows, self.cols)
        self.piece = random_piece()

    @staticmethod
    def empty_line(color: tuple, cols: int):
        return [color for _ in range(cols)]

    def clean_grid(self):
        """Removes all non-locked positions from grid. Make sure current piece is locked before calling."""
        for y, row in enumerate(self.locked_grid):
            for x, color in enumerate(row):
                if color != self.bg_color:
                    self.grid[y][x] = color
                else:
                    self.grid[y][x] = self.bg_color

    def lock_piece(self):
        """Copies a pieces block positions into locked positions."""
        for position in self.piece.positions:
            self.locked_grid[self.piece.y + position[1]][self.piece.x + position[0]] = self.piece.color

    def piece_to_grid(self):
        for position in self.piece.positions:
            self.grid[self.piece.y + position[1]][self.piece.x + position[0]] = self.piece.color

    def check_down(self):
        """Return true if piece can move down"""
        for position in self.piece.positions:
            row = self.piece.y + position[1]
            col = self.piece.x + position[0]
            if row >= (len(self.grid) - 1):
                return False
            color_below = self.grid[row + 1][col]
            if color_below != self.bg_color:
                color_in_locked_pos = self.locked_grid[row + 1][col]
                if color_in_locked_pos != self.bg_color:
                    if self.piece.y == 0:
                        return 0
                    return False
        return True

    def check_right(self):
        """Return true if piece can move right."""
        for position in self.piece.positions:
            row = self.piece.y + position[1]
            col = self.piece.x + position[0]
            if col >= (len(self.grid[0]) - 1):
                return False
            color_right = self.grid[row][col + 1]
            if color_right != self.bg_color:
                color_in_locked_pos = self.locked_grid[row][col + 1]
                if color_in_locked_pos != self.bg_color:
                    return False
        return True

    def check_left(self):
        for position in self.piece.positions:
            row = self.piece.y + position[1]
            col = self.piece.x + position[0]
            if col == 0:
                return False
            color_right = self.grid[row][col - 1]
            if color_right != self.bg_color:
                color_in_locked_pos = self.locked_grid[row][col - 1]
                if color_in_locked_pos != self.bg_color:
                    return False
        return True

    def check_lines(self):
        """Check if all elements in a row are not background. If so clear the line"""
        score_for_cleared_lines = [40, 100, 300, 1200]
        cleared = 0
        for i, row in enumerate(self.locked_grid):
            filled = 0
            for color in row:
                if color != self.bg_color:
                    filled += 1
            if filled == len(row):
                cleared += 1
                self.clear_line(i)
        if not cleared:
            return 0
        return score_for_cleared_lines[cleared - 1]

    def clear_line(self, row_n):
        """Clears the given line and shuffles all remaining lines down 1 step.
            #     Also adds an empty line up top."""
        while row_n > 0:
            self.locked_grid[row_n] = self.locked_grid[row_n - 1]
            row_n -= 1
        self.locked_grid[0] = self.empty_line(self.bg_color, self.cols)


class NextPieceGrid(Grid):
    """Inheriting from Grid is not optimal, but will do."""
    def __init__(self, bg_color):
        self.rows = 5
        self.cols = 5
        super().__init__(bg_color, self.rows, self.cols)
        self.piece = random_piece()

    def next_piece(self):
        self.piece = random_piece()

    def piece_to_grid(self):
        self.grid = empty_grid(self.bg_color, self.rows, self.cols)
        for position in self.piece.positions:
            self.grid[position[1]][position[0]] = self.piece.color
