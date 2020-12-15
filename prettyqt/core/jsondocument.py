from typing import Union

from qtpy import QtCore

from prettyqt import core


class JsonDocument(QtCore.QJsonDocument):
    def __str__(self):
        return str(self.toVariant())

    def __repr__(self):
        return f"{type(self).__name__}({self.toVariant()!r})"

    def __getitem__(self, index: Union[int, str]):
        val = self.array() if self.isArray() else self.object()
        return core.JsonValue(val[index])

    def __setitem__(self, index: Union[int, str], value):
        if self.isArray():
            if not isinstance(index, int):
                raise TypeError()
            array = self.array()
            array[index] = value
            self.setArray(array)
        if self.isObject():
            if not isinstance(index, str):
                raise TypeError()
            array = self.object()
            array[index] = value
            self.setObject(array)

    def to_string(self, indented: bool = False) -> str:
        flag = QtCore.QJsonDocument.Indented if indented else QtCore.QJsonDocument.Compact
        return bytes(self.toJson(flag)).decode()

    @classmethod
    def from_variant(cls, obj):
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
    print(str(doc))
    new = JsonDocument()
    new.setObject(doc.object())
    print("test")
    print(type(new["a"]))
    print(str(new["a"]))
    new["k"] = "v"
    print("new", new["k"])
    print(new.to_json())
