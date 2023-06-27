from __future__ import annotations

from typing import Literal

from typing_extensions import Self

from prettyqt import core
from prettyqt.utils import bidict, get_repr


JsonFormatStr = Literal["indented", "compact"]


JSON_FORMAT: bidict[JsonFormatStr, core.QJsonDocument.JsonFormat] = bidict(
    indented=core.QJsonDocument.JsonFormat.Indented,
    compact=core.QJsonDocument.JsonFormat.Compact,
)


class JsonDocument(core.QJsonDocument):
    def __str__(self):
        return str(self.toVariant())

    def __format__(self, fmt):
        if fmt in JSON_FORMAT:
            return self.to_string(fmt == "indented")
        return super().__format__(fmt)

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
    def from_variant(cls, obj) -> Self:
        doc = cls.fromVariant(obj)
        new = cls()
        if doc.isArray():
            new.setArray(doc.array())
        else:
            new.setObject(doc.object())
        return new


if __name__ == "__main__":
    doc = JsonDocument.from_variant(dict(a="b"))
    new = JsonDocument()
    new.setObject(doc.object())
    new["k"] = "v"
