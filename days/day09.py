from day import Day
from utils.grid import Grid


class DepthGrid(Grid):
    def is_low_point(self, point):
        at_point = self[point]
        for p in point.neighbors():
            if not self.in_bounds(p):
                continue

            if self[p] <= at_point:
                return False
        return True

    def get_basin_size(self, point):
        seen = set()
        stack = [point]

        while stack:
            point = stack.pop()
            seen.add(point)

            for p in point.neighbors():
                if not self.in_bounds(p) or self[p] >= 9:
                    continue

                if p not in seen:
                    stack.append(p)

        return len(seen)

    def get_risk_level(self):
        risk_level = 0
        for point in self.iter_points():
            if self.is_low_point(point):
                risk_level += self[point] + 1
        return risk_level

    def get_total_basins(self):
        basins = []
        for point in self.iter_points():
            if self.is_low_point(point):
                basins.append(self.get_basin_size(point))

        basins = list(sorted(basins, reverse=True))
        return basins[0] * basins[1] * basins[2]


class Day09(Day):

    def parse(self, content):
        grid = DepthGrid()

        for y, line in enumerate(super().parse(content)):
            for x, col in enumerate(line):
                grid[(x, y)] = int(col)

        return grid

    def part1(self):
        return self.input.get_risk_level()

    def part2(self):
        return self.input.get_total_basins()
