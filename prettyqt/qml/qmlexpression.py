from __future__ import annotations

import pathlib

from prettyqt import core, qml
from prettyqt.qt import QtQml


class QmlExpression(core.ObjectMixin, QtQml.QQmlExpression):
    def get_source_file(self) -> pathlib.Path | None:
        return pathlib.Path(source) if (source := self.sourceFile()) else None

    def get_error(self) -> qml.QmlError:
        return qml.QmlError(self.error())


if __name__ == "__main__":
    exp = QmlExpression()
    print(exp.get_error())
