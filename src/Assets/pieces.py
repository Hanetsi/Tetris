try:
    from src.Assets.colors import *
except ModuleNotFoundError:
    from src.Assets.colors import *


class Piece:
    shapes_colors = [
        WHITE,
        RED,
        GREEN,
        BLUE,
        YELLOW,
        CYAN,
        MAGENTA
    ]

    def __init__(self):
        self.x = 4
        self.y = 0
        self.rotation = 0

    def rotate(self):
        """Each piece implements their own version."""
        pass

    def move_down(self):
        self.y += 1

    def move_right(self):
        self.x += 1

    def move_left(self):
        self.x -= 1


class iPiece(Piece):
    def __init__(self):
        super().__init__()
        self.color = CYAN
        self.shape = [
            [(0, 0), (1, 0), (2, 0), (3, 0)],
            [(0, 0), (0, 1), (0, 2), (0, 3)]
        ]
        self.x = 3
        self.positions = self.shape[self.rotation]

    def rotate(self):
        if self.rotation:
            self.rotation = 0
        elif not self.rotation:
            self.rotation = 1
        self.positions = self.shape[self.rotation]


class oPiece(Piece):
    def __init__(self):
        super().__init__()
        self.color = YELLOW
        self.shape = [
            [(0, 0), (0, 1), (1, 0), (1, 1)]
        ]
        self.positions = self.shape[self.rotation]


class tPiece(Piece):
    def __init__(self):
        super().__init__()
        self.color = MAGENTA
        self.shape = [
            [(0, 1), (1, 1), (2, 1), (1, 0)],
            [(0, 0), (0, 1), (0, 2), (1, 1)],
            [(0, 0), (1, 0), (2, 0), (1, 1)],
            [(1, 0), (1, 1), (1, 2), (0, 1)]
        ]
        self.positions = self.shape[self.rotation]

    def rotate(self):
        if self.rotation >= 3:
            self.rotation = 0
        else:
            self.rotation += 1
        self.positions = self.shape[self.rotation]


class sPiece(Piece):
    def __init__(self):
        super().__init__()
        self.color = GREEN
        self.shape = [
            [(0, 1), (1, 0), (1, 1), (2, 0)],
            [(0, 0), (0, 1), (1, 1), (1, 2)]
        ]
        self.positions = self.shape[self.rotation]

    def rotate(self):
        if self.rotation:
            self.rotation = 0
        elif not self.rotation:
            self.rotation = 1
        self.positions = self.shape[self.rotation]


class zPiece(Piece):
    def __init__(self):
        super().__init__()
        self.color = RED
        self.shape = [
            [(0, 0), (1, 0), (1, 1), (2, 1)],
            [(0, 1), (0, 2), (1, 0), (1, 1)]
        ]
        self.positions = self.shape[self.rotation]

    def rotate(self):
        if self.rotation:
            self.rotation = 0
        elif not self.rotation:
            self.rotation = 1
        self.positions = self.shape[self.rotation]


class lPiece(Piece):
    def __init__(self):
        super().__init__()
        self.color = ORANGE
        self.shape = [
            [(0, 1), (1, 1), (2, 1), (2, 0)],
            [(0, 0), (0, 1), (0, 2), (1, 2)],
            [(0, 0), (1, 0), (2, 0), (0, 1)],
            [(0, 0), (1, 0), (1, 1), (1, 2)]
        ]
        self.positions = self.shape[self.rotation]

    def rotate(self):
        if self.rotation >= 3:
            self.rotation = 0
        else:
            self.rotation += 1
        self.positions = self.shape[self.rotation]


class jPiece(Piece):
    def __init__(self):
        super().__init__()
        self.color = BLUE
        self.shape = [
            [(0, 0), (0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 0), (1, 1), (1, 2)],
            [(0, 0), (1, 0), (2, 0), (2, 1)],
            [(0, 0), (0, 1), (0, 2), (1, 0)]
        ]
        self.positions = self.shape[self.rotation]

    def rotate(self):
        if self.rotation >= 3:
            self.rotation = 0
        else:
            self.rotation += 1
        self.positions = self.shape[self.rotation]


piece_types = [iPiece, oPiece, tPiece, sPiece, zPiece, lPiece, jPiece]
