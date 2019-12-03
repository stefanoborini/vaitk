import logging

from .. import core
from ..consts import Index
from .. import FocusPolicy
from .Application import Application
from .Palette import Palette
from .Painter import Painter
from vaitk.gui import ScreenArea
from . import events


logger = logging.getLogger(__name__)


class Widget(core.BaseObject):
    def __init__(self, parent=None):
        if parent is None:
            parent = Application.vApp.root_widget()

        super().__init__(parent)

        if self.parent() is None:
            self._geometry = (0, 0) + Application.vApp.screen().size()
        else:
            self._geometry = self.parent().contents_rect()

        self._layout = None
        self._visible_implicit = False
        self._visible_explicit = None
        self._palette = None
        self._enabled = True
        self._active = True
        self._focus_policy = FocusPolicy.NoFocus
        self._needs_update = False
        self._minimum_size = (0, 0)

        # True for dialogs and other widgets that hover, grabbing the focus
        self._is_window = False

    def set_focus(self, reason=None):
        """
        Gives focus to this widget.
        Arguments:
            reason: The reason behind the focus change
        """
        Application.vApp.set_focus_widget(self)

    def has_focus(self):
        """
        Returns:
            True if the widget has focus, otherwise False
        """
        return (self is Application.vApp.focus_widget())

    # State change
    def move(self, pos):
        """
        Sets the size to the specified amount.
        Generates an immediate VMoveEvent if the widget is visible.
        If not visible, the widget will receive it as soon as made visible

        Arguments:
            size: a 2-tuple (x, y)
        """
        if not isinstance(pos, tuple) or len(pos) != 2:
            raise TypeError("Invalid pos argument")

        self.set_geometry(pos + self.size())

    def resize(self, size):
        """
        Sets the size to the specified amount.
        Generates an immediate VResizeEvent if the widget is visible.
        If not visible, the widget will receive it as soon as made visible

        Arguments:
            size: a 2-tuple (width, height)
        """

        if not isinstance(size, tuple) or len(size) != 2:
            raise TypeError("Invalid size argument")

        self.set_geometry(self.pos() + size)

    def set_geometry(self, rect):
        old_geometry = self._geometry

        min_size = self.minimum_size()
        self._geometry = (rect[Index.RECT_X],
                          rect[Index.RECT_Y],
                          max(min_size[Index.SIZE_WIDTH],
                              rect[Index.RECT_WIDTH]),
                          max(min_size[Index.SIZE_HEIGHT],
                              rect[Index.RECT_HEIGHT])
                          )

        if self.is_visible():
            deliver_routine = Application.vApp.sendEvent
        else:
            deliver_routine = Application.vApp.post_event

        if (old_geometry[Index.RECT_X], old_geometry[Index.RECT_Y])  \
                != (self._geometry[Index.RECT_X],
                    self._geometry[Index.RECT_Y]):

            deliver_routine(self, events.MoveEvent())

        if (old_geometry[Index.RECT_WIDTH], old_geometry[Index.RECT_WIDTH]) \
                != (self._geometry[Index.RECT_HEIGHT],
                    self._geometry[Index.RECT_HEIGHT]):

            deliver_routine(self, events.ResizeEvent())

    def show(self):
        """
        Makes the widget visible. Equivalent to self.setVisible(True)
        """
        self.set_visible(True)

    def hide(self):
        """
        Makes the widget hidden. Equivalent to self.setVisible(False)
        """
        self.set_visible(False)

    def lower(self):
        pass

    def raise_(self):
        pass

    def close(self):
        pass

    def set_visible(self, visible):
        """
        Changes the visibility of the widget. If setVisible(True) is called
        on a visible widget, nothing
        happens. The same for the hidden case.
        A ShowEvent (HideEvent) is sent before (resp. after) the visibility
        change is performed on screen.

        Arguments:
            visible: True to set the widget to visible. False to hide it.

        """
        logger.info(
            "Setting explicit visibility for %s : %s",
            str(self),
            str(visible))
        visible_before = self.is_visible()
        self._visible_explicit = visible

        if visible and not visible_before:
            Application.vApp.post_event(self, events.ShowEvent())
        elif not visible and visible_before:
            Application.vApp.post_event(self, events.HideEvent())

        for w in self.children():
            w.set_visible_implicit(visible)

    def set_visible_implicit(self, visible):
        # XXX private?
        logger.info(
            "Setting implicit visibility for %s : %s",
            str(self), str(visible))
        self._visible_implicit = visible

        if visible:
            Application.vApp.post_event(self, events.ShowEvent())
        else:
            Application.vApp.post_event(self, events.HideEvent())

        for w in self.children():
            w.set_visible_implicit(visible)

    # Query methods
    def size(self):
        """
        Returns:
            the widget current size as a 2-tuple (width, height)
        """
        return (self.geometry()[Index.RECT_WIDTH],
                self.geometry()[Index.RECT_HEIGHT])

    def rect(self):
        """
        Returns:
            The widget current rect as a 4-tuple (0, 0, width, height).
        """
        return (0, 0)+self.size()

    def absolute_rect(self):
        return self.map_to_global((0, 0)) + self.size()

    def geometry(self):
        """
        Returns the geometry of the widget.

        Returns:
            A 4-tuple with (x, y, width, height)
        """
        return self._geometry

    def width(self):
        """
        Returns the width of the widget.

        Returns:
            integer
        """
        return self.geometry()[Index.RECT_WIDTH]

    def height(self):
        """
        Returns the height of the widget.

        Returns:
            integer
        """
        return self.geometry()[Index.RECT_HEIGHT]

    def pos(self):
        """
        Returns the position of the widget within its parent.

        Returns:
            A 2-tuple of integers
        """
        geometry = self.geometry()
        return (geometry[Index.RECT_X], geometry[Index.RECT_Y])

    def x(self):
        """
        Returns the x position of the widget within its parent.

        Returns:
            integer
        """
        geometry = self.geometry()
        return geometry[Index.RECT_X]

    def y(self):
        """
        Returns the y position of the widget within its parent.

        Returns:
            integer
        """
        geometry = self.geometry()
        return geometry[Index.RECT_Y]

    def is_visible(self):
        """
        Returns:
            True if the widget is visible. False if hidden.
            Note that a widget is considered visible even if fully covered by
            an overlapping widget.
        """
        return (self._visible_explicit if self._visible_explicit is not None
                else self._visible_implicit)

    def is_visible_to(self, ancestor):
        pass

    def minimum_size(self):
        """
        Returns:
            a 2-tuple (width, height) with the minimum allowed size of the
            widget
        """
        return self._minimum_size

    def add_layout(self, layout):
        self._layout = layout
        self._layout.set_parent(self)

    def map_to_global(self, pos):
        """
        Given a position pos in coordinates relative to this widget, return
        the coordinate
        in absolute screen coordinates.

        Arguments:
            pos: 2-tuple (x,y)

        Returns:
            a 2-tuple (x,y) with the absolute coordinates
        """
        top_left = self.pos()
        if self.parent() is None:
            return (pos[Index.X]+top_left[Index.X],
                    pos[Index.Y]+top_left[Index.Y])

        parent_corner = self.parent().map_to_global((0, 0))
        return (parent_corner[Index.X] + top_left[Index.X] + pos[Index.X],
                parent_corner[Index.Y] + top_left[Index.Y] + pos[Index.Y]
                )

    def screen_area(self):
        abs_pos_topleft = self.map_to_global((0, 0))

        return ScreenArea(Application.vApp.screen(),
                          abs_pos_topleft + self.size()
                          )
    # Events

    def event(self, event):
        """
        Generic event method. Gets called for all events, and dispatches to a
        more specific event handler.

        Arguments:
            event: the event.
        """

        logger.info(
            "Event %s. Receiver %s",
            str(event),
            str(self))

        if isinstance(event, events.PaintEvent):
            if not self.is_visible():
                return True
            self.paint_event(event)
            self._needs_update = False

        elif isinstance(event, events.FocusEvent):
            if self.is_visible():
                if event.eventType() == core.Event.EventType.FocusIn:
                    self.focus_in_event(event)
            else:
                if event.eventType() == core.Event.EventType.FocusOut:
                    self.focus_out_event(event)

            self.update()

        elif isinstance(event, events.HideEvent):
            self.hide_event(event)

            for w in self.depthFirstFullTree():
                logger.info("Widget %s in tree", str(w))
                if not w.is_visible():
                    continue
                logger.info("Repainting widget %s", str(w))
                w.update()

        elif isinstance(event, events.ShowEvent):
            self.show_event(event)

            for w in self.depthFirstFullTree():
                logger.info("Widget %s in tree", str(w))
                if not w.is_visible():
                    continue
                w.update()

        elif isinstance(event, events.MoveEvent):
            if not self.is_visible():
                return True

            self.move_event(event)

            for w in self.depthFirstFullTree():
                logger.info("Widget %s in tree", str(w))
                if not w.is_visible():
                    continue
                w.update()

        elif isinstance(event, events.ResizeEvent):
            if not self.is_visible():
                return True

            self.resize_event(event)

            for w in self.depthFirstFullTree():
                logger.info("Widget %s in tree", str(w))
                if not w.is_visible():
                    continue
                w.update()
        else:
            return super().event(event)

        return True

    def key_event(self, event):
        """
        Handle VKeyEvents.
        """
        pass

    def paint_event(self, event):
        painter = Painter(self)
        # if self._layout is not None:
        #    self._layout.apply()

        size = self.size()

        string = ' '*size[Index.SIZE_WIDTH]
        for i in range(0, size[Index.SIZE_HEIGHT]):
            painter.draw_text((0, i), string)

    def focus_in_event(self, event):
        logger.info("FocusIn event")

    def focus_out_event(self, event):
        logger.info("FocusOut event")

    def hide_event(self, event):
        logger.info("Hide event")

    def move_event(self, event):
        logger.info("Move event")

    def show_event(self, event):
        logger.info("Show event")

    def resize_event(self, event):
        logger.info("Resize event")

    def set_focus_policy(self, policy):
        self._focus_policy = policy

    def focus_policy(self):
        return self._focus_policy

    def needs_update(self):
        return self._needs_update

    def is_enabled(self):
        """
        Returns:
            True if the widget is enabled. False otherwise.
        """
        # XXX Check if an enabled widget is not sent focus events, and how
        # focus is reassigned when a widget is made enabled False
        return self._enabled

    def is_enabled_to(self, ancestor):
        pass

    def is_active(self):
        return self._active

    def set_active(self, active):
        self._active = active

    def set_enabled(self, enabled):
        """
        Enables or disables a widget.

        Arguments:
            enabled: True to enable the widget. False to disable.
        """
        self._enabled = enabled

    def palette(self):
        """
        Returns:
            the widget palette. If no palette has been set, a copy of the
            application palette will be installed the first time this method is
            called, and then returned.
        """
        if self._palette is None:
            self._palette = Application.vApp.palette().copy()

        return self._palette

    def set_colors(self, fg=None, bg=None):
        self.palette().set_color(Palette.ColorGroup.Active,
                                 Palette.ColorRole.WindowText, fg)
        self.palette().set_color(Palette.ColorGroup.Active,
                                 Palette.ColorRole.Window, bg)

    def colors(self, color_group=Palette.ColorGroup.Active):
        fg = self.palette().color(color_group, Palette.ColorRole.WindowText)
        bg = self.palette().color(color_group, Palette.ColorRole.Window)

        return (fg, bg)

    def current_colors(self):
        if self.is_active():
            color_group = Palette.ColorGroup.Active
        else:
            if self.is_enabled(self):
                color_group = Palette.ColorGroup.Inactive
            else:
                color_group = Palette.ColorGroup.Disabled
        return self.colors(color_group)

    def background_role(self):
        pass

    def foreground_role(self):
        pass

    def set_foreground_role(self, role):
        pass

    def set_background_role(self, role):
        pass

    def update(self):
        self._needs_update = True

    # Sizes

    def contents_rect(self):
        # XXX Check because I think we also have to subtract border and padding
        margins = self.contents_margins()
        return (margins[Index.MARGIN_LEFT],
                margins[Index.MARGIN_TOP],
                self.width()-margins[Index.MARGIN_LEFT] -
                margins[Index.MARGIN_RIGHT],
                self.height()-margins[Index.MARGIN_TOP] -
                margins[Index.MARGIN_BOTTOM]
                )

    def contents_margins(self):
        # XXX not sure about the definition of margins for qt
        return (0, 0, 0, 0)

    def children_rect(self):
        pass

    def frame_geometry(self):
        pass

    def normal_geometry(self):
        pass

    def base_size(self):
        pass

    def frame_size(self):
        pass

    def maximum_size(self):
        pass

    def maximum_width(self):
        pass

    def maximum_height(self):
        pass

    def minimum_height(self):
        pass

    def minimum_width(self):
        pass

    def minimum_size_hint(self):
        pass

    def size_hint(self):
        pass

    def height_for_width(self):
        pass

    def set_base_size(self, size):
        pass

    def set_contents_margins(self, margins):
        pass

    def set_maximum_height(self, maxh):
        pass

    def set_maximum_size(self, max_size):
        pass

    def set_maximum_width(self, maxw):
        pass

    def set_minimum_height(self, minh):
        self._minimum_size = (self._minimum_size[Index.SIZE_WIDTH], minh)

    def set_minimum_width(self, minw):
        self._minimum_size = (minw, self._minimum_size[Index.SIZE_HEIGHT])

    def set_minimum_size(self, min_size):
        self._minimum_size = min_size

    def set_fixed_height(self, height):
        pass

    def set_fixed_width(self, width):
        pass

    def set_fixed_size(self, size):
        pass

    def font_info(self):
        pass
