from typing import Literal, Self

from prettyqt.qt import QtCore
from prettyqt.utils import bidict, get_repr


TypeStr = Literal["system_v", "posix_realtime", "windows"]

TYPE: bidict[TypeStr, QtCore.QNativeIpcKey.Type] = bidict(
    system_v=QtCore.QNativeIpcKey.Type.SystemV,
    posix_realtime=QtCore.QNativeIpcKey.Type.PosixRealtime,
    windows=QtCore.QNativeIpcKey.Type.Windows,
)


class NativeIpcKey(QtCore.QNativeIpcKey):
    """Holds a native key used by QSystemSemaphore and QSharedMemory."""

    def __init__(
        self,
        key: str | QtCore.QNativeIpcKey = "",
        typ: TypeStr | QtCore.QNativeIpcKey.Type | None = None,
    ):
        if isinstance(key, QtCore.QNativeIpcKey) or typ is None:
            super().__init__(key)
        else:
            super().__init__(key, TYPE.get_enum_value(typ))

    def __repr__(self):
        return get_repr(self, self.nativeKey(), self.get_type())

    def __str__(self):
        return self.toString()

    def __bool__(self):
        return self.isValid()

    def set_type(self, typ: TypeStr | QtCore.QNativeIpcKey.Type):
        """Set the IPC key type.

        Args:
            typ: IPC key type to use
        """
        self.setType(TYPE.get_enum_value(typ))

    def get_type(self) -> TypeStr:
        """Return the IPC key type.

        Returns:
            IPC key type
        """
        return TYPE.inverse[self.type()]

    @classmethod
    def from_string(cls, string: str) -> Self:
        return cls(cls.fromString(string))
