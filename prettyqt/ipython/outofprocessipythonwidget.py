from __future__ import annotations

import logging
import multiprocessing
import os
import sys

import IPython
from qtconsole.client import QtKernelClient

from prettyqt import core, ipython, widgets


logger = logging.getLogger(__name__)

# ipython = IPython.get_ipython()
# ipython.magic(f"gui qt{qt.QT_VERSION}")

# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def run_server(connection_file: os.PathLike):
    IPython.embed_kernel(
        local_ns=sys._getframe(1).f_locals,
        connection_file=os.fspath(connection_file),
        gui="qt6",
    )


class OutOfProcessIPythonWidget(ipython.BaseIPythonWidget):
    """Convenience class for a live IPython console widget running out-of-process."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        temp_path = core.Dir.get_temp_path()
        self.connection_file = temp_path / f"connection-{os.getpid()}.json"
        self.p = multiprocessing.Process(target=run_server, args=(self.connection_file,))
        self.p.daemon = True
        self.p.start()
        logger.info("waiting for connection file creation....")
        for _ in range(500):
            if self.connection_file.exists() and self.connection_file.stat().st_size > 0:
                break
            widgets.app().sleep(0.1)
        else:
            raise FileNotFoundError(self.connection_file)
        logger.info("Connection file found. Opening channels.")
        kernel_client = QtKernelClient(connection_file=os.fspath(self.connection_file))
        kernel_client.load_connection_file()  # can throw FileNotFoundError
        kernel_client.start_channels()
        self.kernel_client = kernel_client

    def shutdown(self):
        """Stop IPython server process and clean up."""
        logger.info("shutting down IPython MP kernel")
        self.kernel_client.stop_channels()
        self.kernel_client.shutdown()
        self.p.terminate()
        self.connection_file.unlink(missing_ok=True)
        logger.info("shutdown successful.")


if __name__ == "__main__":
    from prettyqt.custom_widgets import commandpalette

    app = widgets.app()
    cp = commandpalette.CommandPalette()
    app.set_style("fusion")
    console_widget = OutOfProcessIPythonWidget(app)
    console_widget.print_text("hallo")
    console_widget.show()
    console_widget.add_shortcut("Ctrl+P", cp.show)
    cp.populate_from_widget(console_widget)
    app.main_loop()
