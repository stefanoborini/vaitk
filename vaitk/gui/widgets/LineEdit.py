from vaitk.gui import Cursor
from vaitk.gui.enums import FocusPolicy
from vaitk.keys import Key
from vaitk import core
from vaitk.consts import Index
from vaitk.gui.Widget import Widget
from vaitk.gui.Painter import Painter


class LineEdit(Widget):
    def __init__(self, contents="", parent=None):
        super().__init__(parent)
        self._text = contents
        self._cursor_position = len(self._text)
        self._selection = None
        self._max_length = 32767
        self.set_focus_policy(FocusPolicy.StrongFocus)

        self.returnPressed = core.Signal(self)
        self.cursorPositionChanged = core.Signal(self)
        self.textChanged = core.Signal(self)
        self.selectionChanged = core.Signal(self)
        self.editingFinished = core.Signal(self)

    def max_length(self):
        return self._max_length

    def set_max_length(self, max_length):
        self._max_length = max_length
        self._text = self._text[:self._max_length]
        self.deselect()

    def cursor_position(self):
        return self._cursor_position

    def set_cursor_position(self, position):
        old_pos = self._cursor_position
        self._cursor_position = position
        self.cursorPositionChanged.emit(old_pos, position)

    def set_selection(self, start, length):
        if len(self._text) == 0:
            return
        self._selection = (0, len(self._text))
        self.selectionChanged.emit()

    def select_all(self):
        if len(self._text) == 0:
            return
        self._selection = (0, len(self._text))
        self.selectionChanged.emit()

    def selection_start(self):
        pass

    def selection_end(self):
        pass

    def size_hint(self):
        pass

    def deselect(self):
        self._selection = None
        self.selectionChanged.emit()

    def home(self):
        old_pos = self._cursor_position
        self._cursor_position = 0
        self.cursorPositionChanged.emit(old_pos, self._cursor_position)

    def end(self):
        old_pos = self._cursor_position
        self._cursor_position = len(self._text)
        self.cursorPositionChanged.emit(old_pos, self._cursor_position)

    def text(self):
        return self._text

    def set_text(self, text):
        self.deselect()
        if text != self._text:
            self._text = text
            self.textChanged.emit(self._text)
            self.update()

    def backspace(self):
        if self._selection:
            pass
        else:
            pass

    def clear(self):
        self.set_text("")
        self._cursor_position = 0

    def cursor_forward(self, mark):
        pass

    def cursor_backward(self, mark):
        pass

    def cursor_word_forward(self, mark):
        pass

    def cursor_word_backward(self, mark):
        pass

    def minimum_size_hint(self):
        return core.Size(len(self._text), 1)

    def paint_event(self, event):
        w, h = self.size()
        painter = Painter(self)
        painter.draw_text((0, 0), self._text + ' ' * (w - len(self._text)))
        if self.has_focus():
            abs_top_left = self.map_to_global((0, 0))
            Cursor.set_pos((abs_top_left[Index.X] + self._cursor_position,
                            abs_top_left[Index.Y]
                            )
                           )

    def focus_in_event(self, event):
        abs_top_left = self.map_to_global((0, 0))
        Cursor.set_pos((abs_top_left[Index.X] + self._cursor_position,
                        abs_top_left[Index.Y]
                        )
                       )

    def key_event(self, event):
        if event.key() == Key.Key_Return:
            self.returnPressed.emit()
        elif event.key() == Key.Key_Left:
            self._cursor_position = max(0, self._cursor_position-1)
        elif event.key() == Key.Key_Right:
            self._cursor_position = min(
                len(self._text), self._cursor_position+1)
        elif event.key() == Key.Key_Backspace:
            if self._cursor_position == 0:
                event.accept()
                return
            self._cursor_position -= 1
            self._text = self._text[:self._cursor_position] + \
                self._text[self._cursor_position+1:]
        else:
            self._text = self._text[:self._cursor_position] + \
                event.text() + self._text[self._cursor_position:]
            self._cursor_position += len(event.text())
        event.accept()
        self.update()

    def minimum_size(self):
        return (len(self._text), 1)

    def selected_text(self):
        pass
