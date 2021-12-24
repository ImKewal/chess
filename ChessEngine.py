import pygame
import sys
import numpy as np
from pygame.locals import *
from copy import deepcopy
from tkinter import *
from tkinter import messagebox

SIZE_STRIP = 30
SIZE_CELL = 80
HEIGHT_BOARD = 8*SIZE_CELL + 2*SIZE_STRIP
DARK = (118, 150, 86)
LIGHT = (238, 238, 210)
RED = (255, 0, 0)
# ELECTRIC_BLUE = (160, 230, 255)
DARK_RED = (200, 0, 0)
LIGHT_RED = (255, 0, 0)
ELECTRIC_BLUE = (125, 249, 255)
# DARK_ELECTRIC_BLUE = (3, 97, 115)

DARK_ELECTRIC_BLUE = (8, 120, 208)
BLACK = (25, 39, 52)
H = ['1', '2', '3', '4', '5', '6', '7', '8']
V = ['h', 'g', 'f', 'e', 'd', 'c', 'b', 'a']
screen = pygame.display.set_mode((HEIGHT_BOARD, HEIGHT_BOARD))
STARTED = '0X1'
ONGOING = '0X2'
ENDED = '0X3'


class Piece:
    def __init__(self):
        self.CELL = None
        self.LAST_CELL = None
        self.side = None
        self.name = None
        self.image = None
        self.oppo = None
        self.possible_cells = []
        self.temp = None

    def init(self, side):
        self.side = side
        image = rf"data/{self.side.upper()}_{self.name.upper()}.png"
        self.image = pygame.image.load(image)
        self.oppo = 'b' if self.side == 'w' else 'w'

    def checked_cells(self, b):
        pass

    def possible_moves(self, b):
        pass

    def __repr__(self) -> str:
        return f"{self.side.upper()}{self.name.upper()}"


class Move:
    def __init__(self):
        self.piece = None
        self.cell1 = None
        self.cell2 = None
        self.move_number = None

    def moved(self, piece: Piece, cell1: tuple, cell2: tuple, move_number: int):
        self.piece = piece
        self.cell1 = cell1
        self.cell2 = cell2
        self.move_number = move_number


class WP(Piece):
    def __init__(self, file: int):
        super().__init__()
        self.name = 'p'
        super().init('w')
        self.file = file
        self.home = 6
        self.oppo_home = 1

    def en_passant_possible(self, last_move: Move, move_number: int):
        return last_move.move_number == move_number - 1 and last_move.piece.name == 'p' and last_move.piece.side == self.oppo and (
                    last_move.piece.file == self.file - 1 or last_move.piece.file == self.file + 1) and last_move.cell1[
                   0] == self.oppo_home and last_move.cell2[0] == self.oppo_home + 2

    def checked_cells(self, b):
        checked_cells = set()
        temp = deepcopy(self.CELL)
        # left top cell
        temp = temp[0] - 1, temp[1] - 1
        if is_valid_cell(temp):
            checked_cells.add(temp)
        # right top cell
        temp = temp[0], temp[1] + 2
        if is_valid_cell(temp):
            checked_cells.add(temp)
        return checked_cells

    def possible_moves(self, b, last_move: Move = None, move_number: int = None):
        self.file = self.CELL[1]
        self.possible_cells = []
        temp = deepcopy(self.CELL)
        temp = temp[0] - 1, temp[1]
        if b[temp[0]][temp[1]].piece.side is None:
            if is_valid_cell(temp):
                self.possible_cells.append(temp)

            if self.CELL[0] == self.home:
                temp = temp[0] - 1, temp[1]
                if b[temp[0]][temp[1]].piece.side is None:
                    self.possible_cells.append(temp)

        checked_cells = list(self.checked_cells(b))
        for cell in checked_cells:
            if b[cell[0]][cell[1]].piece.side == self.oppo:
                self.possible_cells.append(cell)
        if last_move is not None and move_number is not None:
            if self.CELL[0] == self.oppo_home + 2:
                if self.en_passant_possible(last_move, move_number):
                    temp = deepcopy(last_move.cell2)
                    temp = temp[0] - 1, temp[1]
                    self.possible_cells.append(temp)
        return self.possible_cells


