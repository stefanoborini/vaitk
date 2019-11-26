from traitlets import HasTraits, Int


class Point(HasTraits):
    x = Int()
    y = Int()

    def __init__(self, x, y):
        super().__init__(x=x, y=y)

    @classmethod
    def from_tuple(cls, t):
        return cls(*t)

    def __add__(self, other):
        return Point(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other):
        return Point(x=self.x - other.x, y=self.y - other.y)

    def __str__(self):
        return f"{self.__class__.__name__}(x={self.x}, y={self.y})"

    def as_tuple(self):
        return self.x, self.y
