import re

from day import Day
from utils.grid import Grid

rx_line = re.compile(r'(\d+),(\d+) -> (\d+),(\d+)')


class VentGrid(Grid):
    fallback = 0

    def cell_to_string(self, x, y):
        if self[(x, y)] == 0:
            return '.'
        return super().cell_to_string(x, y)

    def add_line(self, line, diagonal=False):
        match = rx_line.match(line)
        if not match:
            return

        x1, y1, x2, y2 = [int(g) for g in match.groups()]
        if x1 != x2 and y1 != y2 and not diagonal:
            # only vertical and horizontal...
            return

        if x1 != x2 and y1 != y2:
            iterator = self.iter_diagonal(x1, y1, x2, y2)
        else:
            iterator = self.iter_line(x1, y1, x2, y2)

        for x, y in iterator:
            self[(x, y)] += 1

    def iter_line(self, x1, y1, x2, y2):
        if x1 > x2:
            x1, x2 = (x2, x1)

        if y1 > y2:
            y1, y2 = (y2, y1)

        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                yield x, y

    def iter_diagonal(self, x1, y1, x2, y2):
        while x1 != x2 and y1 != y2:
            yield x1, y1
            x1 += 1 if x2 > x1 else -1
            y1 += 1 if y2 > y1 else -1

        yield x1, y1

    def count_overlap(self):
        return len([val for val in self.iter_values() if val > 1])


class Day05(Day):
    def part1(self):
        grid = VentGrid()
        for line in self.input:
            grid.add_line(line)

        return grid.count_overlap()

    def part2(self):
        grid = VentGrid()
        for line in self.input:
            grid.add_line(line, True)

        return grid.count_overlap()
