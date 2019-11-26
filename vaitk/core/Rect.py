from traitlets import HasTraits, Instance

from .Point import Point
from .Size import Size


class Rect(HasTraits):
    """
    Describes a rectangle in the screen coordinate system.
    The rectangle is defined by its top left corner (a Point) and
    its size (a Size), according to the following example

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

    rectangle A has top_left at (2, 2), and size (5,3). Its bottom right corner
    is therefore at (6, 4).
    """
    top_left = Instance(Point)
    size = Instance(Size)

    def __init__(self, top_left, size):
        """
        Constructor.

        Args:
            top_left: Point or tuple
                The top left coordinate of the rectangle
            size: Size or tuple
                The size of the rectangle
        """
        if isinstance(top_left, tuple):
            top_left = Point.from_tuple(top_left)

        if isinstance(size, tuple):
            size = Size.from_tuple(size)

        super().__init__(top_left=top_left, size=size)

    @classmethod
    def from_x_y_width_height(cls, x, y, width, height):
        """
        Alternate constructor: creates the Rect from x y coordinates of
        the top left corner, and from width and height of the rectangle.

        Args:
            x: int
                The x coordinate of the top left corner
            y: int
                The y coordinate of the top left corner
            width: int
                The width of the rectangle
            height: int
                The height of the rectangle

        Returns: Rect
        """
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
        """
        Check if the Rect is null, defined as being true when
        it has both width and height equal to zero. Note that
        an empty Rect is not necessarily null.

        Returns: bool
            True if width and height are zero, False otherwise
        """
        return self.width == 0 and self.height == 0

    def move_to(self, point):
        """
        Moves the rect to a different top left corner. Does not change
        the size.

        Args:
            point: Point
                The new top left corner

        Returns: None

        """
        self.top_left.x = point.x
        self.top_left.y = point.y

    def intersects(self, other):
        """
        Checks if a rect "other" intersects (has overlap) with this Rect.

        Args:
            other: Rect
                The other rect

        Returns: bool
            True if there's an intersection area. False otherwise

        """
        return (self.left <= other.right
                and self.right >= other.left
                and self.top <= other.bottom
                and self.bottom >= other.top)

    def as_tuple(self):
        """
        Returns: tuple
            A 4-tuple (x, y, width, height)

        """
        return self.x, self.y, self.width, self.height

    def __str__(self):
        return (f"Rect(x={self.x}, y={self.y}, " 
                f"width={self.width}, height={self.height})")
