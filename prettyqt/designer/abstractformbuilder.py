from typing import TYPE_CHECKING

from prettyqt.qt import QtDesigner


if TYPE_CHECKING:
    _AbstractFormBuilderBase = QtDesigner.QAbstractFormBuilder
else:
    _AbstractFormBuilderBase = object


class AbstractFormBuilderMixin(_AbstractFormBuilderBase):
    pass


class AbstractFormBuilder(AbstractFormBuilderMixin, QtDesigner.QAbstractFormBuilder):
    """Default implementation for classes that create user interfaces at run-time."""


if __name__ == "__main__":
    builder = AbstractFormBuilder()
    print(dir(builder))
