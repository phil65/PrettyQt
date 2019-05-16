# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore, QtWebEngineWidgets

from prettyqt import widgets


class WebEngineView(QtWebEngineWidgets.QWebEngineView):

    @classmethod
    def from_local_file(cls, path):
        url = QtCore.QUrl.fromLocalFile(str(path))
        reader = cls()
        reader.setUrl(url)
        return reader


WebEngineView.__bases__[0].__bases__ = (widgets.Widget,)


if __name__ == "__main__":
    from prettyqt import widgets
    app = widgets.app()
    path = path = "E:\\dev\\datacook\\processanalyzer\\docs\\index.html"
    widget = WebEngineView.from_local_file(path)
    widget.show()
    app.exec_()
