from collections import defaultdict

from day import Day


class Day14(Day):
    def parse(self, content):
        content = content.split('\n\n')
        start = content[0]
        replacements = {}

        for line in content[1].split('\n'):
            if not line:
                continue

            replace = line.split(' -> ')
            replacements[replace[0]] = replace[1]
        return start, replacements

    def _make_pairs(self, string_in: str):
        pairs_out = defaultdict(int)
        overlaps = defaultdict(int)

        for i in range(0, len(string_in) - 1):
            pair = string_in[i] + string_in[i+1]
            pairs_out[pair] += 1

            if i > 0:
                overlaps[string_in[i]] += 1

        return pairs_out, overlaps

    def _replace_pairs(self, pairs, overlaps):
        result = defaultdict(int)

        for pair, current in pairs.items():
            sub = self.input[1].get(pair)
            overlaps[sub] += current

            result[f'{pair[0]}{sub}'] += current
            result[f'{sub}{pair[1]}'] += current

        return result

    def _counts(self, pairs, overlaps):
        counts = defaultdict(int)
        for pair, value in pairs.items():
            counts[pair[0]] += value
            counts[pair[1]] += value

        for key, value in overlaps.items():
            if key in counts:
                counts[key] -= value

        return list(sorted(counts.values()))

    def _solve(self, count):
        pairs, overlaps = self._make_pairs(self.input[0])

        for _ in range(count):
            pairs = self._replace_pairs(pairs, overlaps)

        counts = self._counts(pairs, overlaps)
        return counts[-1] - counts[0]

    def part1(self):
        return self._solve(10)

    def part2(self):
        return self._solve(40)
