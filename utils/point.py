class Point:
    def __init__(self, x, y, name=None):
        self.x = int(x)
        self.y = int(y)
        self.name = name

    def dist(self, other):
        # manhattan distance
        return abs(self.x - other.x) + abs(self.y - other.y)

    def eq(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        name = f'({self.name})' if self.name else ''
        return f'{self.__class__.__name__}[{self.x},{self.y}]{name}'


class UniquePoint(Point):
    def __eq__(self, other):
        return self.eq(other)

    def __hash__(self):
        return hash((self.x, self.y))
