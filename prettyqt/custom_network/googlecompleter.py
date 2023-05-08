from __future__ import annotations

from prettyqt import core, gui, network, widgets
from prettyqt.qt import QtNetwork


class GoogleSearchModel(gui.StandardItemModel):
    finished = core.Signal()
    error = core.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._manager = network.NetworkAccessManager(self)
        self._reply = None

    @core.Slot(str)
    def search(self, text):
        self.clear()
        if self._reply is not None:
            self._reply.abort()
        if text:
            r = self.create_request(text)
            self._reply = self._manager.get(r)
            self._reply.finished.connect(self.on_finished)
            loop = core.EventLoop()
            self.finished.connect(loop.quit)
            loop.exec()

    def create_request(self, text):
        url = f"https://google.com/complete/search?output=toolbar&q={text}"
        return network.NetworkRequest(url)

    @core.Slot()
    def on_finished(self):
        if self._reply.error() == QtNetwork.QNetworkReply.NetworkError.NoError:
            response = self._reply.readAll()
            for xml in core.XmlStreamReader(response.data().decode()):
                if (
                    xml.tokenType() == core.XmlStreamReader.TokenType.StartElement
                    and xml.name() == "suggestion"
                ):
                    s = xml.attributes().value("data")
                    self.appendRow(gui.StandardItem(s))
        self.finished.emit()
        # self._reply.deleteLater()


class GoogleCompleter(widgets.Completer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_completion_mode("unfiltered_popup")
        self.set_case_sensitive(False)
        self.setModel(GoogleSearchModel())
        self.setCompletionPrefix("")

    def splitPath(self, path):
        self.model().search(path)
        return super().splitPath(path)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    wnd = widgets.Widget()
    wnd.set_layout("horizontal")
    widget = widgets.LineEdit()
    wnd.box.add(widget)
    completer = GoogleCompleter(widget)
    widget.set_completer(completer)
    wnd.show()
    app.main_loop()
