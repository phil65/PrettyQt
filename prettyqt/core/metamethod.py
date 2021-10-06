from __future__ import annotations

from typing import Literal

from prettyqt.qt import QtCore
from prettyqt.utils import bidict


ACCESS = bidict(
    private=QtCore.QMetaMethod.Access.Private,
    protected=QtCore.QMetaMethod.Access.Protected,
    public=QtCore.QMetaMethod.Access.Public,
)

AccessStr = Literal["private", "protected", "public"]

METHOD_TYPE = bidict(
    method=QtCore.QMetaMethod.MethodType.Method,
    signal=QtCore.QMetaMethod.MethodType.Signal,
    slot=QtCore.QMetaMethod.MethodType.Slot,
    constructor=QtCore.QMetaMethod.MethodType.Constructor,
)

MethodTypeStr = Literal["method", "signal", "slot", "constructor"]


class MetaMethod:
    def __init__(self, metaobject: QtCore.QMetaMethod):
        self.item = metaobject

    def __bool__(self):
        return self.item.isValid()

    def __repr__(self):
        return f"{type(self).__name__}({self.get_name()!r})"

    def get_access(self) -> AccessStr:
        return ACCESS.inverse[self.item.access()]

    def get_method_type(self) -> MethodTypeStr:
        return METHOD_TYPE.inverse[self.item.methodType()]

    def get_method_signature(self) -> str:
        return bytes(self.item.methodSignature()).decode()

    def get_name(self) -> str:
        return bytes(self.item.name()).decode()


if __name__ == "__main__":
    from prettyqt import core

    metaobj = core.Object.get_metaobject()
    method = metaobj.get_method("to_json")
