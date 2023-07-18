from __future__ import annotations

from prettyqt.qt import QtDesigner


class AbstractFormBuilderMixin:
    pass


class AbstractFormBuilder(AbstractFormBuilderMixin, QtDesigner.QAbstractFormBuilder):
    """Default implementation for classes that create user interfaces at run-time."""


if __name__ == "__main__":
    builder = AbstractFormBuilder()
    print(dir(builder))
