from collections import defaultdict

import numpy as np

from day import Day


class BeaconVector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

        self._facings = None

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def dist(self, other):
        return sum(map(abs, self.diff(other)))

    def diff(self, other):
        return self.x - other.x, self.y - other.y, self.z - other.z

    def __repr__(self):
        return str((self.x, self.y, self.z))

    @property
    def facings(self):
        if not self._facings:
            self._facings = list(self._make_facings())
        return self._facings

    def _make_facings(self):
        # shamelessly stolen, because i suck at vector math.
        vector = np.array([self.x, self.y, self.z])
        rotations = list(map(np.array, [
            (1, 0, 0),
            (-1, 0, 0),
            (0, 1, 0),
            (0, -1, 0),
            (0, 0, 1),
            (0, 0, -1),
        ]))
        for vec_x in rotations:
            for vec_y in rotations:
                if vec_x.dot(vec_y) == 0:
                    vec_z = np.cross(vec_x, vec_y)
                    vec = np.matmul(vector, np.array([vec_x, vec_y, vec_z]))
                    yield BeaconVector(*vec)


class Scanner:
    def __init__(self, name, beacons):
        self.beacons = beacons
        self.name = name

        self.facing = 0
        self.offset = (0, 0, 0)

    def rotated(self, x, y, z):
        return [beacon.rotated(x, y, z) for beacon in self.beacons]

    def relative_positions(self, face):
        rel_pos = defaultdict(set)

        for beacon in self.beacons:
            for other in self.beacons:
                if beacon is other:
                    continue

                rel_pos[beacon].add(beacon.facings[face].diff(other.facings[face]))

        return rel_pos

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return self.name

    def overlap(self, other):
        rel_pos = other.relative_positions(other.facing)

        for facing in range(24):
            other_pos = self.relative_positions(facing)

            for key, value in rel_pos.items():
                for key2, value2 in other_pos.items():
                    # if both have the same neighborhood (at least 11 matching neighbors), we have a match
                    if len(value & value2) > 10:
                        matches = key.facings[other.facing].diff(key2.facings[facing])
                        return matches, facing

        return None, None

    def normalized(self):
        return [(
            beacon.facings[self.facing].x + self.offset[0],
            beacon.facings[self.facing].y + self.offset[1],
            beacon.facings[self.facing].z + self.offset[2],
        ) for beacon in self.beacons]


class Day19(Day):
    def parse(self, content):
        scanners = content.split('\n\n')
        results = []

        for scanner in scanners:
            beacons = []
            lines = scanner.split('\n')
            for line in lines[1:]:
                x, y, z = list(map(int, line.split(',')))
                beacons.append(BeaconVector(x, y, z))

            results.append(Scanner(lines[0], beacons))
        return results

    def get_unique(self):
        all_points = set((beacon.x, beacon.y, beacon.z) for beacon in self.input[0].beacons)
        queue = [self.input[0]]
        found = {self.input[0]}

        while queue:
            start = queue.pop(0)

            for item in self.input:
                if item in found:
                    # already found the offset and beacons of this scanner
                    continue

                offset, facing = item.overlap(start)
                if not offset:
                    # no match found
                    continue

                item.offset = (
                    start.offset[0] + offset[0],
                    start.offset[1] + offset[1],
                    start.offset[2] + offset[2],
                )
                item.facing = facing

                for point in item.normalized():
                    all_points.add(point)

                # now that we know the offset, we can test other scanners against this
                queue.append(item)
                found.add(item)

        return all_points

    def part1(self):
        # takes about 10sec ...sorry
        return len(self.get_unique())

    def part2(self):
        # note: requires part1 to be run first (because that sets the offsets on the input scanners)
        scanners = [BeaconVector(*scan.offset) for scan in self.input]
        return max([scanner.dist(other) for other in scanners for scanner in scanners])
