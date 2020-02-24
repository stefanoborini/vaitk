from traitlets import HasTraits, Int


class Point(HasTraits):
    """
    Defines a point on the x, y screen.
    The coordinate system is meant to be:
    - x horizontally with zero at the top left, growing from left to right
    - y vertically with zero at the top left, growing from top to bottom

    They are therefore screen x y, not cartesian ones.
    """
    x = Int()
    y = Int()

    def __init__(self, x, y):
        super().__init__(x=x, y=y)

    def __add__(self, other):
        """
        Adds this point to another point "other".
        x and y coordinates are added.
        Returns a new point
        """
        return Point(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other):
        """
        Subtracts this point to another point "other".
        x and y coordinates are subtracted. Returns a new point
        """
        return Point(x=self.x - other.x, y=self.y - other.y)

    def __str__(self):
        return f"{self.__class__.__name__}(x={self.x}, y={self.y})"
