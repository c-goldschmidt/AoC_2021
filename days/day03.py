from day import Day


class Day03(Day):

    def _atoi(self, value):
        if not isinstance(value, str):
            value = ''.join([str(i) for i in value])
        return int(value, 2)

    def _get_common_bits(self, from_value=None):
        if not from_value:
            from_value = self.input

        bits = len(from_value[0])
        sums = [0] * bits

        for line in from_value:
            for i in range(bits):
                sums[i] += int(line[i])

        most_common = [int((sums[i] / len(from_value)) >= .5) for i in range(bits)]
        least_common = [int(not i) for i in most_common]
        return most_common, least_common

    def _filter_list(self, use_most_common):
        current = [*self.input]
        index = 0
        while len(current) > 1:
            most_common, least_common = self._get_common_bits(current)
            commons = most_common if use_most_common else least_common
            current = [item for item in current if int(item[index]) == commons[index]]
            index += 1

        return current[0] if current else None

    def part1(self):
        most_common, least_common = self._get_common_bits()
        return self._atoi(most_common) * self._atoi(least_common)

    def part2(self):
        oxy = self._filter_list(True)
        co2 = self._filter_list(False)
        return self._atoi(oxy) * self._atoi(co2)
