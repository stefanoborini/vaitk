from traitlets import HasTraits, Instance

from .Point import Point
from .Size import Size
#  012345678901234567890 -> x
# 0
# 1
# 2  AAAAA
# 3  AAAAA
# 4  AAAAA
# 5       BBB
# 6       BBB
# 7       BBB
# 8
#
# |
# v
#
# y
#
# A = (2,2),(5,3) topleft 2,2 bottomright 6,4


class Rect(HasTraits):
    top_left = Instance(Point)
    size = Instance(Size)

    def __init__(self, top_left, size):
        if isinstance(top_left, tuple):
            top_left = Point.from_tuple(top_left)

        if isinstance(size, tuple):
            size = Size.from_tuple(size)

        super().__init__(top_left=top_left, size=size)

    @classmethod
    def from_x_y_width_height(cls, x, y, width, height):
        top_left = Point(x, y)
        size = Size(width, height)
        return cls(top_left, size)

    @classmethod
    def from_tuple(cls, t):
        return cls.from_x_y_width_height(*t)

    @property
    def x(self):
        return self.top_left.x

    @property
    def y(self):
        return self.top_left.y

    @property
    def width(self):
        return self.size.width

    @property
    def height(self):
        return self.size.height

    @property
    def left(self):
        return self.top_left.x

    @property
    def right(self):
        return self.top_left.x + self.width - 1

    @property
    def top(self):
        return self.top_left.y

    @property
    def bottom(self):
        return self.y + self.height - 1

    @property
    def top_right(self):
        return Point(self.right, self.top)

    @property
    def bottom_left(self):
        return Point(self.left, self.bottom)

    @property
    def bottom_right(self):
        return Point(self.right, self.bottom)

    def is_null(self):
        return self.width == 0 and self.height == 0

    def move_to(self, point):
        self.top_left.x = point.x
        self.top_left.y = point.y

    def intersects(self, other):
        return (self.left <= other.right
                and self.right >= other.left
                and self.top <= other.bottom
                and self.bottom >= other.top)

    def as_tuple(self):
        return self.x, self.y, self.width, self.height

    def __str__(self):
        return (f"Rect(x={self.x}, y={self.y}, " 
                f"width={self.width}, height={self.height})")
