import heapq

from day import Day
from utils.grid import Grid
from utils.point import UniquePoint


class RiskGrid(Grid):
    def next(self, point):
        return [n for n in point.neighbors() if self.in_bounds(n)]

    @property
    def end(self):
        return UniquePoint(self.max_x, self.max_y)

    @property
    def start(self):
        return UniquePoint(0, 0)

    def find_least_risky_path(self):
        return self._path(self.start, self.end)

    def _path(self, start, end):
        distance = float('inf')
        distances = {point: distance for point in self.iter_points()}
        distances[start] = 0

        queue = [(0, start)]
        while queue:
            dist, point = heapq.heappop(queue)
            if dist > distances[point]:
                continue

            for neighbor in self.next(point):
                distance = dist + self[neighbor]

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(queue, (distance, neighbor))

        return distances[end]

    def extend(self):
        grid_size = self.max_x + 1
        assert grid_size == self.max_y + 1

        clone = self.clone()
        for i in range(1, 10):
            for point in clone.iter_points():
                new_val = clone[point] + 1
                clone[point] = 1 if new_val >= 10 else new_val

            for y in range(i + 1):
                for x in range(i + 1):
                    if y + x == i and x < 5 and y < 5:
                        self._insert(clone, x, y, grid_size)

    def _insert(self, clone, offset_x, offset_y, grid_size):
        if offset_x == 0 and offset_y == 0:
            return

        for y in range(grid_size):
            dst_y = offset_y * grid_size + y
            for x in range(grid_size):
                dst_x = offset_x * grid_size + x
                self[(dst_x, dst_y)] = clone[(x, y)]


class Day15(Day):
    def parse(self, content):
        grid = RiskGrid()
        for y, line in enumerate(super().parse(content)):
            for x, col in enumerate(line):
                grid[(x, y)] = int(col)
        return grid

    def part1(self):
        return self.input.find_least_risky_path()

    def part2(self):
        grid = self.input.clone()
        grid.extend()
        return grid.find_least_risky_path()
