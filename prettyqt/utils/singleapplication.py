from __future__ import annotations

import sys

from prettyqt import core, network, widgets


class SingleApplication(widgets.Application):

    messageReceived = core.Signal(str)

    def __init__(self, app_id: str):

        super().__init__(sys.argv)
        self.app_id = app_id
        self._activate_on_message = True

        # Is there another instance running?
        out_socket = network.LocalSocket()
        out_socket.connect_to_server(self.app_id)
        self._is_running = out_socket.waitForConnected()
        self._in_socket = None
        self._in_stream = None
        if not self._is_running:
            self._out_socket = None
            self._out_stream = None
            self._server = network.LocalServer()
            self._server.listen(self.app_id)
            self._server.newConnection.connect(self._on_new_connection)
        else:
            self._out_socket = out_socket
            self._out_stream = core.TextStream(self._out_socket)
            self._out_stream.set_codec("UTF-8")

    def is_running(self) -> bool:
        return self._is_running

    def activate_window(self):
        window = self.get_mainwindow()
        if window is None:
            return
        window.raise_to_top()

    def send_message(self, msg: str) -> bool:
        if self._out_stream is None or self._out_socket is None:
            return False
        self._out_stream << msg << "\n"
        self._out_stream.flush()
        return self._out_socket.waitForBytesWritten()

    def _on_new_connection(self):
        if self._in_socket:
            self._in_socket.readyRead.disconnect(self._on_ready_read)
        self._in_socket = self._server.nextPendingConnection()  # type: ignore
        if self._in_socket is None:
            return
        self._in_stream = core.TextStream(self._in_socket)
        self._in_stream.set_codec("UTF-8")
        self._in_socket.readyRead.connect(self._on_ready_read)
        if self._activate_on_message:
            self.activate_window()

    def _on_ready_read(self):
        if self._in_stream is None:
            raise RuntimeError()
        for msg in self._in_stream.read_lines():
            self.messageReceived.emit(msg)


if __name__ == "__main__":
    app1 = SingleApplication("test")
    print(app1.is_running())
    app1.exec()
