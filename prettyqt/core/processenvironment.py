from __future__ import annotations

from collections.abc import MutableMapping
from typing import TYPE_CHECKING, Self

from prettyqt.qt import QtCore
from prettyqt.utils import datatypes


if TYPE_CHECKING:
    from collections.abc import Iterator


class ProcessEnvironment(
    QtCore.QProcessEnvironment, MutableMapping, metaclass=datatypes.QABCMeta
):
    """Holds the environment variables that can be passed to a program."""

    def __bool__(self):
        return not self.isEmpty()

    def __contains__(self, other: str):
        return self.contains(other)

    def __getitem__(self, index: str) -> str:
        if index not in self:
            msg = "Environment variable not set."
            raise KeyError(msg)
        return self.value(index)

    def __delitem__(self, index: str):
        self.remove(index)

    def __setitem__(self, index: str, value: str):
        return self.insert(index, value)

    def __iter__(self) -> Iterator[str]:
        return iter(self.keys())

    def __len__(self):
        return len(self.keys())

    @classmethod
    def get_system_environment(cls) -> Self:
        return cls(cls.systemEnvironment())


if __name__ == "__main__":
    env = ProcessEnvironment.get_system_environment()
    env.update(dict(a="b"))
    print(list(env.items()))
