from __future__ import annotations

import logging

from typing import Literal

from typing_extensions import Self

from prettyqt import qml
from prettyqt.utils import bidict, get_repr


logger = logging.getLogger()

ErrorTypeStr = Literal["none", "generic", "range", "reference", "syntax", "type", "uri"]

ERROR_TYPES = bidict(
    none=qml.QJSValue.ErrorType(0),
    generic=qml.QJSValue.ErrorType.GenericError,
    range=qml.QJSValue.ErrorType.RangeError,
    reference=qml.QJSValue.ErrorType.ReferenceError,
    syntax=qml.QJSValue.ErrorType.SyntaxError,
    type=qml.QJSValue.ErrorType.TypeError,
    uri=qml.QJSValue.ErrorType.URIError,
)


class JSValue(qml.QJSValue):
    """Acts as a container for Qt/JavaScript data types."""

    def __repr__(self):
        return get_repr(self, self.toVariant())

    def __len__(self):
        return self.property("length").toVariant()

    def __getitem__(self, index: int | str):
        return self.property(index).toVariant()

    def __delitem__(self, index: str):
        self.deleteProperty(index)

    def __setitem__(self, index: int | str, value):
        self.setProperty(index, value)

    def __iter__(self):
        iterator = qml.JSValueIterator(self)
        return iter(list(iterator))

    def __contains__(self, index: str):
        return self.hasProperty(index)

    def __call__(self, *args) -> JSValue:
        result = self.call(args)
        return JSValue(result)

    def get_value(self):
        return self.toVariant()

    def get_error_type(self) -> ErrorTypeStr | None:
        if (error_type := self.errorType()) == qml.QJSValue.ErrorType(0):
            return None
        else:
            return ERROR_TYPES.inverse[error_type]

    @classmethod
    def from_object(cls, obj, jsengine: qml.QJSEngine) -> Self:
        """Convert any python object into a QJSValue (must happen in GUI thread)."""
        match obj:
            case None:
                return cls()
            case list() | tuple():
                length = len(obj)
                array = cls(jsengine.newArray(length))
                for i, v in enumerate(obj):
                    array.setProperty(i, cls.from_object(v, jsengine))
                return array
            case dict():
                array = cls(jsengine.newArray())
                for k, v in obj.items():
                    array.setProperty(k, cls.from_object(v, jsengine))
                return array
            case _:
                try:
                    return cls(obj)
                except TypeError:
                    logger.debug(f"unknown type: {obj}")
                    return cls()


if __name__ == "__main__":
    val = JSValue()
