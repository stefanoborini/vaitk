from traitlets import HasTraits, Instance, This, List, default

import logging

from vaitk.core import TimerEvent

logger = logging.getLogger(__name__)


class BaseObject(HasTraits):
    """
    Base class for all objects in VaiTk.
    """
    parent = This(allow_none=True)
    children = List(Instance(This))

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent=parent, **kwargs)
        self.children = []
        self._event_filters = []
        if self.parent is not None:
            parent.add_child(self)

    @default('children')
    def children_default(self):
        return []

    def add_child(self, child):
        self.children.append(child)

    def remove_child(self, child):
        self.children.remove(child)

    def install_event_filter(self, event_filter):
        self._event_filters.append(event_filter)

    def event_filter(self, watched, event):
        return False

    def installed_event_filters(self):
        return self._event_filters

    def event(self, event):
        if isinstance(event, TimerEvent):
            self.timer_event(event)
            return True
        return False

    def timer_event(self, event):
        return True


# Traversal routines

def depth_first_full_tree(obj):
    return depth_first_sub_tree(root(obj))


def depth_first_sub_tree(obj):
    result = [obj]
    for c in obj.children:
        result.extend(depth_first_sub_tree(c))
    return result


def root(obj):
    return traverse_to_root(obj)[-1]


def traverse_to_root(obj):
    result = [obj]
    if obj.parent is None:
        return result
    result.extend(traverse_to_root(obj.parent))
    return result


def depth_first_right_tree(obj):
    depth_first_tree = depth_first_full_tree(obj)
    return depth_first_tree[depth_first_tree.index(obj)+1:]


def depth_first_left_tree(obj):
    depth_first_tree = depth_first_full_tree(obj)
    return depth_first_tree[:depth_first_tree.index(obj)]

