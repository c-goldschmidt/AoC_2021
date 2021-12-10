from day import Day


class Day10(Day):

    def check_line(self, line):
        stack = []
        expect = {')': '(', '}': '{', ']': '[', '>': '<'}
        points = {')': 3, ']': 57, '}': 1197, '>': 25137}

        for item in line:
            if item in '([{<':
                stack.append(item)

            if item in expect:
                last_open = stack.pop()
                if last_open != expect[item]:
                    return points[item], None

        close = {v: k for k, v in expect.items()}
        return 0, [close[item] for item in reversed(stack)]

    def get_line_completion_score(self, line):
        invalid, completion = self.check_line(line)
        if invalid:
            return []

        points = {')': 1, ']': 2, '}': 3, '>': 4}
        score = 0
        for item in completion:
            score *= 5
            score += points[item]

        return [score]

    def part1(self):
        points = 0
        for line in self.input:
            line_points, _ = self.check_line(line)
            points += line_points

        return points

    def part2(self):
        scores = []

        for line in self.input:
            scores += self.get_line_completion_score(line)

        return list(sorted(scores))[len(scores) // 2]
