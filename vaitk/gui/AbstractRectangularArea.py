'''

from abc import ABC, abstractmethod

from vaitk.consts import Index


class AbstractRectangularArea(ABC):
    @abstractmethod
    def rect(self):
        """
        Returns the rectangle from the top left corner to the bottom right
        corner
        """

    def size(self):
        return self.rect()[Index.RECT_WIDTH], self.rect()[Index.RECT_HEIGHT]

    def top_left(self):
        """
        Returns the coordinate of the top left corner in the relative
        coordinate system
        """
        return self.rect()[Index.RECT_X], self.rect()[Index.RECT_Y]

    def bottom_right(self):
        """
        Returns the coordinate of the bottom_right corner in the
        relative coordinate system
        """
        return self.size()

    def width(self):
        """Returns the width of the area"""
        return self.size()[Index.SIZE_WIDTH]

    def height(self):
        """Returns the height of the area"""
        return self.size()[Index.SIZE_HEIGHT]
'''
