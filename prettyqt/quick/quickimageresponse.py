from qtpy import QtQuick

from prettyqt import core


QtQuick.QQuickImageResponse.__bases__ = (core.Object,)


class QuickImageResponse(QtQuick.QQuickImageResponse):
    pass


if __name__ == "__main__":
    item = QuickImageResponse()
