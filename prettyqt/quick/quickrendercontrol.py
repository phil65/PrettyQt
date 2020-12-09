from qtpy import QtQuick

from prettyqt import core


QtQuick.QQuickRenderControl.__bases__ = (core.Object,)


class QuickRenderControl(QtQuick.QQuickRenderControl):
    pass


if __name__ == "__main__":
    item = QuickRenderControl()
