# Used in order keep track of the sort states during Block Sort
class QSortState:
    low: int
    high: int
    i: int
    j: int

    def __init__(self, l, h):
        self.low = l
        self.high = h
        self.i = self.low - 1
        self.j = self.low