class BP(Piece):
    def __init__(self, file: int):
        super().__init__()
        self.name = 'p'
        super().init('b')
        self.file = file
        self.home = 1
        self.oppo_home = 6

    def en_passant_possible(self, last_move: Move, move_number: int):
        return last_move.move_number == move_number - 1 and last_move.piece.name == 'p' and last_move.piece.side == self.oppo and (
                    last_move.piece.file == self.file - 1 or last_move.piece.file == self.file + 1) and last_move.cell1[
                   0] == self.oppo_home and last_move.cell2[0] == self.oppo_home - 2

    def checked_cells(self, b):
        checked_cells = set()
        temp = deepcopy(self.CELL)
        # left top cell
        temp = temp[0] + 1, temp[1] + 1
        if is_valid_cell(temp):
            checked_cells.add(temp)
        temp = temp[0], temp[1] - 2
        if is_valid_cell(temp):
            checked_cells.add(temp)
        return checked_cells

    def possible_moves(self, b, last_move: Move = None, move_number: int = None):
        self.file = self.CELL[1]
        self.possible_cells = []
        temp = deepcopy(self.CELL)
        temp = temp[0] + 1, temp[1]
        if b[temp[0]][temp[1]].piece.side is None:
            if is_valid_cell(temp):
                self.possible_cells.append(temp)

            if self.CELL[0] == self.home:
                temp = temp[0] + 1, temp[1]
                if b[temp[0]][temp[1]].piece.side is None:
                    self.possible_cells.append(temp)

        checked_cells = list(self.checked_cells(b))
        for cell in checked_cells:
            if b[cell[0]][cell[1]].piece.side == self.oppo:
                self.possible_cells.append(cell)
        if last_move is not None and move_number is not None:
            if self.CELL[0] == self.oppo_home - 2:
                if self.en_passant_possible(last_move, move_number):
                    temp = deepcopy(last_move.cell2)
                    temp = temp[0] + 1, temp[1]
                    self.possible_cells.append(temp)
        return self.possible_cells


class Rook(Piece):
    def __init__(self):
        super().__init__()
        self.name = 'r'
        self.moved = False

    def checked_cells(self, b):
        checked_cells = set()
        temp = deepcopy(self.CELL)
        # left cells
        while True:
            temp = temp[0], temp[1] - 1

            if is_valid_cell(temp):
                if b[temp[0]][temp[1]].piece.side is None or (
                        b[temp[0]][temp[1]].piece.name == 'k' and b[temp[0]][temp[1]].piece.side == self.oppo):
                    checked_cells.add(temp)
                else:
                    checked_cells.add(temp)
                    break
            else:
                break
        temp = deepcopy(self.CELL)
        # bottom cells
        while True:
            temp = temp[0] + 1, temp[1]

            if is_valid_cell(temp):
                if b[temp[0]][temp[1]].piece.side is None or (
                        b[temp[0]][temp[1]].piece.name == 'k' and b[temp[0]][temp[1]].piece.side == self.oppo):
                    checked_cells.add(temp)
                else:
                    checked_cells.add(temp)
                    break
            else:
                break
        temp = deepcopy(self.CELL)
        # right cells
        while True:
            temp = temp[0], temp[1] + 1

            if is_valid_cell(temp):
                if b[temp[0]][temp[1]].piece.side is None or (
                        b[temp[0]][temp[1]].piece.name == 'k' and b[temp[0]][temp[1]].piece.side == self.oppo):
                    checked_cells.add(temp)
                else:
                    checked_cells.add(temp)
                    break
            else:
                break
        temp = deepcopy(self.CELL)
        # top cells
        while True:
            temp = temp[0] - 1, temp[1]

            if is_valid_cell(temp):
                if b[temp[0]][temp[1]].piece.side is None or (
                        b[temp[0]][temp[1]].piece.name == 'k' and b[temp[0]][temp[1]].piece.side == self.oppo):
                    checked_cells.add(temp)
                else:
                    checked_cells.add(temp)
                    break
            else:
                break
        return checked_cells

    def possible_moves(self, b):
        self.possible_cells = []
        temp = deepcopy(self.CELL)
        # left cells
        while True:
            temp = (temp[0], temp[1] - 1)
            if is_valid_cell(temp) and b[temp[0]][temp[1]].piece.side is None:
                self.possible_cells.append(temp)
            elif is_valid_cell(temp) and b[temp[0]][temp[1]].piece.side == self.oppo:
                self.possible_cells.append(temp)
                break
            else:
                break
        temp = deepcopy(self.CELL)
        # bottom cells
        while True:
            temp = (temp[0] + 1, temp[1])
            if is_valid_cell(temp) and b[temp[0]][temp[1]].piece.side is None:
                self.possible_cells.append(temp)
            elif is_valid_cell(temp) and b[temp[0]][temp[1]].piece.side == self.oppo:
                self.possible_cells.append(temp)
                break
            else:
                break
        temp = deepcopy(self.CELL)
        # right cells
        while True:
            temp = (temp[0], temp[1] + 1)
            if is_valid_cell(temp) and b[temp[0]][temp[1]].piece.side is None:
                self.possible_cells.append(temp)
            elif is_valid_cell(temp) and b[temp[0]][temp[1]].piece.side == self.oppo:
                self.possible_cells.append(temp)
                break
            else:
                break
        temp = deepcopy(self.CELL)
        # top cells
        while True:
            temp = (temp[0] - 1, temp[1])
            if is_valid_cell(temp) and b[temp[0]][temp[1]].piece.side is None:
                self.possible_cells.append(temp)
            elif is_valid_cell(temp) and b[temp[0]][temp[1]].piece.side == self.oppo:
                self.possible_cells.append(temp)
                break
            else:
                break
        return self.possible_cells


