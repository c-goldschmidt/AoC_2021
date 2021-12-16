import math

from day import Day


class Operator:
    def __init__(self, version, pkg_type, sub_packages):
        self.version = version
        self.type = pkg_type
        self.sub_packages = sub_packages

    @property
    def total_version(self):
        return self.version + sum(sub.total_version for sub in self.sub_packages)

    @property
    def value(self):
        values = [sub.value for sub in self.sub_packages]
        if self.type == 0:
            return sum(values)
        if self.type == 1:
            return math.prod(values)
        if self.type == 2:
            return min(values)
        if self.type == 3:
            return max(values)
        if self.type == 5:
            return int(values[0] > values[1])
        if self.type == 6:
            return int(values[0] < values[1])
        if self.type == 7:
            return int(values[0] == values[1])


class Literal:
    def __init__(self, version, value):
        self.version = version
        self._value = value

    @property
    def total_version(self):
        return self.version

    @property
    def value(self):
        return self._value


class PackageReader:
    def __init__(self, value):
        self.value = value
        self.offset = 0

    def read_list(self):
        packages = []
        while self.offset < len(self.value):
            packages.append(self.read_package())
            if sum([int(bit) for bit in self.value[self.offset:]]) == 0:
                # only padding ahead
                break

        return packages

    def read_package(self):
        version = self._int(3)
        pkg_type = self._int(3)

        if pkg_type == 4:
            return self._read_literal(version)
        return self._read_operator(version, pkg_type)

    def _read(self, bits):
        value = self.value[self.offset:self.offset + bits]
        self.offset += bits
        return value

    def _int(self, bits):
        return int(self._read(bits), 2)

    def _read_literal(self, version):
        more = True
        number = ''
        while more:
            more = self._int(1)
            number += self._read(4)

        return Literal(version, int(number, 2))

    def _read_operator(self, version, pkg_type):
        op_type = self._int(1)

        if op_type == 0:
            read_len = self._int(15)
            content = self._read(read_len)
            subs = PackageReader(content).read_list()
        else:
            sub_packages = self._int(11)
            subs = []
            for i in range(sub_packages):
                subs.append(self.read_package())

        return Operator(version, pkg_type, subs)


class Day16(Day):
    def parse(self, content):
        bits = len(content) * 4
        lz_format = f'{{0:0{bits}b}}'
        return lz_format.format(int(content, 16))

    def part1(self):
        main_package = PackageReader(self.input).read_package()
        return main_package.total_version

    def part2(self):
        main_package = PackageReader(self.input).read_package()
        return main_package.value
