from __future__ import annotations

from prettyqt.qt import QtDesigner


class AbstractExtensionFactory(QtDesigner.QAbstractExtensionFactory):
    pass


if __name__ == "__main__":
    fact = AbstractExtensionFactory()