class Knight(Piece):
    def __init__(self):
        super().__init__()
        self.name = 'n'
        self.temp = deepcopy(self.CELL)
        self.moves = []

    def update_moves(self):
        self.moves = [
            (self.temp[0] - 2, self.temp[1] - 1),
            (self.temp[0] - 2, self.temp[1] + 1),
            (self.temp[0] - 1, self.temp[1] + 2),
            (self.temp[0] + 1, self.temp[1] + 2),
            (self.temp[0] + 2, self.temp[1] + 1),
            (self.temp[0] + 2, self.temp[1] - 1),
            (self.temp[0] + 1, self.temp[1] - 2),
            (self.temp[0] - 1, self.temp[1] - 2)
        ]

    def checked_cells(self, b):
        checked_cells = set()
        self.temp = deepcopy(self.CELL)
        for i in range(8):
            self.temp = deepcopy(self.CELL)
            self.update_moves()
            self.temp = self.moves[i]
            if is_valid_cell(self.temp):
                checked_cells.add(self.temp)
        return checked_cells

    def possible_moves(self, b):
        self.possible_cells = []
        self.temp = deepcopy(self.CELL)
        for i in range(8):
            self.temp = deepcopy(self.CELL)
            self.update_moves()
            self.temp = self.moves[i]
            if is_valid_cell(self.temp) and b[self.temp[0]][self.temp[1]].piece.side is None:
                self.possible_cells.append(self.temp)
            elif is_valid_cell(self.temp) and b[self.temp[0]][self.temp[1]].piece.side == self.oppo:
                self.possible_cells.append(self.temp)
        return self.possible_cells


class Bishop(Piece):
    def __init__(self):
        super().__init__()
        self.name = 'b'

    def checked_cells(self, b):
        checked_cells = set()
        temp = deepcopy(self.CELL)
        # top left cells
        while True:
            temp = temp[0] - 1, temp[1] - 1

            if is_valid_cell(temp):
                if b[temp[0]][temp[1]].piece.side is None or (
                        b[temp[0]][temp[1]].piece.name == 'k' and b[temp[0]][temp[1]].piece.side == self.oppo):
                    checked_cells.add(temp)
                else:
                    checked_cells.add(temp)
                    break
            else:
                break
        temp = deepcopy(self.CELL)
        # top right cells
        while True:
            temp = temp[0] - 1, temp[1] + 1

            if is_valid_cell(temp):
                if b[temp[0]][temp[1]].piece.side is None or (
                        b[temp[0]][temp[1]].piece.name == 'k' and b[temp[0]][temp[1]].piece.side == self.oppo):
                    checked_cells.add(temp)
                else:
                    checked_cells.add(temp)
                    break
            else:
                break
        temp = deepcopy(self.CELL)
        # bottom right cells
        while True:
            temp = temp[0] + 1, temp[1] + 1

            if is_valid_cell(temp):
                if b[temp[0]][temp[1]].piece.side is None or (
                        b[temp[0]][temp[1]].piece.name == 'k' and b[temp[0]][temp[1]].piece.side == self.oppo):
                    checked_cells.add(temp)
                else:
                    checked_cells.add(temp)
                    break
            else:
                break
        temp = deepcopy(self.CELL)
        # bottom left cells
        while True:
            temp = temp[0] + 1, temp[1] - 1

            if is_valid_cell(temp):
                if b[temp[0]][temp[1]].piece.side is None or (
                        b[temp[0]][temp[1]].piece.name == 'k' and b[temp[0]][temp[1]].piece.side == self.oppo):
                    checked_cells.add(temp)
                else:
                    checked_cells.add(temp)
                    break
            else:
                break
        return checked_cells

    def possible_moves(self, b):
        self.possible_cells = []
        temp = deepcopy(self.CELL)
        # top left cells
        while True:
            temp = temp[0] - 1, temp[1] - 1
            if is_valid_cell(temp) and b[temp[0]][temp[1]].piece.side is None:
                self.possible_cells.append(temp)
            elif is_valid_cell(temp) and b[temp[0]][temp[1]].piece.side == self.oppo:
                self.possible_cells.append(temp)
                break
            else:
                break
        temp = deepcopy(self.CELL)
        # top right cells
        while True:
            temp = temp[0] - 1, temp[1] + 1
            if is_valid_cell(temp) and b[temp[0]][temp[1]].piece.side is None:
                self.possible_cells.append(temp)
            elif is_valid_cell(temp) and b[temp[0]][temp[1]].piece.side == self.oppo:
                self.possible_cells.append(temp)
                break
            else:
                break
        temp = deepcopy(self.CELL)
        # bottom right cells
        while True:
            temp = temp[0] + 1, temp[1] + 1
            if is_valid_cell(temp) and b[temp[0]][temp[1]].piece.side is None:
                self.possible_cells.append(temp)
            elif is_valid_cell(temp) and b[temp[0]][temp[1]].piece.side == self.oppo:
                self.possible_cells.append(temp)
                break
            else:
                break
        temp = deepcopy(self.CELL)
        # bottom left cells
        while True:
            temp = temp[0] + 1, temp[1] - 1
            if is_valid_cell(temp) and b[temp[0]][temp[1]].piece.side is None:
                self.possible_cells.append(temp)
            elif is_valid_cell(temp) and b[temp[0]][temp[1]].piece.side == self.oppo:
                self.possible_cells.append(temp)
                break
            else:
                break
        return self.possible_cells


