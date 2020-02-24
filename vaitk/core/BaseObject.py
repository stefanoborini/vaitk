from traitlets import HasTraits, Instance, This, List, default

import logging

from vaitk.core.timer_event import TimerEvent

logger = logging.getLogger(__name__)


class BaseObject(HasTraits):
    """
    Base class for all objects in VaiTk.
    """

    # The parent of this object
    parent = This(allow_none=True)

    # The list of its children
    children = List(Instance(This))

    # The list of installed event filters.
    event_filters = List(Instance(This))

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent=parent, **kwargs)
        self._event_filters = []
        if self.parent is not None:
            parent.add_child(self)

    @default('children')
    def children_default(self):
        return []

    def add_child(self, child):
        """
        Adds a child to the list of children of this object.
        If the child is already in the list, do nothing.
        You don't need to call this method explicitly, as the
        hierarchy is set up by the parent relationship.

        Args:
            child: BaseObject
                the child to add

        Returns: None

        """
        if child not in self.children:
            self.children.append(child)

    def remove_child(self, child):
        """
        Removes a previously added child to the list of children.
        You don't need to call this method explicitly, as the
        hierarchy is set up by the parent relationship.

        Args:
            child:

        Returns: None

        Raises:
            ValueError: if the child is not present

        """
        self.children.remove(child)

    def install_event_filter(self, event_filter):
        """
        Installs an event filter.
        If the event filter is already present, do nothing.

        Args:
            event_filter: BaseObject
                The object that will receive notifications.

        Returns: None

        """
        if event_filter not in self.event_filters:
            self.event_filters.append(event_filter)

    def event_filter(self, watched, event):
        """
        Method that is called when this object has been registered
        as an event filter.

        By default, the implementation does nothing. Classes that want
        to act must reimplement this method

        Args:
            watched: BaseObject
                The original object that received the event
            event: Event
                The event that is being dispatched.

        Returns: bool
            True if the event has been handled. False otherwise.

        """
        return False

    def event(self, event):
        """
        Receives a dispatched event.

        Args:
            event: Event
                The event that is being dispatched

        Returns: bool
            True if the event was recognised and handled. False otherwise.
        """
        if isinstance(event, TimerEvent):
            self.timer_event(event)
            return True
        return False

    def timer_event(self, event):
        """
        Event handler for timer events. The timer event is dispatched
        to this method that needs to be reimplemented in the derived
        class. The default implementation does nothing.

        Args:
            event: TimerEvent

        Returns: None

        """


# Traversal routines

def depth_first_full_tree(obj):
    """
    Given an object, it goes back to root, then returns
    the whole hierarchy.

    Args:
        obj: BaseObject
            the object.

    Returns: list
        A traversal of the tree in depth first.

    """
    return depth_first_sub_tree(root(obj))


def depth_first_sub_tree(obj):
    """
    Given an object, traverses its subtree in depth first.

    Args:
        obj: BaseObject
            The object.

    Returns: list

    """
    result = [obj]
    for c in obj.children:
        result.extend(depth_first_sub_tree(c))
    return result


def root(obj):
    """
    Returns the root of the tree.

    Args:
        obj: BaseObject
            The object

    Returns: BaseObject
        The hierarchy root

    """
    return traverse_to_root(obj)[-1]


def traverse_to_root(obj):
    """
    Walks the hierarchy up until it reaches root.
    Returns the list of steps to reach the root, including root.

    Args:
        obj: BaseObject
            The object.

    Returns: list

    """
    result = [obj]
    if obj.parent is None:
        return result
    result.extend(traverse_to_root(obj.parent))
    return result


def depth_first_right_tree(obj):
    """
    Given a full, starting from root depth first traversal,
    returns all nodes from obj excluded to the end.

    Args:
        obj: BaseObject
            The object.

    Returns: list

    """
    depth_first_tree = depth_first_full_tree(obj)
    return depth_first_tree[depth_first_tree.index(obj)+1:]


def depth_first_left_tree(obj):
    """
    Given a full, starting from root depth first traversal,
    returns all nodes up to obj excluded.

    Args:
        obj: BaseObject
            The object.

    Returns: list

    """
    depth_first_tree = depth_first_full_tree(obj)
    return depth_first_tree[:depth_first_tree.index(obj)]
