from day import Day


class Day07(Day):

    def parse(self, content):
        return [int(i) for i in super().parse(content)[0].split(',')]

    def gauss(self, val):
        return (val * (val + 1)) // 2

    def solve(self, use_sum=False):
        min_val = min(self.input)
        max_val = max(self.input)
        min_fuel = sum(self.gauss(x) for x in self.input) if use_sum else sum(self.input)

        for i in range(min_val, max_val):
            fuel = 0
            for val in self.input:
                fuel += self.gauss(abs(val - i)) if use_sum else abs(val - i)

            if fuel < min_fuel:
                min_fuel = fuel

        return min_fuel

    def part1(self):
        return self.solve()

    def part2(self):
        return self.solve(True)
