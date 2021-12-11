import copy

from day import Day
from utils.grid import Grid


class OctoGrid(Grid):

    def step(self):
        flashes = 0
        queue = list(self.iter_points())
        while queue:
            point = queue.pop()
            self[point] += 1

            if self[point] == 10:
                flashes += 1
                queue += [p for p in point.neighbors(True) if self.in_bounds(p)]

        for point in self.iter_points():
            if self[point] > 9:
                self[point] = 0

        return flashes


class Day11(Day):

    def parse(self, content):
        grid = OctoGrid()
        for y, line in enumerate(super().parse(content)):
            for x, col in enumerate(line):
                grid[(x, y)] = int(col)
        return grid

    def part1(self):
        grid = copy.deepcopy(self.input)
        total = 0
        for i in range(100):
            total += grid.step()

        return total

    def part2(self):
        grid = copy.deepcopy(self.input)

        flashes = 0
        count = 0
        while flashes != 100:
            count += 1
            flashes = grid.step()

        return count
