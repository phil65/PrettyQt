# credits to
# https://stackoverflow.com/questions/48425316/how-to-create-pyqt-properties-dynamically
from __future__ import annotations

import functools

from prettyqt.qt import QtCore


class PropertyMeta(type(QtCore.QObject)):
    """Lets a class succinctly define Qt properties."""

    def __new__(cls, name, bases, attrs):
        for key in list(attrs.keys()):
            attr = attrs[key]
            if not isinstance(attr, SyncedProperty):
                continue

            types = {list: "QVariantList", dict: "QVariantMap"}
            type_ = types.get(attr.type_, attr.type_)

            notifier = QtCore.Signal(type_)
            attrs[f"_{key}_changed"] = notifier
            attrs[key] = PropertyImpl(type_=type_, name=key, notify=notifier)

        return super().__new__(cls, name, bases, attrs)


class SyncedProperty:
    """Property definition.

    Instances of this class will be replaced with their full
    implementation by the PropertyMeta metaclass.
    """

    def __init__(self, type_):
        self.type_ = type_


class PropertyImpl(QtCore.Property):
    """Property implementation: gets, sets, and notifies of change."""

    def __init__(self, type_, name, notify):
        super().__init__(type_, self.getter, self.setter, notify=notify)
        self.name = name

    def getter(self, instance):
        return getattr(instance, f"_{self.name}")

    def setter(self, instance, value):
        signal = getattr(instance, f"_{self.name}_changed")

        if type(value) in {list, dict}:
            value = make_notified(value, signal)

        setattr(instance, f"_{self.name}", value)
        signal.emit(value)


class MakeNotified:
    """Adds notifying signals to lists and dictionaries.

    Creates the modified classes just once, on initialization.
    """

    change_methods = {
        list: [
            "__delitem__",
            "__iadd__",
            "__imul__",
            "__setitem__",
            "append",
            "extend",
            "insert",
            "pop",
            "remove",
            "reverse",
            "sort",
        ],
        dict: [
            "__delitem__",
            "__ior__",
            "__setitem__",
            "clear",
            "pop",
            "popitem",
            "setdefault",
            "update",
        ],
    }

    def __init__(self):
        self.notified_class = {
            type_: self.make_notified_class(type_) for type_ in [list, dict]
        }

    def __call__(self, seq, signal):
        """Returns a notifying version of the supplied list or dict."""
        notified_class = self.notified_class[type(seq)]
        notified_seq = notified_class(seq)
        notified_seq.signal = signal
        return notified_seq

    @classmethod
    def make_notified_class(cls, parent):
        notified_class = type(f"notified_{parent.__name__}", (parent,), {})
        for method_name in cls.change_methods[parent]:
            original = getattr(notified_class, method_name)
            notified_method = cls.make_notified_method(original, parent)
            setattr(notified_class, method_name, notified_method)
        return notified_class

    @staticmethod
    def make_notified_method(method, parent):
        @functools.wraps(method)
        def notified_method(self, *args, **kwargs):
            result = getattr(parent, method.__name__)(self, *args, **kwargs)
            self.signal.emit(self)
            return result

        return notified_method


make_notified = MakeNotified()


if __name__ == "__main__":

    class Demo(QtCore.QObject, metaclass=PropertyMeta):
        number = SyncedProperty(float)
        things = SyncedProperty(list)

        def __init__(self, parent=None):
            super().__init__(parent)
            self.number = 3.14

    demo1 = Demo()
    demo2 = Demo()
    demo1.number = 2.7
    demo1.things = ["spam", "spam", "baked beans", "spam"]
