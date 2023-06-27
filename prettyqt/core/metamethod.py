from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.utils import bidict, get_repr


AccessStr = Literal["private", "protected", "public"]

ACCESS: bidict[AccessStr, core.QMetaMethod.Access] = bidict(
    private=core.QMetaMethod.Access.Private,
    protected=core.QMetaMethod.Access.Protected,
    public=core.QMetaMethod.Access.Public,
)

MethodTypeStr = Literal["method", "signal", "slot", "constructor"]

METHOD_TYPE: bidict[MethodTypeStr, core.QMetaMethod.MethodType] = bidict(
    method=core.QMetaMethod.MethodType.Method,
    signal=core.QMetaMethod.MethodType.Signal,
    slot=core.QMetaMethod.MethodType.Slot,
    constructor=core.QMetaMethod.MethodType.Constructor,
)


class MetaMethod:
    def __init__(self, metamethod: core.QMetaMethod):
        self.item = metamethod

    def __getattr__(self, val):
        return getattr(self.item, val)

    def __bool__(self):
        return self.item.isValid()

    def __repr__(self):
        return get_repr(self, self.get_name())

    def get_access(self) -> AccessStr:
        return ACCESS.inverse[self.item.access()]

    def get_method_type(self) -> MethodTypeStr:
        return METHOD_TYPE.inverse[self.item.methodType()]

    def get_method_signature(self) -> str:
        return self.item.methodSignature().data().decode()

    def get_normalized_method_signature(self) -> str:
        """Returns something like 'objectNameChanged(QString)'."""
        sig = self.item.methodSignature()
        normalized = core.QMetaObject.normalizedSignature(sig.data().decode())
        return normalized.data().decode()

    def get_name(self) -> str:
        return self.item.name().data().decode()

    def get_parameters(self) -> list[core.MetaType]:
        count = self.parameterCount()
        return [core.MetaType(self.parameterMetaType(i).id()) for i in range(count)]

    def get_return_type(self) -> core.MetaType:
        return core.MetaType(self.returnMetaType().id())

    def get_parameter_types(self) -> list[str]:
        """Returns sth. like ['QString']."""
        return [i.data().decode() for i in self.parameterTypes()]


if __name__ == "__main__":
    obj = core.Object()
    metaobj = obj.get_metaobject()
    method = metaobj.get_method("objectNameChanged")
