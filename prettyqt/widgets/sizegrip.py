from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QSizeGrip.__bases__ = (widgets.Widget,)


class SizeGrip(QtWidgets.QSizeGrip):
    pass


if __name__ == "__main__":
    app = widgets.app()
    widget = SizeGrip()
    widget.show()
    app.main_loop()