class Queen(Piece):
    def __init__(self):
        super().__init__()
        self.name = 'q'

    def checked_cells(self, b):
        checked_cells = set()
        temp = deepcopy(self.CELL)
        # left cells
        while True:
            temp = temp[0], temp[1] - 1

            if is_valid_cell(temp):
                if b[temp[0]][temp[1]].piece.side is None or (
                        b[temp[0]][temp[1]].piece.name == 'k' and b[temp[0]][temp[1]].piece.side == self.side):
                    checked_cells.add(temp)
                else:
                    checked_cells.add(temp)
                    break
            else:
                break
        temp = deepcopy(self.CELL)
        # bottom cells
        while True:
            temp = temp[0] + 1, temp[1]

            if is_valid_cell(temp):
                if b[temp[0]][temp[1]].piece.side is None or (
                        b[temp[0]][temp[1]].piece.name == 'k' and b[temp[0]][temp[1]].piece.side == self.oppo):
                    checked_cells.add(temp)
                else:
                    checked_cells.add(temp)
                    break
            else:
                break
        temp = deepcopy(self.CELL)
        # right cells
        while True:
            temp = temp[0], temp[1] + 1

            if is_valid_cell(temp):
                if b[temp[0]][temp[1]].piece.side is None or (
                        b[temp[0]][temp[1]].piece.name == 'k' and b[temp[0]][temp[1]].piece.side == self.oppo):
                    checked_cells.add(temp)
                else:
                    checked_cells.add(temp)
                    break
            else:
                break
        temp = deepcopy(self.CELL)
        # top cells
        while True:
            temp = temp[0] - 1, temp[1]

            if is_valid_cell(temp):
                if b[temp[0]][temp[1]].piece.side is None or (
                        b[temp[0]][temp[1]].piece.name == 'k' and b[temp[0]][temp[1]].piece.side == self.oppo):
                    checked_cells.add(temp)
                else:
                    checked_cells.add(temp)
                    break
            else:
                break
        temp = deepcopy(self.CELL)
        # top left cells
        while True:
            temp = temp[0] - 1, temp[1] - 1

            if is_valid_cell(temp):
                if b[temp[0]][temp[1]].piece.side is None or (
                        b[temp[0]][temp[1]].piece.name == 'k' and b[temp[0]][temp[1]].piece.side == self.oppo):
                    checked_cells.add(temp)
                else:
                    checked_cells.add(temp)
                    break
            else:
                break
        temp = deepcopy(self.CELL)
        # top right cells
        while True:
            temp = temp[0] - 1, temp[1] + 1

            if is_valid_cell(temp):
                if b[temp[0]][temp[1]].piece.side is None or (
                        b[temp[0]][temp[1]].piece.name == 'k' and b[temp[0]][temp[1]].piece.side == self.oppo):
                    checked_cells.add(temp)
                else:
                    checked_cells.add(temp)
                    break
            else:
                break
        temp = deepcopy(self.CELL)
        # bottom right cells
        while True:
            temp = temp[0] + 1, temp[1] + 1

            if is_valid_cell(temp):
                if b[temp[0]][temp[1]].piece.side is None or (
                        b[temp[0]][temp[1]].piece.name == 'k' and b[temp[0]][temp[1]].piece.side == self.oppo):
                    checked_cells.add(temp)
                else:
                    checked_cells.add(temp)
                    break
            else:
                break
        temp = deepcopy(self.CELL)
        # bottom left cells
        while True:
            temp = temp[0] + 1, temp[1] - 1

            if is_valid_cell(temp):
                if b[temp[0]][temp[1]].piece.side is None or (
                        b[temp[0]][temp[1]].piece.name == 'k' and b[temp[0]][temp[1]].piece.side == self.oppo):
                    checked_cells.add(temp)
                else:
                    checked_cells.add(temp)
                    break
            else:
                break
        return checked_cells

    def possible_moves(self, b):
        self.possible_cells = []
        temp = deepcopy(self.CELL)
        # left cells
        while True:
            temp = temp[0], temp[1] - 1
            if is_valid_cell(temp) and b[temp[0]][temp[1]].piece.side is None:
                self.possible_cells.append(temp)
            elif is_valid_cell(temp) and b[temp[0]][temp[1]].piece.side == self.oppo:
                self.possible_cells.append(temp)
                break
            else:
                break
        temp = deepcopy(self.CELL)
        # bottom cells
        while True:
            temp = temp[0] + 1, temp[1]
            if is_valid_cell(temp) and b[temp[0]][temp[1]].piece.side is None:
                self.possible_cells.append(temp)
            elif is_valid_cell(temp) and b[temp[0]][temp[1]].piece.side == self.oppo:
                self.possible_cells.append(temp)
                break
            else:
                break
        temp = deepcopy(self.CELL)
        # right cells
        while True:
            temp = temp[0], temp[1] + 1
            if is_valid_cell(temp) and b[temp[0]][temp[1]].piece.side is None:
                self.possible_cells.append(temp)
            elif is_valid_cell(temp) and b[temp[0]][temp[1]].piece.side == self.oppo:
                self.possible_cells.append(temp)
                break
            else:
                break
        temp = deepcopy(self.CELL)
        # top cells
        while True:
            temp = temp[0] - 1, temp[1]
            if is_valid_cell(temp) and b[temp[0]][temp[1]].piece.side is None:
                self.possible_cells.append(temp)
            elif is_valid_cell(temp) and b[temp[0]][temp[1]].piece.side == self.oppo:
                self.possible_cells.append(temp)
                break
            else:
                break
        temp = deepcopy(self.CELL)
        # top left cells
        while True:
            temp = temp[0] - 1, temp[1] - 1
            if is_valid_cell(temp) and b[temp[0]][temp[1]].piece.side is None:
                self.possible_cells.append(temp)
            elif is_valid_cell(temp) and b[temp[0]][temp[1]].piece.side == self.oppo:
                self.possible_cells.append(temp)
                break
            else:
                break
        temp = deepcopy(self.CELL)
        # top right cells
        while True:
            temp = temp[0] - 1, temp[1] + 1
            if is_valid_cell(temp) and b[temp[0]][temp[1]].piece.side is None:
                self.possible_cells.append(temp)
            elif is_valid_cell(temp) and b[temp[0]][temp[1]].piece.side == self.oppo:
                self.possible_cells.append(temp)
                break
            else:
                break
        temp = deepcopy(self.CELL)
        # bottom right cells
        while True:
            temp = temp[0] + 1, temp[1] + 1
            if is_valid_cell(temp) and b[temp[0]][temp[1]].piece.side is None:
                self.possible_cells.append(temp)
            elif is_valid_cell(temp) and b[temp[0]][temp[1]].piece.side == self.oppo:
                self.possible_cells.append(temp)
                break
            else:
                break
        temp = deepcopy(self.CELL)
        # bottom left cells
        while True:
            temp = temp[0] + 1, temp[1] - 1
            if is_valid_cell(temp) and b[temp[0]][temp[1]].piece.side is None:
                self.possible_cells.append(temp)
            elif is_valid_cell(temp) and b[temp[0]][temp[1]].piece.side == self.oppo:
                self.possible_cells.append(temp)
                break
            else:
                break
        return self.possible_cells


