from collections import defaultdict

from day import Day


class Day06(Day):

    def parse(self, content):
        return list(map(int, super().parse(content)[0].split(',')))

    def sim(self, days):
        current_gen = defaultdict(int)
        for item in self.input:
            current_gen[item] += 1

        for i in range(days):
            next_gen = defaultdict(int)

            for value, length in current_gen.items():
                if value == 0:
                    next_gen[6] += length
                    next_gen[8] += length
                else:
                    next_gen[value - 1] += length

            current_gen = next_gen

        return sum(current_gen.values())

    def part1(self):
        return self.sim(80)

    def part2(self):
        return self.sim(256)
