from traitlets import HasTraits, Int


class Size(HasTraits):
    width = Int()
    height = Int()

    def __init__(self, width, height):
        super().__init__(width=width, height=height)

    @classmethod
    def from_tuple(cls, t):
        return cls(*t)

    def __str__(self):
        return f"Size(width={self.width}, height={self.height})"

    def as_tuple(self):
        return self.width, self.height
