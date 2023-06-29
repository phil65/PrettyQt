from __future__ import annotations

from prettyqt import core, network


class SingleApplicationMixin:
    message_received = core.Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # generate a (hopefully) unique name
        self.app_id = type(self).__name__ + self.applicationName()
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
            # self._out_stream.set_codec("UTF-8")

    def is_running(self) -> bool:
        return self._is_running

    def _activate_window(self):
        # bit dumb inheritance check to avoid importing QtWidgets so that this mixin
        # can also get used with QGuiApplication and QCoreApplication
        if hasattr(self, "get_mainwindow"):
            window = self.get_mainwindow()
            if window is None:
                return
            window.raise_to_top()

    def _send_message(self, msg: str) -> bool:
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
        # self._in_stream.set_codec("UTF-8")
        self._in_socket.readyRead.connect(self._on_ready_read)
        if self._activate_on_message:
            self._activate_window()

    def _on_ready_read(self):
        if self._in_stream is None:
            raise RuntimeError
        for msg in self._in_stream.read_lines():
            self.message_received.emit(msg)


if __name__ == "__main__":
    App = type("SingleApp", (SingleApplicationMixin, core.CoreApplication), {})
    app1 = App()
    # app1.exec()

# Alternative:
# logger = logging.getLogger(__name__)


# class SingleApplicationMixin:
#     message_received = core.Signal(str)

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # generate a (hopefully) unique name
#         self.key = type(self).__name__ + self.applicationName()
#         self.timeout = 1000
#         self.server = network.LocalServer(self)

#         # cleanup (only needed for unix)
#         core.SharedMemory(self.key).attach()
#         self.memory = core.SharedMemory(self)
#         self.memory.setKey(self.key)

#         if self.memory.attach():
#             self.is_running = True
#             self.send_message(sys.argv[1] if len(sys.argv) > 1 else "show")
#             logger.info("Another instance is already running.")
#             sys.exit(1)

#         self.is_running = False
#         if not self.memory.create(1):
#             logger.error(self.memory.errorString())
#             raise RuntimeError(self.memory.errorString())

#         self.server.newConnection.connect(self._on_new_connection)
#         self.server.listen(self.key)

#     def _on_new_connection(self):
#         socket = self.server.nextPendingConnection()
#         if socket.waitForReadyRead(self.timeout):
#             data = socket.readAll().data().decode()
#             self.message_received.emit(data)
#             socket.disconnectFromServer()

#     def send_message(self, message: str):
#         if not self.is_running:
#             return

#         # connect to another application
#         socket = network.LocalSocket(self)
#         socket.connectToServer(self.key, socket.OpenModeFlag.WriteOnly)
#         if not socket.waitForConnected(self.timeout):
#             logger.error(socket.errorString())
#             return

#         # send message
#         socket.write(message.encode())
#         if not socket.waitForBytesWritten(self.timeout):
#             logger.error(socket.errorString())
#             return

#         socket.disconnectFromServer()


# if __name__ == "__main__":
#     App = type("SingleApp", (SingleApplicationMixin, core.CoreApplication), {})
#     app1 = App(sys.argv)
#     app1.exec()
