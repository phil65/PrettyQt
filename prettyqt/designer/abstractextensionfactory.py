from __future__ import annotations

from prettyqt.qt import QtDesigner


class AbstractExtensionFactory(QtDesigner.QAbstractExtensionFactory):
    """Interface for extension factories in Qt Designer."""


if __name__ == "__main__":
    fact = AbstractExtensionFactory()