class King(Piece):
    def __init__(self):
        super().__init__()
        self.name = 'k'
        self.temp = deepcopy(self.CELL)
        self.moves = []
        self.king_in_check = False
        self.moved = False
        self.right_squares = None
        self.left_squares = None

    def update_moves(self):
        self.moves = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 or j != 0:
                    self.moves.append((self.temp[0] + i, self.temp[1] + j))

    def update_is_in_check(self, cells: set):
        if self.CELL in cells:
            self.king_in_check = True
        else:
            self.king_in_check = False

    def square_in_check(self, cell, cells: set):
        return cell in cells

    def checked_cells(self, b):
        checked_cells = set()
        self.temp = deepcopy(self.CELL)
        for i in range(8):
            self.temp = deepcopy(self.CELL)
            self.update_moves()
            self.temp = self.moves[i]
            if is_valid_cell(self.temp):
                checked_cells.add(self.temp)
        return checked_cells

    def possible_moves(self, b, checked_cells: set = None):
        self.possible_cells = []
        self.temp = deepcopy(self.CELL)
        for i in range(8):
            self.temp = deepcopy(self.CELL)
            self.update_moves()
            self.temp = self.moves[i]
            if is_valid_cell(self.temp) and \
                    b[self.temp[0]][self.temp[1]].piece.side is None and \
                    self.temp not in checked_cells:
                self.possible_cells.append(self.temp)
            elif is_valid_cell(self.temp) and \
                    b[self.temp[0]][self.temp[1]].piece.side == self.oppo and \
                    self.temp not in checked_cells:
                self.possible_cells.append(self.temp)
            if self.moved is False:
                castlable = True
                for cell in self.right_squares:
                    if b[cell[0]][cell[1]].piece.side is not None:
                        castlable = False
                squares_to_be_checked = self.right_squares + [self.CELL]
                for cell in squares_to_be_checked:
                    if self.square_in_check(cell, checked_cells):
                        castlable = False
                if b[7][7].piece.moved:
                    castlable = False
                if castlable:
                    temp = deepcopy(self.CELL)
                    temp = temp[0], temp[1] + 2
                    self.possible_cells.append(temp)
                castlable = True
                for cell in self.left_squares:
                    if b[cell[0]][cell[1]].piece.side is not None:
                        castlable = False
                squares_to_be_checked = self.left_squares + [self.CELL]
                squares_to_be_checked = squares_to_be_checked.pop(2)
                for cell in squares_to_be_checked:
                    if self.square_in_check(cell, checked_cells):
                        castlable = False
                if b[7][0].piece.moved:
                    castlable = False
                if castlable:
                    temp = deepcopy(self.CELL)
                    temp = temp[0], temp[1] - 2
                    self.possible_cells.append(temp)
        return self.possible_cells


class WR(Rook):
    def __init__(self):
        super().__init__()
        super().init('w')


class BR(Rook):
    def __init__(self):
        super().__init__()
        super().init('b')


