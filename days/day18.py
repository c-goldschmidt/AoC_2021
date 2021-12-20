import itertools
import math

from day import Day

NUMBERS = tuple(map(str, range(10)))


class Day18(Day):
    """
    def parse(self, content):
        results = []
        for line in super().parse(content):
            results.append(eval(line))
        return results
    """

    def _add(self, a, b):
        return f'[{a},{b}]'

    def _reduce(self, snail):
        exploded = split = True
        while exploded or split:
            exploded = self._check_explode(snail)
            if exploded:
                snail = exploded
                continue

            split = self._check_split(snail)
            if split:
                snail = split

        return snail

    def _explode(self, snail, index):
        array_start = index
        array_end = None
        for i in range(index, len(snail)):
            if snail[i] == ']':
                array_end = i + 1
                break

        array = eval(snail[array_start:array_end])
        left = array[0]
        right = array[1]

        before = snail[:array_start]
        after = snail[array_end:]

        # add left
        number_end = None
        for i in range(len(before) - 1, 0, -1):
            if before[i] not in '[],' and not number_end:
                number_end = i + 1
            elif before[i] in '[],' and number_end:
                number_start = i + 1

                value = int(before[number_start:number_end]) + left
                before = before[:number_start] + str(value) + before[number_end:]
                break

        # add right
        number_start = None
        for i in range(0, len(after)):
            if after[i] not in '[],' and not number_start:
                number_start = i
            elif after[i] in '[],' and number_start:
                number_end = i

                value = int(after[number_start:number_end]) + right
                after = after[:number_start] + str(value) + after[number_end:]
                break

        return before + '0' + after

    def _split(self, value):
        value_str = str(value)
        if value >= 10:
            a = math.floor(value / 2)
            b = math.ceil(value / 2)
            value_str = f'[{a},{b}]'
        return value_str

    def _check_split(self, snail):
        prev = None
        for i, item in enumerate(snail):
            if prev is not None and item not in '[],':
                value = int(snail[i-1:i+1])
                value = self._split(value)
                return snail[:i-1] + value + snail[i+1:]
            elif item not in '[],':
                prev = int(snail[i])
            else:
                prev = None

        return None

    def _check_explode(self, snail):
        depth = 0
        for index, item in enumerate(snail):
            if item == '[':
                depth += 1
                if depth == 5:
                    return self._explode(snail, index)

            if item == ']':
                depth -= 1
        return None

    def _snail_sum(self):
        start = self.input[0]
        for item in self.input[1:]:
            start = self._add(start, item)
            start = self._reduce(start)
        return start

    def _magnitude(self, snail_arr):
        a = snail_arr[0]
        if isinstance(a, list):
            a = self._magnitude(a)

        b = snail_arr[1]
        if isinstance(b, list):
            b = self._magnitude(b)

        return a * 3 + b * 2

    def _max_magnitude(self):
        calculated = set()
        max_val = 0
        for items in itertools.product(self.input, self.input):
            items = tuple(sorted(items))
            item_a, item_b = items
            if item_a == item_b:
                continue

            if items in calculated:
                # no need to calculate the same items twice
                continue
            calculated.add(items)

            value = self._add(item_a, item_b)
            value = self._magnitude(eval(self._reduce(value)))
            max_val = max(max_val, value)
        return max_val

    def part1(self):
        return self._magnitude(eval(self._snail_sum()))

    def part2(self):
        return self._max_magnitude()
