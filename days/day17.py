import re

from day import Day
from utils.grid import Grid

rx_parse = re.compile(r'x=(?P<x0>-?\d+)\.\.(?P<x1>-?\d+), y=(?P<y0>-?\d+)\.\.(?P<y1>-?\d+)')


class AimGrid(Grid):

    def __init__(self, target_x, target_y):
        super().__init__()
        self.target_x = target_x
        self.target_y = target_y

    def _clone_instance(self):
        return self.__class__(self.target_x, self.target_y)

    def fire(self, x_vel, y_vel):
        x = y = max_y = 0

        while True:
            x += x_vel
            y += y_vel
            max_y = max(max_y, y)

            self[(x, y)] = '#'
            if self.target_x[0] <= x <= self.target_x[1] and self.target_y[0] <= y <= self.target_y[1]:
                return True, max_y
            elif x > self.target_x[1] or y < self.target_y[0]:  # this might need tweaking if your target is at -x
                return False, None

            if x_vel > 0:
                x_vel -= 1
            elif x_vel < 0:
                x_vel += 1

            y_vel -= 1


class Day17(Day):
    def parse(self, content):
        match = rx_parse.search(content)
        x0 = int(match.group('x0'))
        x1 = int(match.group('x1'))
        y0 = int(match.group('y0'))
        y1 = int(match.group('y1'))

        grid = AimGrid((x0, x1), (y0, y1))
        return grid

    def _fire(self):
        max_x_vel = max([abs(t) + 1 for t in self.input.target_x])
        max_y_vel = max([abs(t) + 1 for t in self.input.target_y])

        max_y = 0
        hits = 0
        for y_vel in range(-max_y_vel, max_y_vel):
            # this might need tweaking if your target zone is at -x or directly below
            for x_vel in range(1, max_x_vel):
                clone = self.input.clone()
                result, max_shot_y = clone.fire(x_vel, y_vel)
                if result:
                    hits += 1
                    max_y = max(max_y, max_shot_y)

        return max_y, hits

    def part1(self):
        max_y, hits = self._fire()
        return max_y

    def part2(self):
        max_y, hits = self._fire()
        return hits
