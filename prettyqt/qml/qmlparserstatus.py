from typing import TYPE_CHECKING

from prettyqt.qt import QtQml


if TYPE_CHECKING:
    _QmlParserStatusBase = QtQml.QQmlParserStatus
else:
    _QmlParserStatusBase = object


class QmlParserStatusMixin(_QmlParserStatusBase):
    pass


class QmlParserStatus(QmlParserStatusMixin, QtQml.QQmlParserStatus):
    """Updates on the QML parser state."""
