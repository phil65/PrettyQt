from __future__ import annotations

from prettyqt.qt import QtDesigner


class AbstractFormBuilderMixin:
    pass


class AbstractFormBuilder(AbstractFormBuilderMixin, QtDesigner.QAbstractFormBuilder):
    pass


if __name__ == "__main__":
    builder = AbstractFormBuilder()
    print(dir(builder))
