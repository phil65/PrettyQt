from __future__ import annotations

from prettyqt.qt import QtCore


class JsonValue(QtCore.QJsonValue):
    def __str__(self):
        return str(self.toVariant())

    def __repr__(self):
        return f"{type(self).__name__}({self.toVariant()!r})"


if __name__ == "__main__":
    from prettyqt import core

    doc = core.JsonDocument.from_variant(dict(a="b"))
    print(doc.toVariant())
    print(str(doc))
    new = core.JsonDocument()
    new.setObject(doc.object())
    print("test")
    val = doc["a"]
    print(type(val), val)
