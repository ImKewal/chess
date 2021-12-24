from copy import deepcopy
class a:
    def __init__(self):
        self.CELL = (5, 6)
        self.side = None
        self.name = None
        self.image = None
        self.oppo = None
        self.temp = None
        self.moves = []
        self.possible_cells = []

    def init(self, side):
        self.side = side
        self.image = rf"data/{self.side.upper()}_{self.name.upper()}"
        self.oppo = 'b' if self.side == 'w' else 'w'
        self.temp = deepcopy(self.CELL)

    def get_moves(self):
        for temp in self.moves:
            self.temp = temp

    def get_single_move(self):
        if is_valid_cell(self.temp) and b[self.temp[0]][self.temp[1]].piece.side is None:
            self.possible_cells.append(self.temp)
        elif is_valid_cell(self.temp) and b[self.temp[0]][self.temp[1]].piece.side == self.oppo:
            self.possible_cells.append(self.temp)

    def get_multiple_moves(self):
        for temp in self.moves:
            self.temp = temp
            if is_valid_cell(self.temp) and b[]


class b(a):
    def __init__(self):
        super().__init__()
        self.name = 'r'
        self.moves = [
            (self.temp[0], self.temp[1] - 1), (self.temp[0] + 1, self.temp[1]),
            (self.temp[0], self.temp[1] + 1), (self.temp[0] - 1, self.temp[1])
        ]


class c(b):
    def __init__(self):
        super().__init__()
        side = 'w'
        super().init(side)


def is_valid_cell(cell: tuple):
    return cell[0] in range(0, 8) and cell[1] in range(0, 8)


ia = a()
ib = b()
ic = c()

print(ic.side)
print(ic.image)
print(ic.oppo)