class WN(Knight):
    def __init__(self):
        super().__init__()
        super().init('w')


class BN(Knight):
    def __init__(self):
        super().__init__()
        super().init('b')


class WB(Bishop):
    def __init__(self):
        super().__init__()
        super().init('w')


class BB(Bishop):
    def __init__(self):
        super().__init__()
        super().init('b')


class WQ(Queen):
    def __init__(self):
        super().__init__()
        super().init('w')


class BQ(Queen):
    def __init__(self):
        super().__init__()
        super().init('b')


class WK(King):
    def __init__(self):
        super().__init__()
        super().init('w')
        self.right_squares = [(7, 5), (7, 6)]
        self.left_squares = [(7, 3), (7, 2), (7, 1)]


class BK(King):
    def __init__(self):
        super().__init__()
        super().init('b')
        self.right_squares = [(0, 5), (0, 6)]
        self.left_squares = [(0, 3), (0, 2), (0, 1)]


class NP(Piece):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"data/N_P.png")
        self.side = None

    def possible_moves(self, b):
        return []

    def __repr__(self) -> str:
        return "NP"


lwr = WR()
rwr = WR()
lwn = WN()
rwn = WN()
lwb = WB()
rwb = WB()
wq = WQ()
wk = WK()
awp, bwp, cwp, dwp, ewp, fwp, gwp, hwp = WP(0), WP(1), WP(2), WP(3), WP(4), WP(5), WP(6), WP(7)

lbr = BR()
rbr = BR()
lbn = BN()
rbn = BN()
lbb = BB()
rbb = BB()
bq = BQ()
bk = BK()
abp, bbp, cbp, dbp, ebp, fbp, gbp, hbp = BP(0), BP(1), BP(2), BP(3), BP(4), BP(5), BP(6), BP(7)


board = np.array([
    [lbr, lbn, lbb, bq, bk, rbb, rbn, rbr],
    [abp, bbp, cbp, dbp, ebp, fbp, gbp, hbp],
    [NP(), NP(), NP(), NP(), NP(), NP(), NP(), NP()],
    [NP(), NP(), NP(), NP(), NP(), NP(), NP(), NP()],
    [NP(), NP(), NP(), NP(), NP(), NP(), NP(), NP()],
    [NP(), NP(), NP(), NP(), NP(), NP(), NP(), NP()],
    [awp, bwp, cwp, dwp, ewp, fwp, gwp, hwp],
    [lwr, lwn, lwb, wq, wk, rwb, rwn, rwr],

])


class Cell:
    def __init__(self, cell: tuple):
        self.number = cell
        self.selected = False
        self.piece = None
        self.color = LIGHT if sum(self.number)%2 == 0 else DARK
        self.coordinates = SIZE_STRIP + self.number[1]*SIZE_CELL, SIZE_STRIP + self.number[0]*SIZE_CELL

    def select(self):
        self.selected = True
        if self.piece.side is None:
            self.color = ELECTRIC_BLUE if sum(self.number)%2 == 0 else DARK_ELECTRIC_BLUE
        else:
            self.color = LIGHT_RED if sum(self.number)%2 == 0 else DARK_RED
        self.update()

    def deselect(self):
        self.selected = False
        self.color = LIGHT if sum(self.number)%2 == 0 else DARK
        self.update()

    def assign(self, piece):
        self.piece = piece
        self.piece.CELL = self.number
        self.piece.temp = deepcopy(self.piece.CELL)
        self.update()

    def unassign(self):
        empty = NP()
        self.piece = empty
        self.update()

    def update(self):
        pygame.draw.rect(screen, self.color, self.coordinates + (SIZE_CELL, SIZE_CELL))
        # image = pygame.image.load(r'data/glass.png')
        # screen.blit(image, self.coordinates)
        screen.blit(self.piece.image, self.coordinates)


