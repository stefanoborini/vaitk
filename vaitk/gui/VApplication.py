from .. import KeyModifier, Key
from .. import FocusPolicy
from .. import core
from . import events
from .VPalette import VPalette
from .VCursesScreen import VCursesScreen
from .events import VFocusEvent
from .VGraphicElements import VGraphicElements
import threading
import queue


class _VExceptionEvent:
    def __init__(self, exception):
        self.exception = exception


class _KeyEventThread(threading.Thread):
    """
    Separate thread class to handle keyboard events
    extracted from ncurses.
    It communicates to the main thread in three ways:
    - with a queue, where it puts all the key events
    - and with an event flag, which is set when key events are available
    - with the stop_thread flag, which stops the loop

    the reason why we use the event_available_flag is because we have two
    queues, one for the key events, and the other for the other events
    (timer etc).
    We can't check the queues without altering them, so we need a flag to
    communicate
    when either of the queues has something to fetch. (to be verified, I
    remember
    I had to devise this solution due to limits of the queue object)

    Important thing (for future resolution): the stop_event is pretty useless
    since the thread stay stopped in getKeyCode and can't check the flag until
    it leaves. Either I need to add a timer, or come up with a better solution.
    In any case, the self.daemon flag should solve the problem, since the main
    thread is free to quit even if the secondary daemon thread is still
    running.
    """

    def __init__(self, screen, key_event_queue, event_available_flag):
        super().__init__()
        self.daemon = True
        self.stop_event = threading.Event()
        self.exception = None

        self._screen = screen
        self._key_event_queue = key_event_queue
        self.throttle = threading.Event()
        self._event_available_flag = event_available_flag

    def run(self):
        """
        Runs on the separate thread. Fetches key events from ncurses,
        converts them into vaitk key events, and post them into the key
        event queue for further processing from the main thread.
        """

        while not self.stop_event.is_set():
            try:
                c = self._screen.get_key_code()

                event = events.VKeyEvent.from_native_key_code(c)
                if event is not None:
                    self._key_event_queue.put(event)
                    self._event_available_flag.set()

                    self.throttle.wait()
                    self.throttle.clear()

            except Exception as e:
                event = _VExceptionEvent(e)
                self._key_event_queue.put(event)
                self._event_available_flag.set()

    def register_timer(self, timer):
        pass


