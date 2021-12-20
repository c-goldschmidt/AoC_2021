from functools import lru_cache

from day import Day
from utils.grid import Grid
from utils.timer import Timer


class PixelGrid(Grid):
    enhance = None
    fallback = 0

    def clone(self):
        grid = super().clone()
        grid.enhance = self.enhance
        return grid

    def cell_to_string(self, x, y):
        if self[(x, y)] in (0, 1):
            return '#' if self[(x, y)] == 1 else '.'
        return self[(x, y)]

    def get_enhanced(self):
        self.min_y -= 1
        self.min_x -= 1
        self.max_y += 1
        self.max_x += 1
        result_grid = self.clone()

        # set "infinite" area pixel value for next generation
        result_grid.fallback = self.enhance[-1 if self.fallback == 1 else 0]

        for point in self.iter_points():
            value = ''.join([str(self[p]) for p in self._next(point)])
            result_grid[point] = self.enhance[int(value, 2)]

        return result_grid

    def value(self):
        return sum(self.iter_values())

    def _next(self, point):
        return sorted([*point.neighbors(True), point], key=lambda p: (p.y, p.x))


class Day20(Day):
    def parse(self, content):
        grid = PixelGrid()
        parts = content.split('\n\n')

        grid.enhance = [int(x == '#') for x in parts[0]]

        for y, line in enumerate(super().parse(parts[1])):
            for x, col in enumerate(line):
                grid[(x, y)] = int(col == '#')

        grid.fixed_bounds = True
        return grid

    def _enhance(self, times):
        result = self.input
        for i in range(times):
            result = result.get_enhanced()
        return result

    def part1(self):
        return self._enhance(2).value()

    def part2(self):
        # takes 30sec ...sorry again...
        return self._enhance(50).value()
