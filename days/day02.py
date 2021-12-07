from day import Day


class Day02(Day):

    def parse(self, content):
        result = []
        for line in super().parse(content):
            direction, value = line.split(' ')
            value = int(value)
            result.append((direction, value))
        return result

    def part1(self):
        x = y = 0

        for direction, value in self.input:
            if direction == 'forward':
                x += value
            elif direction == 'down':
                y += value
            elif direction == 'up':
                y -= value

        return x * y

    def part2(self):
        x = y = 0
        aim = 0

        for direction, value in self.input:
            if direction == 'forward':
                x += value
                y += aim * value
            elif direction == 'down':
                aim += value
            elif direction == 'up':
                aim -= value

        return x * y
