from __future__ import annotations

import logging
from typing import Literal

from typing_extensions import Self

from prettyqt import qml
from prettyqt.qt import QtQml
from prettyqt.utils import bidict, get_repr


logger = logging.getLogger()

ErrorTypeStr = Literal["none", "generic", "range", "reference", "syntax", "type", "uri"]

ERROR_TYPES = bidict(
    none=QtQml.QJSValue.ErrorType(0),
    generic=QtQml.QJSValue.ErrorType.GenericError,
    range=QtQml.QJSValue.ErrorType.RangeError,
    reference=QtQml.QJSValue.ErrorType.ReferenceError,
    syntax=QtQml.QJSValue.ErrorType.SyntaxError,
    type=QtQml.QJSValue.ErrorType.TypeError,
    uri=QtQml.QJSValue.ErrorType.URIError,
)


class JSValue(QtQml.QJSValue):
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
        if (error_type := self.errorType()) == QtQml.QJSValue.ErrorType(0):
            return None
        else:
            return ERROR_TYPES.inverse[error_type]

    @classmethod
    def from_object(cls, obj, jsengine: QtQml.QJSEngine) -> Self:
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
                    logger.debug(f"unknown type: {str(obj)}")
                    return cls()


if __name__ == "__main__":
    val = JSValue()
