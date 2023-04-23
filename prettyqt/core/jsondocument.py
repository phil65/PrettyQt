from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import get_repr


class JsonDocument(QtCore.QJsonDocument):
    def __str__(self):
        return str(self.toVariant())

    def __repr__(self):
        return get_repr(self, self.toVariant())

    def __getitem__(self, index: int | str):
        val = self.array() if self.isArray() else self.object()
        return core.JsonValue(val[index])  # type: ignore

    def __setitem__(self, index: int | str, value):
        if self.isArray():
            if not isinstance(index, int):
                raise TypeError()
            array = self.array()
            array[index] = value
            self.setArray(array)
        elif self.isObject():
            if not isinstance(index, str):
                raise TypeError()
            obj = self.object()
            obj[index] = value
            self.setObject(obj)

    def to_string(self, indented: bool = False) -> str:
        flag = self.JsonFormat.Indented if indented else self.JsonFormat.Compact
        return self.toJson(flag).data().decode()

    @classmethod
    def from_variant(cls, obj) -> JsonDocument:
        doc = cls.fromVariant(obj)
        new = cls()
        if doc.isArray():
            new.setArray(doc.array())
        else:
            new.setObject(doc.object())
        return new


if __name__ == "__main__":
    doc = JsonDocument.from_variant(dict(a="b"))
    print(doc.toVariant())
    print(doc)
    new = JsonDocument()
    new.setObject(doc.object())
    print(type(new["a"]))
    print(new["a"])
    new["k"] = "v"
    print("new", new["k"])
    print(new.to_json())
