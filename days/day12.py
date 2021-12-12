from day import Day


class Node:

    def __init__(self, name):
        self.name = name
        self.big = name.lower() != name
        self.reachable = []
        self.hash = hash(self.name)

    def __hash__(self):
        return self.hash

    def __repr__(self):
        return f'Node {self.name} ({self.big})'


class NodeList(dict):

    def add(self, line):
        names = line.split('-')
        self[names[0]].reachable.append(self[names[1]])
        self[names[1]].reachable.append(self[names[0]])

    def find_paths(self, max_visit=1, start=None, visited=None):
        if not start:
            start = self.start

        if start.name == 'end':
            return [[start]]

        if not visited:
            visited = {}

        visited[start] = visited.get(start, 0) + 1
        max_visited = max([mx for node, mx in visited.items() if not node.big])

        paths = []
        for reach in start.reachable:
            current = visited.get(reach, 0)

            if not reach.big and any((
                (current == max_visit or (current == 1 and max_visited == max_visit)),
                (current == 1 and reach.name == 'end'),
                reach.name == 'start',
            )):
                continue

            _visited = {**visited}
            sub_paths = self.find_paths(max_visit, reach, _visited)
            for sub_path in sub_paths:
                paths.append([start] + sub_path)

        return paths

    @property
    def start(self):
        return self['start']

    def __getitem__(self, name):
        node = super().get(name)
        if not node:
            self[name] = Node(name)
        return super().get(name)


class Day12(Day):

    def parse(self, content):
        nodes = NodeList()
        for line in super().parse(content):
            nodes.add(line)

        return nodes

    def part1(self):
        return len(self.input.find_paths())

    def part2(self):
        return len(self.input.find_paths(2))

