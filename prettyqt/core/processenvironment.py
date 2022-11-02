from __future__ import annotations

from collections.abc import Iterator, Mapping

from prettyqt.qt import QtCore


class ProcessEnvironment(QtCore.QProcessEnvironment):
    def __bool__(self):
        return not self.isEmpty()

    def __contains__(self, other: str):
        return self.contains(other)

    def __getitem__(self, index: str) -> str:
        if index not in self:
            raise KeyError("Environment variable not set.")
        return self.value(index)

    def __delitem__(self, index: str):
        self.remove(index)

    def __setitem__(self, index: str, value: str):
        return self.insert(index, value)

    def __iter__(self) -> Iterator[tuple[str, str]]:
        return iter((k, self.value(k)) for k in self.keys())

    def update(self, other: Mapping[str, str]):
        for k, v in other.items():
            self.insert(k, v)

    def items(self):
        return list(self)

    @classmethod
    def get_system_environment(cls) -> ProcessEnvironment:
        return cls(cls.systemEnvironment())

    @classmethod
    def from_dict(cls, dictionary: Mapping[str, str]) -> ProcessEnvironment:
        env = cls()
        for k, v in dictionary.items():
            env.insert(k, v)
        return env


if __name__ == "__main__":
    env = ProcessEnvironment.get_system_environment()
    print(dict(env))
