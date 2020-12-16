from __future__ import annotations

import logging
from typing import Optional, Union

from qtpy import QtQml

from prettyqt import qml
from prettyqt.utils import bidict


logger = logging.getLogger()

ERROR_TYPES = bidict(
    generic=QtQml.QJSValue.GenericError,
    range=QtQml.QJSValue.RangeError,
    reference=QtQml.QJSValue.ReferenceError,
    syntax=QtQml.QJSValue.SyntaxError,
    type=QtQml.QJSValue.TypeError,
    uri=QtQml.QJSValue.URIError,
)


class JSValue(QtQml.QJSValue):
    def __repr__(self):
        return f"JSValue({self.toVariant()})"

    def __len__(self):
        return self.property("length").toVariant()

    def __getitem__(self, index: Union[int, str]):
        return self.property(index).toVariant()

    def __delitem__(self, index: str):
        self.deleteProperty(index)

    def __setitem__(self, index: Union[int, str], value):
        self.setProperty(index, value)

    def __iter__(self):
        iterator = qml.JSValueIterator(self)
        return iter([val for val in iterator])

    def __contains__(self, index: str):
        return self.hasProperty(index)

    def get_value(self):
        return self.toVariant()

    def get_error_type(self) -> Optional[str]:
        error_type = self.errorType()
        if int(error_type) == 0:
            return None
        return ERROR_TYPES.inverse[error_type]

    @classmethod
    def from_object(cls, obj, jsengine) -> JSValue:
        """Convert any python object into a QJSValue (must happen in GUI thread)."""
        if obj is None:
            return cls()
        elif isinstance(obj, list) or isinstance(obj, tuple):
            length = len(obj)
            array = JSValue(jsengine.newArray(length))
            for i, v in enumerate(obj):
                array.setProperty(i, cls.from_object(v, jsengine))
            return array
        elif isinstance(obj, dict):
            array = JSValue(jsengine.newArray())
            for k, v in obj.items():
                array.setProperty(k, cls.from_object(v, jsengine))
            return array
        else:
            try:
                return cls(obj)
            except TypeError:
                logger.debug("unknown type: " + str(obj))
                return cls()


if __name__ == "__main__":
    val = JSValue()
