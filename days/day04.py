from collections import defaultdict

from day import Day


class BingoMatrix:

    def __init__(self, lines):
        self.numbers = set()
        self.hit_numbers = set()
        self.winning_number = None

        self.matrix = []
        for line in lines:
            numbers = [int(item) for item in line.split(' ') if item]
            self.numbers |= set(numbers)
            self.matrix.append(numbers)

    def add_number(self, value):
        if self.winning_number is not None:
            return

        self.hit_numbers.add(value)
        all_in_col = defaultdict(lambda: True)
        for y, line in enumerate(self.matrix):
            all_in_line = True
            for x, col in enumerate(line):
                hit = col in self.hit_numbers

                all_in_line = all_in_line and hit
                all_in_col[x] = all_in_col[x] and hit

            if all_in_line:
                self.winning_number = value

        if any(all_in_col.values()):
            self.winning_number = value

    @property
    def value(self):
        return self.winning_number * sum(self.numbers - self.hit_numbers)


class Day04(Day):

    def parse(self, content):
        lines = super().parse(content)
        numbers = [int(item) for item in lines[0].split(',')]
        boards = []
        for i in range(2, len(lines), 6):
            boards.append(BingoMatrix(lines[i:i+5]))

        return boards, numbers

    def solve(self, boards, number, return_winner=True):
        for board in boards:
            board.add_number(number)
            if board.winning_number is not None and return_winner:
                return board
        return None

    def part1(self):
        for number in self.input[1]:
            winning = self.solve(self.input[0], number)
            if winning:
                return winning.value

        return None

    def part2(self):
        boards = self.input[0]

        for number in self.input[1]:
            boards = [board for board in boards if board.winning_number is None]
            if len(boards) == 1:
                winning = self.solve(boards, number)
                if winning:
                    return winning.value
            else:
                self.solve(boards, number, False)

        return None