class VApplication(core.VCoreApplication):
    def __init__(self, argv, screen=None):
        from . import VWidget
        super().__init__(argv)
        if screen is not None:
            self._screen = screen
        else:
            self._screen = VScreen()

        # The root widget is the one representing the whole background screen.
        # It it always rendered last.
        # This may seem weird, but we need to initialize it first to None,
        # _then_ create the root VWidget.
        # The reason is that VWidget asks for the current root widget if
        # there's no parent, and the
        # subsequent initialization results in a chicken-egg problem
        # (the root widget is the only widget
        # having strictly None as parent).
        self._root_widget = None
        self._root_widget = VWidget()

        # The widget that currently has the focus (gets key events)
        self._focus_widget = None
        self._palette = self.default_palette()

        self._event_available_flag = threading.Event()
        self._event_queue = queue.Queue()
        self._key_event_queue = queue.Queue()
        self._key_event_thread = _KeyEventThread(
            self._screen, self._key_event_queue, self._event_available_flag)

        # XXX I am not sure we need the delete later anymore.
        self._delete_later_queue = []

        # Used to terminate the exec loop
        self._exit_flag = False

        # Signals.
        self.lastWindowClosed = core.VSignal(self)
        self.focusChanged = core.VSignal(self)

        # Graphic elements contains characters to draw boxes, buttons, icons,
        # and so on.
        # We choose ascii as default because in basic ncurses implementation
        # unicode is not
        # rendered correctly. We stay conservative, and allow overriding if
        # the client code is
        # confident of the current ncurses implementation.
        self._default_graphic_elements = VGraphicElements.ASCII

    def exec_(self):
        """
        Starts the event loop.
        """
        self._root_widget.show()
        self.process_events(True)
        self._key_event_thread.start()
        while self._exit_flag is not True:
            self.logger.info("Waiting for events")
            self._event_available_flag.wait()
            self._event_available_flag.clear()
            self.logger.info("Event available")
            self.process_events(True)
            self._key_event_thread.throttle.set()

        self._exit_cleanup()

    def process_events(self, native=False):
        self.logger.info("++++---- %s processing events ---+++++" %
                         ("Native" if native else "Forced"))
        self._process_key_events()
        self._process_remaining_events()
        self._send_paint_events()
        self._delete_scheduled()
        self.logger.info("===================================")
        self._screen.refresh()

    def post_event(self, receiver, event):
        """
        Add an event to the event queue, to be delivered at a later time to
        receiver.

        Arguments:
            receiver: the intended receiver of the event
            event: a VEvent object
        """
        self.logger.info(" <posted " + str(receiver) + " " + str(event))
        self._event_queue.put((receiver, event))
        self._event_available_flag.set()

    def exit(self):
        self._exit_flag = True

    def add_top_level_widget(self, widget):
        self._root_widget.addChild(widget)

    def delete_later(self, widget):
        self.logger.info("Added widget %s to deleteLater queue" % str(widget))
        self._delete_later_queue.append(widget)

    def screen(self):
        return self._screen

    def focus_widget(self):
        return self._focus_widget

    def set_focus_widget(self, widget):
        """
        Gives focus to the specified widget.
        Focused widgets are the one that will receive Key events.

        Arguments:
            widget: the widget to set as focused
        """

        if self._focus_widget is widget:
            return

        self.logger.info("Setting focus on widget %s." % widget)

        if self._focus_widget is not None:
            self.logger.info("Focus out on widget %s." % self._focus_widget)
            VApplication.vApp.post_event(
                self._focus_widget,
                VFocusEvent(core.VEvent.EventType.FocusOut))

        self._focus_widget = None
        if widget is not None:
            if widget.focus_policy() == FocusPolicy.NoFocus:
                self.logger.info(
                    ("Focus not accepted on widget "
                     "%s due to its focus policy.") % self._focus_widget)
                return

            self._focus_widget = widget
            VApplication.vApp.post_event(
                self._focus_widget, VFocusEvent(core.VEvent.EventType.FocusIn))

    def default_palette(self):
        """
        Returns:
            the default palette of the application.
        """
        palette = VPalette()
        palette.set_defaults()
        return palette

    def palette(self):
        """
        Returns:
            the current palette of the application
        """
        return self._palette

    def default_graphic_elements(self):
        return self._default_graphic_elements

    def set_default_graphic_elements(self, graphic_elements):
        self._default_graphic_elements = graphic_elements

    def root_widget(self):
        return self._root_widget

    def reset_screen(self):
        self._screen.reset()

    def top_level_widgets(self):
        raise NotImplementedError()

    def all_widgets(self):
        raise NotImplementedError()

    def active_window(self):
        raise NotImplementedError()

    def set_active_window(self, window):
        raise NotImplementedError()

    def close_all_windows(self):
        raise NotImplementedError()

    def event(self, event):
        raise NotImplementedError()

    def clipboard(self):
        raise NotImplementedError()

    def keyboard_modifiers(self):
        raise NotImplementedError()

    def notify(self):
        raise NotImplementedError()

    def event_filter(self, event):
        """
        Default event filter that is used when no other event interceptor
        catches the event.
        By default, this event filter reacts to Ctrl+C keyevents, quitting
        the application.

        Arguments:
            event: the VEvent

        """
        if (event.key() == Key.Key_C and
                event.modifiers() & KeyModifier.ControlModifier):
            self.exit()

    # Private

    def _hide_scheduled(self):
        self.logger.info("Widget scheduled for deletion: %s" %
                         str(self._delete_later_queue))
        for w in self._delete_later_queue:
            self.logger.info(
                "Posting hide events for deleted widget %s" % str(w))
            w.hide()

    def _delete_scheduled(self):
        for w in self._delete_later_queue:
            w.parent().removeChild(w)

        self._delete_later_queue.clear()

    def _process_key_events(self):
        while True:
            self.logger.info("key queue %d" % self._key_event_queue.qsize())
            try:
                event = self._key_event_queue.get_nowait()
            except queue.Empty:
                event = None

            if event is None:
                return

            if isinstance(event, events.VKeyEvent):
                self._process_single_key_event(event)
            elif isinstance(event, _VExceptionEvent):
                raise event.exception

    def _process_single_key_event(self, key_event):
        self.logger.info("Key event %d %x" %
                         (key_event.key(), key_event.modifiers()))

        key_event.setAccepted(False)

        focus_widget = self.focus_widget()
        if focus_widget:
            for widget in focus_widget.traverse_to_root():
                self.logger.info(
                    "KeyEvent attempting delivery to "+str(widget))
                stop_event = False
                for event_filter in reversed(widget.installed_event_filters()):
                    stop_event = stop_event | event_filter.event_filter(
                        key_event)
                    if key_event.isAccepted():
                        self.logger.info(
                            "KeyEvent accepted by filter "+str(event_filter))
                        return

                if not stop_event:
                    self.logger.info(
                        "KeyEvent not stopped. Sending to widget "+str(widget))
                    widget.key_event(key_event)

                    if key_event.isAccepted():
                        self.logger.info("KeyEvent accepted by "+str(widget))
                        return

        # If all fails, deliver it to the application itself.
        self.event_filter(key_event)

    def _process_remaining_events(self):
        previous_data = None
        while True:
            try:
                receiver, event = self._event_queue.get_nowait()
            except queue.Empty:
                receiver, event = None, None

            if event is None:
                break

            if previous_data is not None:
                prev_receiver, prev_event = previous_data
                if (event.eventType() == prev_event.eventType() and
                        receiver == prev_receiver):
                    continue

            self.logger.info("Data queue %d. Processing %s -> %s." %
                             (self._event_queue.qsize(), str(event),
                              str(receiver)))
            receiver.event(event)
            previous_data = (receiver, event)

            # self._stop_flag.append(1)
        # Check if screen was re-sized (True or False)
        # x,y = self._screen.size()
        # resize = curses.is_term_resized(y, x)

        # Action in loop if resize is True:
        # if resize is True:
            # x, y = self._screen.size()
            # curses.resizeterm(y, x)
            # self.renderWidgets()

    def _send_paint_events(self):
        for w in self.root_widget().depthFirstFullTree():
            if w.needs_update():
                for w2 in w.depth_first_right_tree():
                    if core.VRect.tuple.intersects(w.absolute_rect(),
                                                   w2.absolute_rect()):
                        w2.update()

        for w in self.root_widget().depthFirstFullTree():
            if w.needs_update():
                w.event(events.VPaintEvent())

    def _exit_cleanup(self):
        self._key_event_thread.stop_event.set()
        self._screen.reset()
        super().exit()
