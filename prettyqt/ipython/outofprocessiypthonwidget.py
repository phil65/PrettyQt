from __future__ import annotations

import logging
import multiprocessing
import os
import sys

import IPython
from qtconsole.client import QtKernelClient
from qtconsole.rich_jupyter_widget import RichJupyterWidget

from prettyqt import core, widgets


# import asyncio


logger = logging.getLogger(__name__)


def run_server(connection_file: os.PathLike):
    IPython.embed_kernel(
        local_ns=sys._getframe(1).f_locals,
        connection_file=os.fspath(connection_file),
        gui="qt6",
    )


class OutOfProcessIPythonWidget(RichJupyterWidget, widgets.WidgetMixin):
    """Convenience class for a live IPython console widget running out-of-process."""

    def __init__(self, *args, **kwargs):
        super().__init__(
            gui_completion="droplist",  # 'plain', 'droplist', 'ncurses'
            kind="rich",  # 'plain', 'rich', only applies when no custom control set.
            paging="vsplit",  # h  'inside', 'hsplit', 'vsplit', 'custom', 'none'
            custom_control=widgets.TextEdit,
            custom_page_control=widgets.TextEdit,
        )
        self.banner = "IPython Console"
        widgets.Application.call_on_exit(self.stop)
        # self.exit_requested.connect(self.stop)
        widgets.Application.styleHints().colorSchemeChanged.connect(
            self.adjust_style_to_palette
        )
        self.adjust_style_to_palette()
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
        kernel_client = QtKernelClient(connection_file=os.fspath(self.connection_file))
        kernel_client.load_connection_file()  # can throw FileNotFoundError
        kernel_client.start_channels()
        self.kernel_client = kernel_client

    def adjust_style_to_palette(self):
        """Adjust coloring of the terminal to current palette."""
        pal = widgets.Application.get_palette()
        style = "linux" if pal.is_dark() else "lightbg"
        self.set_default_style(style)

    def stop(self):
        """Stop IPython server process and clean up."""
        logger.info("shutting down IPython MP kernel")
        self.kernel_client.stop_channels()
        self.kernel_client.shutdown()
        self.p.terminate()
        self.connection_file.unlink(missing_ok=True)
        logger.info("shutdown successful.")

    def clear(self):
        """Clear the terminal."""
        self._control.clear()

        # self.kernel_manager

    def print_text(self, text: str, before_prompt: bool = False):
        """Print some plain text to the console."""
        self._append_plain_text(text)

    def execute_command(self, command: str):
        """Execute a command in the frame of the console widget."""
        self._execute(command, False)


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
