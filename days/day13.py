from day import Day
from utils.grid import Grid


class FoldingGrid(Grid):
    fallback = ' '

    def _fix_bounds(self):
        new_x = []
        new_y = []
        for y in self.iter_y():
            for x in self.iter_x():
                if self[(x, y)] == '#':
                    new_x.append(x)
                    new_y.append(y)

        self.min_x = min(new_x)
        self.max_x = max(new_x)
        self.min_y = min(new_y)
        self.max_y = max(new_y)

    def count(self):
        return len([val for val in self.iter_values() if val == '#'])

    def fold(self, horizontal, position):
        if horizontal:
            self._fold_horizontal(position)
        else:
            self._fold_vertical(position)

        self._fix_bounds()

    def _fold_vertical(self, position):
        for y in range(position, self.max_y + 1):
            new_y = position - (y - position)
            for x in self.iter_x():
                current_new = self[(x, new_y)]
                current_old = self[(x, y)]

                if current_new == current_old == ' ':
                    continue

                self[(x, new_y)] = '#'
                self[(x, y)] = ' '

    def _fold_horizontal(self, position):
        for x in range(position, self.max_x + 1):
            new_x = position - (x - position)
            for y in self.iter_y():
                current_new = self[(new_x, y)]
                current_old = self[(x, y)]

                if current_new == current_old == ' ':
                    continue

                self[(new_x, y)] = '#'
                self[(x, y)] = ' '


class Day13(Day):
    def parse(self, content):
        grid = FoldingGrid()
        split = content.split('\n\n')
        for line in split[0].split('\n'):
            x, y = line.split(',')
            grid[(int(x), int(y))] = '#'

        folds = []
        for line in split[1].split('\n'):
            fold, pos = line.split('=')
            folds.append(('x' in fold, int(pos)))

        return grid, folds

    def part1(self):
        grid = self.input[0]
        is_horizontal, pos = self.input[1].pop(0)  # pop from input, so part2 doesn't repeat this fold
        grid.fold(is_horizontal, pos)

        return grid.count()

    def part2(self):
        grid = self.input[0]

        for is_horizontal, pos in self.input[1]:
            grid.fold(is_horizontal, pos)

        return '\n' + grid.to_string()
