from . import TimerEvent
import logging


class BaseObject:
    """
    Base class for all objects in VaiTk.
    Provides methods for the object hierarchy traversal.

    A derived class can set the class variable debug to True to enable
    debugging at the DEBUG level for that specific class.

    Example:
    class Foo(VObject):
        debug = True

    The class can also specify the specific logging level
    class Foo(VObject):
        debug = True
        debug_level = logging.INFO

    An instance of VObject will always have a logger in self.logger
    """

    def __new__(cls, *args, **kwargs):
        instance = object.__new__(cls)
        instance.logger = logging.getLogger(cls.__name__)
        if hasattr(cls, "debug"):
            if hasattr(cls, "debug_level"):
                level = cls.debug_level
            else:
                level = logging.DEBUG
            instance.logger.setLevel(level)
            instance.logger.log(
                level, "Debugging enabled for "+str(cls.__name__))
        else:
            instance.logger.setLevel(logging.CRITICAL+1)

        return instance

    def __init__(self, parent=None):
        self._parent = parent
        self._children = []
        self._event_filters = []
        if self._parent is not None:
            parent.add_child(self)

    def parent(self):
        return self._parent

    def children(self):
        return self._children

    def add_child(self, child):
        self._children.append(child)

    def remove_child(self, child):
        self._children.remove(child)

    def depth_first_full_tree(self):
        return self.root().depth_first_sub_tree()

    def depth_first_sub_tree(self):
        result = [self]
        for c in self.children():
            result.extend(c.depth_first_sub_tree())
        return result

    def root(self):
        return self.traverse_to_root()[-1]

    def traverse_to_root(self):
        result = [self]
        if self.parent() is None:
            return result
        result.extend(self.parent().traverse_to_root())
        return result

    def depth_first_right_tree(self):
        depth_first_tree = self.depth_first_full_tree()
        return depth_first_tree[depth_first_tree.index(self)+1:]

    def depth_first_left_tree(self):
        depth_first_tree = self.depth_first_full_tree()
        return depth_first_tree[:depth_first_tree.index(self)]

    def install_event_filter(self, event_filter):
        self._event_filters.append(event_filter)

    def event_filter(self, watched, event):
        return False

    def installed_event_filters(self):
        return self._event_filters

    def event(self, event):
        if isinstance(event, TimerEvent.VTimerEvent):
            self.timer_event(event)
            return True
        return False

    def timer_event(self, event):
        return True

    def __str__(self):
        return self.__class__.__name__