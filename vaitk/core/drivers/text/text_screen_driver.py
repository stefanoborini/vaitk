import logging
import itertools
from queue import Queue

from vaitk.core import Size
from vaitk.core.events.key_event import KeyEvent
from vaitk.core.point import Point
from vaitk.core.drivers.abc.abc_driver import ABCDriver


logger = logging.getLogger(__file__)


class TextScreenDriver(ABCDriver):
    """
    Dummy Screen that renders information in an indexed buffer, instead of
    the actual terminal screen.
    """

    def __init__(self, size):
        """
        Creates a driver for a text based screen with a given size

        Args:
            size: Size
                The size of the screen.
        """
        if isinstance(size, Size):
            self._size = size
        else:
            self._size = Size(size[0], size[1])

        self._cursor_pos = Point(0, 0)
        self._render_output = []
        self._queue = Queue()
        self.erase()

    def init(self):
        """
        Initializes the driver

        Returns: None

        """
        self.erase()

    def deinit(self):
        """
        Deinitialises the driver.

        Returns: None

        """

    @property
    def num_nominal_colors(self):
        return 1

    @property
    def num_representable_colors(self):
        return 1

    @property
    def cursor_pos(self):
        return self._cursor_pos

    @cursor_pos.setter
    def cursor_pos(self, pos):
        self._cursor_pos = pos

    @property
    def size(self):
        return self._size

    def reset(self):
        self.erase()

    def write(self, pos, string, fg_color=None, bg_color=None):
        """
        Writes a string at a given position with given colors.

        Args:
            pos: Point
                Where in the screen the string should be written,
                top left corner.
            string: str
                String to write
            fg_color: Color or None
                The foreground color
            bg_color: Color or None
                The background color.

        Returns: None
        """
        for pos_x in range(len(string)):
            try:
                self._render_output[pos.y][pos.x+pos_x] = string[pos_x]
            except IndexError:
                logger.warning("Invalid write position : ", str(pos), string)

    def get_event(self):
        """
        Gets an event from the driver.

        Returns: Event

        """
        data = self._queue.get()
        return data

    def type_string(self, string):
        """
        Types the given string in the event buffer as a list of individual
        characters.

        Args:
            string: str
                the string to type

        Returns: None

        """
        for char in string:
            self._queue.put(KeyEvent(char))

    def dump(self):
        """
        Returns the content of the screen as a list of rows. Each row is a
        list of characters.

        Returns: list
        """
        ret = list()
        ret.append(" "+"".join(list(itertools.islice(itertools.cycle(
            list(map(str, list(range(10))))), self._size.width+1))))
        for i, r in enumerate(self._render_output):
            ret.append(str(i % 10)+''.join(r)+"+")
        ret.append("+"*(self._size.width+2))
        return ret

    def __str__(self):
        """
        method for str() resolution.

        Returns: str

        """
        return "\n" + "\n".join(self.dump())

    def char_at(self, pos):
        """
        Returns the character at the given position.
        Args:
            pos: Point
                The position

        Returns: a single character

        """
        return self._render_output[pos.y][pos.x]

    def string_at(self, pos, length):
        """
        Returns the content at position pos of given length.

        Args:
            pos: Point
                the position on the screen
            length: int
                the amount of chars to return

        Returns: the string at the given position
        """
        return ''.join(self._render_output[pos.y][pos.x:pos.x + length])

    def erase(self):
        """
        Clears the whole area
        """
        self._render_output.clear()
        for h in range(self.size.height):
            row = []
            self._render_output.append(row)
            for w in range(self.size.width):
                row.append(' ')
