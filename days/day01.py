from day import Day


class Day01(Day):

    def parse(self, content):
        return [int(line) for line in content.split('\n') if line]

    def part1(self):
        return sum(
            1 if self.input[i] > self.input[i - 1] else 0
            for i in range(1, len(self.input))
        )

    def part2(self):
        return sum(
            1 if sum(self.input[i-2:i+1]) > sum(self.input[i-3:i]) else 0
            for i in range(3, len(self.input))
        )
