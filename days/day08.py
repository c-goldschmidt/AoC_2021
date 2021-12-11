from collections import defaultdict

from day import Day


class Day08(Day):

    def parse(self, content):
        return [[
            [letter.strip() for letter in item.split(' ') if letter.strip()]
            for item in line.split('|')
        ] for line in super().parse(content)]

    def part1(self):
        count = 0
        for line in self.input:
            items = [item for item in line[1] if len(item) in (2, 3, 4, 7)]
            count += len(items)

        return count

    def _solve_overlaps(self, unknowns, seen_numbers):
        # probably way too complex...
        overlaps = {
            0: {2: 4, 3: 4, 5: 4, 6: 5, 9: 5},
            1: {0: 2, 2: 1, 3: 2, 5: 1, 6: 1, 9: 2},
            2: {0: 4, 3: 4, 5: 3, 6: 4, 9: 4},
            3: {0: 4, 2: 4, 5: 4, 6: 4, 9: 5},
            4: {0: 3, 2: 2, 3: 3, 5: 3, 6: 3, 9: 4},
            5: {0: 4, 2: 3, 3: 4, 6: 5, 9: 5},
            6: {0: 5, 2: 4, 3: 4, 5: 5, 9: 5},
            7: {0: 3, 2: 2, 3: 3, 5: 2, 6: 2, 9: 3},
            8: {0: 6, 2: 5, 3: 5, 5: 5, 6: 6, 9: 6},
            9: {0: 5, 2: 4, 3: 5, 5: 5, 6: 5},
        }

        while unknowns:
            item = unknowns.pop()
            possible = set(overlaps.keys()) - set(seen_numbers.keys())

            can_be = False
            for key in possible:
                if len(item) != overlaps[8][key]:
                    # 8 has all segments lit, so its overlap indicates the required number of segments
                    continue

                can_be = True
                for number, value in seen_numbers.items():
                    overlap = len(set(item) & value)
                    if overlap != overlaps[number][key]:
                        can_be = False

                if can_be:
                    seen_numbers[key] = set(item)
                    break

            if not can_be:
                # no match found, try again...
                unknowns.add(item)

    def _get_output(self, numbers, output):
        numbers_by_letters = {tuple(sorted(letters)): number for number, letters in numbers.items()}

        str_out = ''
        for letters in output:
            number = numbers_by_letters[tuple(sorted(letters))]
            str_out += str(number)

        return int(str_out)

    def solve_line(self, config, output):
        numbers_by_len = {2: 1, 3: 7, 4: 4, 7: 8}
        seen_numbers = {}
        unknowns = set()

        for item in config:
            known = numbers_by_len.get(len(item))
            if known:
                seen_numbers[known] = set(item)
            else:
                unknowns.add(item)

        self._solve_overlaps(unknowns, seen_numbers)
        return self._get_output(seen_numbers, output)

    def part2(self):
        total = 0
        for config, output in self.input:
            total += self.solve_line(config, output)

        return total