class Board:
    def __init__(self):
        self.board = np.empty(shape=(8, 8), dtype='object')
        for i in range(8):
            for j in range(8):
                self.board[i][j] = Cell((i, j))
        self.players = ('b', 'w')
        self.current_player = self.players[1]
        self.move_number = 0
        self.states = ('selected', 'unselected')
        self.state = self.states[1]
        self.cell1 = None
        self.cell2 = None
        self.highlighted_cells = []
        self.checked_by = {'b': set(), 'w': set()}
        self.last_move = {'b': Move(), 'w': Move()}

    def cell(self, cell: tuple) -> Cell:
        return self.board[cell[0]][cell[1]]

    t = 0

    def get_king_position(self, side: str):
        for row in self.board:
            for cell in row:
                if cell.piece.name == 'k' and cell.piece.side == side:
                    self.t += 1
                    return cell.piece.CELL

    def if_check_mated(self):
        king_position = self.get_king_position(self.current_player)
        oppo = 'w' if self.current_player == 'b' else 'b'
        self.update_checked_list(player=oppo)
        self.cell(king_position).piece.update_is_in_check(self.checked_by[oppo])
        check_status = self.cell(king_position).piece.king_in_check
        if not check_status:
            return False
        cells = self.cell(king_position).piece.possible_moves(self.board, self.checked_by[oppo])
        self.highlight_cells(cells)
        if len(cells) > 0:
            return False
        checked_by_pieces = self.checked_by_pieces(king_position)
        if len(checked_by_pieces) == 1:
            eliminated_by_pieces = self.eliminated_by(checked_by_pieces[0])
            if len(eliminated_by_pieces) > 0:
                return False
        return True

    def set_board(self):
        font_size = SIZE_STRIP//2
        font = pygame.font.SysFont('ubuntu', font_size)
        pygame.draw.rect(screen, BLACK, (0, 0, 8*SIZE_CELL + 2*SIZE_STRIP, SIZE_STRIP))
        pygame.draw.rect(screen, BLACK, (
            0, SIZE_STRIP + 8*SIZE_CELL, 8*SIZE_CELL + 2*SIZE_STRIP, 8*SIZE_CELL + 2*SIZE_STRIP))
        pygame.draw.rect(screen, BLACK, (0, SIZE_STRIP, SIZE_STRIP, SIZE_STRIP + 8*SIZE_CELL))
        pygame.draw.rect(screen, BLACK, (
            SIZE_STRIP + 8*SIZE_CELL, SIZE_STRIP, 2*SIZE_STRIP + 8*SIZE_CELL, SIZE_STRIP + 8*SIZE_CELL))

        x = SIZE_STRIP + SIZE_CELL/2 - font_size//4
        for i in range(8):
            label = font.render(H[i], True, (255, 255, 255))
            screen.blit(label, (x, SIZE_STRIP/2 - font_size//1.75))
            screen.blit(label, (x, SIZE_STRIP*3/2 + 8*SIZE_CELL - font_size//2))
            x += SIZE_CELL
        y = SIZE_STRIP + SIZE_CELL/2 - font_size/2
        for i in range(8):
            label = font.render(V[i], True, (255, 255, 255))
            screen.blit(label, (SIZE_STRIP/2 - font_size//4, y))
            screen.blit(label, (SIZE_STRIP*3/2 + 8*SIZE_CELL - font_size//2, y))
            y += SIZE_CELL

        for i in range(8):
            for j in range(8):
                self.cell((i, j)).assign(board[i][j])

    def update_checked_list(self, player=None):
        if player is None:
            oppo = 'w' if self.current_player == 'b' else 'b'
        else:
            oppo = player
        self.checked_by[oppo] = set()
        for row in self.board:
            for cell in row:
                if cell.piece.side == oppo:
                    self.checked_by[oppo] |= cell.piece.checked_cells(self.board)

    def checked_by_pieces(self, cell: tuple):
        checked_by_pieces = []
        current_piece_side = self.cell(cell).piece.side
        oppo = 'w' if current_piece_side == 'b' else 'b'
        for row in self.board:
            for c in row:
                piece = c.piece
                if piece.side == oppo:
                    checked_cells = piece.checked_cells(self.board)
                    if cell in checked_cells:
                        checked_by_pieces.append(piece.CELL)
        return checked_by_pieces

    def eliminated_by(self, cell: tuple):
        eliminated_by = []
        current_piece_side = self.cell(cell).piece.side
        oppo = 'w' if current_piece_side == 'b' else 'b'
        for row in self.board:
            for c in row:
                piece = c.piece
                if piece.side == oppo:
                    if piece.name != 'k':
                        if piece.name != 'p':
                            possible_cells = piece.possible_moves(self.board)
                        else:
                            possible_cells = piece.possible_moves(self.board, self.last_move[oppo])
                    else:
                        possible_cells = piece.possible_moves(self.board, self.checked_by[oppo])
                    if cell in possible_cells:
                        eliminated_by.append(piece.CELL)
        return eliminated_by

    def move(self):
        oppo = 'w' if self.current_player == 'b' else 'b'
        # en-passant move
        if self.cell(self.cell1).piece.name == 'p':
            if self.cell(self.cell2).piece.side is None and self.cell1[1] != self.cell2[1]:
                self.cell(self.cell2).assign(self.cell(self.cell1).piece)
                self.cell(self.cell1).unassign()
                temp = deepcopy(self.cell2)
                if self.cell(self.cell2).piece.side == self.players[0]:
                    temp = temp[0] - 1, temp[1]
                    self.cell(temp).unassign()
                else:
                    temp = temp[0] + 1, temp[1]
                    self.cell(temp).unassign()
                self.last_move[self.current_player].moved(self.cell(self.cell2).piece, self.cell1, self.cell2,
                                                          self.move_number)
                self.current_player = self.players[self.move_number%2]
                self.move_number += 1
                return
        # king move
        if self.cell(self.cell1).piece.name == 'k':
            if abs(self.cell2[1] - self.cell1[1]) == 2:
                self.cell(self.cell2).assign(self.cell(self.cell1).piece)
                self.cell(self.cell1).unassign()
                if self.cell2[1] == 6:
                    temp1 = self.cell2[0], self.cell2[1] + 1
                    temp2 = self.cell2[0], self.cell2[1] - 1
                elif self.cell2[1] == 2:
                    temp1 = self.cell2[0], self.cell2[1] - 2
                    temp2 = self.cell2[0], self.cell2[1] + 1
                self.cell(temp2).assign(self.cell(temp1).piece)
                self.cell(temp1).unassign()
            else:
                self.cell(self.cell2).assign(self.cell(self.cell1).piece)
                self.cell(self.cell1).unassign()
            self.cell(self.cell2).piece.moved = True
            self.last_move[self.current_player].moved(self.cell(self.cell2).piece, self.cell1, self.cell2,
                                                      self.move_number)
            self.current_player = self.players[self.move_number%2]
            self.move_number += 1
            return
        if self.cell(self.cell1).piece.name == 'r':
            self.cell(self.cell2).assign(self.cell(self.cell1).piece)
            self.cell(self.cell1).unassign()
            self.cell(self.cell2).piece.moved = True
            self.last_move[self.current_player].moved(self.cell(self.cell2).piece, self.cell1, self.cell2,
                                                      self.move_number)
            self.current_player = self.players[self.move_number%2]
            self.move_number += 1
            return
        self.cell(self.cell2).assign(self.cell(self.cell1).piece)
        self.cell(self.cell1).unassign()
        self.last_move[self.current_player].moved(self.cell(self.cell2).piece, self.cell1, self.cell2, self.move_number)
        self.current_player = self.players[self.move_number%2]
        self.move_number += 1

    def is_valid_selection(self, cell: tuple):
        return cell is not None and self.cell(cell).piece.side == self.current_player

    def deselecting_move(self, cell: tuple):
        if cell is not None:
            if self.cell1 == cell:
                return True
            if self.cell(cell).piece.side is None and cell not in self.highlighted_cells:
                return True

    def piece_changing_move(self, cell: tuple):
        return cell is not None and self.cell(cell).piece.side == self.current_player

    def is_valid_move(self, cell2: tuple):
        return cell2 is not None and self.cell(
            cell2).piece.side != self.current_player and cell2 in self.highlighted_cells

    def highlight(self, cell: tuple):
        oppo = 'w' if self.current_player == 'b' else 'b'
        if self.cell(cell).piece.name == 'k':
            cells = self.cell(cell).piece.possible_moves(self.board, self.checked_by[oppo])
        elif self.cell(cell).piece.name == 'p':
            cells = self.cell(cell).piece.possible_moves(self.board, self.last_move[oppo], self.move_number)
        else:
            cells = self.cell(cell).piece.possible_moves(self.board)
        for square in cells:
            self.cell(square).select()
        self.highlighted_cells = cells
        return len(cells)

    def highlight_cells(self, cells: set):
        for c in cells:
            cell = self.cell(c)
            if cell.piece.side is None:
                cell.color = ELECTRIC_BLUE if sum(cell.number)%2 == 0 else DARK_ELECTRIC_BLUE
            else:
                cell.color = LIGHT_RED if sum(cell.number)%2 == 0 else DARK_RED
            cell.update()

    def unhighlight_cells(self):
        for row in self.board:
            for cell in row:
                cell.color = LIGHT if sum(cell.number)%2 == 0 else DARK
                cell.update()

    def unhighlight(self):
        for square in self.highlighted_cells:
            self.cell(square).deselect()
        self.highlighted_cells = []

    def get_cell(self, event):
        x = event.pos[0]
        y = event.pos[1]
        row = (y - SIZE_STRIP)//SIZE_CELL
        col = (x - SIZE_STRIP)//SIZE_CELL
        if row in range(8) and col in range(8):
            return row, col
        else:
            return None

    def get_move(self, event):
        if self.state == self.states[1]:
            cell1 = self.get_cell(event)
            if self.is_valid_selection(cell1):
                number = self.highlight(cell1)
                if number > 0:
                    self.state = self.states[0]
                    self.cell1 = cell1
                    return
        elif self.state == self.states[0]:
            cell2 = self.get_cell(event)
            if self.is_valid_move(cell2):
                self.cell2 = cell2
                self.state = self.states[1]
                if self.cell1 is not None and self.cell2 is not None:
                    self.move()
                    self.unhighlight()
                    self.cell1 = None
                    self.cell2 = None
                    status = self.if_check_mated()
                    if status:
                        Tk().wm_withdraw()
                        messagebox.showinfo('', 'Game Over')
            elif self.deselecting_move(cell2):
                self.cell1 = None
                self.cell2 = None
                self.state = self.states[1]
                self.unhighlight()

            elif self.piece_changing_move(cell2):
                self.unhighlight()
                cell1 = cell2
                cell2 = None
                if self.is_valid_selection(cell1):
                    number = self.highlight(cell1)
                    if number > 0:
                        self.state = self.states[0]
                        self.cell1 = cell1
                        return


def is_valid_cell(cell: tuple):
    return cell[0] in range(8) and cell[1] in range(8)


def main():
    pygame.init()
    pygame.time.Clock().tick(60)
    pygame.display.set_caption("Chess")
    b = Board()
    b.set_board()
    b.update_checked_list(player='b')
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                b.unhighlight_cells()
                b.get_move(event)
        pygame.display.flip()


if __name__ == "__main__":
    main()
