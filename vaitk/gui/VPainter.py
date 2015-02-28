from .. import Orientation, LineCapStyle, LineStyle, CornerCapStyle, Alignment
from .VApplication import VApplication
from ..consts import Index


class VPainter:
    """
    Class to draw text or "graphics" onto a drawable (a widget).
    """

    def __init__(self, widget):
        self._widget = widget
        colors = self._widget.currentColors()
        self._fg_color = colors[Index.FG_COLOR]
        self._bg_color = colors[Index.BG_COLOR]
        self._corner_cap_style = CornerCapStyle.Plus
        self._line_cap_style = LineCapStyle.Plus
        self._line_style = LineStyle.Full
        self._graphic_elements = VApplication.vApp.defaultGraphicElements()

    @property
    def fg_color(self):
        return self._fg_color
    @fg_color.setter
    def fg_color(self, color):
        self._fg_color = color
    @property
    def bg_color(self):
        return self._bg_color
    @bg_color.setter
    def bg_color(self, color):
        self._bg_color = color

    def drawText(self, pos_or_rect, string, align=0):
        """
        Writes text at a specified position. The behavior of this function depends on the
        pos_or_rect argument.
        """
        if len(pos_or_rect) == 2:
            self._widget.screenArea().write(pos_or_rect, string, self.fg_color, self.bg_color)
            return

        if align & (Alignment.AlignTop | Alignment.AlignVCenter | Alignment.AlignBottom) == 0:
            align |= Alignment.AlignTop

        if align & (Alignment.AlignLeft | Alignment.AlignHCenter | Alignment.AlignRight) == 0:
            align |= Alignment.AlignLeft

        rect = pos_or_rect

        if align & Alignment.AlignLeft:
            line_formatted = string.ljust(rect[Index.RECT_WIDTH])
        elif align & Alignment.AlignRight:
            line_formatted = string.rjust(rect[Index.RECT_WIDTH])
        elif align & Alignment.AlignHCenter:
            line_formatted = string.center(rect[Index.RECT_WIDTH])
        else:
            line_formatted = string.ljust(rect[Index.RECT_WIDTH])

        for h in range(rect[Index.RECT_HEIGHT]):
            if (align & Alignment.AlignTop and h == 0) or \
               (align & Alignment.AlignVCenter and h == int(rect[Index.RECT_HEIGHT]/2)) or\
               (align & Alignment.AlignBottom and h == rect[Index.RECT_HEIGHT]-1):

                self._widget.screenArea().write( (rect[Index.RECT_X], rect[Index.RECT_Y]+h),
                                                      line_formatted,
                                                      self.fg_color,
                                                      self.bg_color)

            else:
                self._widget.screenArea().write( (rect[Index.RECT_X], rect[Index.RECT_Y]+h),
                                                  ' '*rect[Index.RECT_WIDTH],
                                                  self.fg_color,
                                                  self.bg_color)

    def drawRect(self, rect):
        """
        Draws a rectangle with geometry as specified in the rect parameter.
        The internal part of the rectangle will not be drawn. If you want a filled
        rectangle, use fillRect()

        Arguments:
            rect: a 4-tuple containing (x,y,width,height) of the rectangle.
        """
        screen_area = self._widget.screenArea()

        x, y = rect[Index.RECT_X], rect[Index.RECT_Y]
        w, h = rect[Index.RECT_WIDTH], rect[Index.RECT_HEIGHT]
        fg, bg = self.fg_color, self.bg_color
        top_left_corner = self._graphic_elements["BOX DRAWINGS LIGHT DOWN AND RIGHT"]
        top_border = self._graphic_elements["BOX DRAWINGS LIGHT HORIZONTAL"]
        top_right_corner = self._graphic_elements["BOX DRAWINGS LIGHT DOWN AND LEFT"]
        right_border = self._graphic_elements["BOX DRAWINGS LIGHT VERTICAL"]
        bottom_right_corner = self._graphic_elements["BOX DRAWINGS LIGHT UP AND LEFT"]
        bottom_border = self._graphic_elements["BOX DRAWINGS LIGHT HORIZONTAL"]
        bottom_left_corner = self._graphic_elements["BOX DRAWINGS LIGHT UP AND RIGHT"]
        left_border = self._graphic_elements["BOX DRAWINGS LIGHT VERTICAL"]

        if w >= 2 and h >= 2:
            screen_area.write( (x,y), top_left_corner + top_border * (w-2) + top_right_corner, fg, bg)
            for i in range(0, h-2):
                screen_area.write( (x,y+i+1), left_border, fg, bg)
                screen_area.write( (x+w-1, y+i+1), right_border, fg, bg)
            screen_area.write( (x, y+h-1), bottom_left_corner + bottom_border*(w-2) + bottom_right_corner, fg, bg)

    def fillRect(self, rect):
        """
        Draws a filled rectangle with geometry as specified in the rect parameter.
        The internal part of the rectangle will be drawn as empty spaces.
        If you want a non-filled rectangle, use drawRect()

        Arguments:
            rect: a 4-tuple containing (x,y,width,height) of the rectangle.
        """
        screen_area = self._widget.screenArea()

        x, y = rect[Index.RECT_X], rect[Index.RECT_Y]
        w, h = rect[Index.RECT_WIDTH], rect[Index.RECT_HEIGHT]
        fg, bg = self.fg_color, self.bg_color
        top_left_corner = self._graphic_elements["BOX DRAWINGS LIGHT DOWN AND RIGHT"]
        top_border = self._graphic_elements["BOX DRAWINGS LIGHT HORIZONTAL"]
        top_right_corner = self._graphic_elements["BOX DRAWINGS LIGHT DOWN AND LEFT"]
        right_border = self._graphic_elements["BOX DRAWINGS LIGHT VERTICAL"]
        bottom_right_corner = self._graphic_elements["BOX DRAWINGS LIGHT UP AND LEFT"]
        bottom_border = self._graphic_elements["BOX DRAWINGS LIGHT HORIZONTAL"]
        bottom_left_corner = self._graphic_elements["BOX DRAWINGS LIGHT UP AND RIGHT"]
        left_border = self._graphic_elements["BOX DRAWINGS LIGHT VERTICAL"]

        if w >= 2 and h >= 2:
            screen_area.write( (x,y), top_left_corner + top_border * (w-2) + top_right_corner, fg, bg)
            for i in range(0, h-2):
                screen_area.write( (x,y+i+1), left_border + ' '*(w-2) + right_border, fg, bg)
            screen_area.write( (x, y+h-1), bottom_left_corner + bottom_border*(w-2) + bottom_right_corner, fg, bg)

    def drawLine(self, pos, length, direction):
        """
        Draws a line starting from a given pos and length, either horizontal or vertical.
        The line is always drawn left to right (Horizontal) or top to bottom (Vertical)

        Arguments:
            pos: 2-tuple containing (x,y) of the starting position.
            length: integer containing the length of the line
            direction: either Orientation.Horizontal or Orientation.Vertical
        """
        screen_area = self._widget.screenArea()
        x,y = pos
        fg, bg = self.fg_color, self.bg_color
        h_line = self._graphic_elements["BOX DRAWINGS LIGHT HORIZONTAL"]
        v_line = self._graphic_elements["BOX DRAWINGS LIGHT VERTICAL"]

        if direction == Orientation.Horizontal:
            screen_area.write( (x,y), h_line * length, fg, bg)
        elif direction == Orientation.Vertical:
            for i in range(0, length):
                screen_area.write( (x,y+i), v_line, fg, bg)

    def eraseRect(self, rect):
        """
        Deletes the contents of a given rect area

        Arguments:
            rect: a 4-tuple containing (x,y,width,height) of the rectangle to delete.
        """
        widget_colors = self._widget.currentColors()
        screen_area = self._widget.screenArea()
        top_left = (rect[Index.RECT_X], rect[Index.RECT_Y])
        string = ' '*rect[Index.RECT_WIDTH]
        for h_idx in range(rect[Index.RECT_HEIGHT]):
            screen_area.write( (top_left[Index.X], top_left[Index.Y] + h_idx),
                               string,
                               widget_colors[Index.FG_COLOR], widget_colors[Index.BG_COLOR])

    def erase(self):
        """
        Deletes the contents of the full area associated to the VPainter.
        """
        self.eraseRect(self._widget.rect())

    def recolor(self, pos, colors):
        """
        Modifies the color of a given position in the drawable area.
        """
        self._widget.screenArea().setColors(pos, colors)


