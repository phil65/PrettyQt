from typing import Optional

from prettyqt import core
from prettyqt.qt import QtCore


class PropertyMeta(type(QtCore.QObject)):  # type: ignore
    def __new__(cls, name, bases, attrs):
        for key in list(attrs.keys()):
            attr = attrs[key]
            if not isinstance(attr, SyncedProperty):
                continue
            initial_value = attr.initial_value
            type_ = type(initial_value)
            notifier = core.Signal(type_)
            attrs[key] = PropertyImpl(
                initial_value, name=key, type_=type_, notify=notifier
            )
            attrs[signal_attribute_name(key)] = notifier
        return super().__new__(cls, name, bases, attrs)


class SyncedProperty:
    """Property definition.

    This property will be patched by the PropertyMeta metaclass into a PropertyImpl type.
    """

    def __init__(self, initial_value, name: str = ""):
        self.initial_value = initial_value
        self.name = name


class PropertyImpl(core.Property):
    """Actual property implementation using a signal to notify any change."""

    def __init__(
        self, initial_value, name: str = "", type_: Optional[type] = None, notify=None
    ):
        super().__init__(type_, self.getter, self.setter, notify=notify)
        self.initial_value = initial_value
        self.name = name

    def getter(self, inst):
        return getattr(inst, value_attribute_name(self.name), self.initial_value)

    def setter(self, inst, value):
        setattr(inst, value_attribute_name(self.name), value)
        notifier_signal = getattr(inst, signal_attribute_name(self.name))
        notifier_signal.emit(value)


def signal_attribute_name(property_name: str) -> str:
    """Return a magic key for the attribute storing the signal name."""
    return f"_{property_name}_prop_signal_"


def value_attribute_name(property_name: str) -> str:
    """Return a magic key for the attribute storing the property value."""
    return f"_{property_name}_prop_value_"


if __name__ == "__main__":

    class Demo(core.Object, metaclass=PropertyMeta):
        my_prop = SyncedProperty(3.14)

    Demo()
