from prettyqt.qt import QtQml


class QmlParserStatusMixin:
    pass


class QmlParserStatus(QmlParserStatusMixin, QtQml.QQmlParserStatus):
    """Updates on the QML parser state."""
