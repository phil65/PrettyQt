from __future__ import annotations

from prettyqt import core, gui, network, widgets
from prettyqt.qt import QtCore, QtNetwork


class BaseScrapeModel(gui.StandardItemModel):
    finished = core.Signal()
    error = core.Signal(str)
    search_url: str

    def __init__(self, parent: QtCore.QObject | None = None):
        super().__init__(parent)
        self._manager = network.NetworkAccessManager(self)
        self._reply = None

    @core.Slot(str)
    def search(self, text: str):
        self.clear()
        if self._reply is not None:
            self._reply.abort()
        if text:
            r = self.search_url.format(text=text)
            self._reply = self._manager.get(r)
            self._reply.finished.connect(self.on_finished)
            loop = core.EventLoop()
            self.finished.connect(loop.quit)
            loop.exec()

    @core.Slot()
    def on_finished(self):
        if self._reply.error() == QtNetwork.QNetworkReply.NetworkError.NoError:
            response = self._reply.readAll().data().decode()
            for s in self.process_reply(response):
                self.appendRow(gui.StandardItem(s))
        self.finished.emit()
        # self._reply.deleteLater()

    def process_reply(self, reply: str) -> list[str]:
        return NotImplemented


class GoogleSearchModel(BaseScrapeModel):
    search_url = "https://google.com/complete/search?output=toolbar&q={text}"

    def process_reply(self, reply: str) -> list[str]:
        return [
            xml.attributes().value("data")
            for xml in core.XmlStreamReader(reply)
            if (
                xml.tokenType() == core.XmlStreamReader.TokenType.StartElement
                and xml.name() == "suggestion"
            )
        ]


class GoogleCompleter(widgets.Completer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_completion_mode("unfiltered_popup")
        self.set_case_sensitive(False)
        self.setModel(GoogleSearchModel())
        self.setCompletionPrefix("")

    def splitPath(self, path: str):
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
    app.exec()
