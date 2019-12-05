from traitlets import HasTraits, Int


class Size(HasTraits):
    """
    Describes a Size in terms of width and height
    """
    width = Int()
    height = Int()

    def __init__(self, width, height):
        """
        Creates a size from width and height
        Args:
            width: int
                The width
            height: int
                The height
        """
        super().__init__(width=width, height=height)

    def __str__(self):
        return f"Size(width={self.width}, height={self.height})"
