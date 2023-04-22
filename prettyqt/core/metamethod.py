from __future__ import annotations

from typing import Literal

from prettyqt import core
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
    def __init__(self, metamethod: QtCore.QMetaMethod):
        self.item = metamethod

    def __getattr__(self, val):
        return getattr(self.item, val)

    def __bool__(self):
        return self.item.isValid()

    def __repr__(self):
        return f"{type(self).__name__}({self.get_name()!r})"

    def get_access(self) -> AccessStr:
        return ACCESS.inverse[self.item.access()]

    def get_method_type(self) -> MethodTypeStr:
        return METHOD_TYPE.inverse[self.item.methodType()]

    def get_method_signature(self) -> str:
        return self.item.methodSignature().data().decode()

    def get_name(self) -> str:
        return self.item.name().data().decode()

    def get_parameters(self) -> list[core.MetaType]:
        count = self.parameterCount()
        return [core.MetaType(self.parameterMetaType(i).id()) for i in range(count)]

    def get_return_type(self) -> core.MetaType:
        return core.MetaType(self.returnMetaType().id())


if __name__ == "__main__":
    metaobj = core.Object.get_metaobject()
    method = metaobj.get_method("objectNameChanged")
    print(method.get_parameters())
