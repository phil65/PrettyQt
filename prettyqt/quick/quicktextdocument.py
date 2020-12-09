from qtpy import QtQuick

from prettyqt import core


QtQuick.QQuickTextDocument.__bases__ = (core.Object,)


class QuickTextDocument(QtQuick.QQuickTextDocument):
    pass


if __name__ == "__main__":
    item = QuickTextDocument()
