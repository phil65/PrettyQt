from __future__ import annotations

import importlib.util
import logging

from qtconsole.inprocess import QtInProcessKernelManager
from qtconsole.rich_jupyter_widget import RichJupyterWidget

from prettyqt import core, widgets


# import asyncio


logger = logging.getLogger(__name__)

# disables 'Please pass -Xfrozen_modules=off' warning
# os.environ["PYDEVD_DISABLE_FILE_VALIDATION"] = "1"


class InProcessIPythonWidget(widgets.WidgetMixin, RichJupyterWidget):
    """Convenience class for a live IPython console widget."""

    evaluated = core.Signal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.banner = "IPython Console"
        self.font_size = 6
        self.gui_completion = "droplist"
        widgets.Application.styleHints().colorSchemeChanged.connect(
            self.adjust_style_to_palette
        )
        self.adjust_style_to_palette()
        self.kernel_manager = QtInProcessKernelManager()
        self.kernel_manager.start_kernel(show_banner=False)

        # def _abort_queues(kernel):
        #     """override to prevent breaking when exception occurs"""
        #     pass

        # self.kernel_manager.kernel._abort_queues = _abort_queues
        self.kernel_manager.kernel.log.setLevel(logging.CRITICAL)
        self.kernel_manager.kernel.gui = "qt"
        if importlib.util.find_spec("matplotlib"):
            self.kernel_manager.kernel.shell.enable_matplotlib(gui="inline")
        self.kernel_client = self._kernel_manager.client()
        self.kernel_client.start_channels()

        def stop():
            logger.info("shutting down IPython kernel...")
            self.kernel_client.stop_channels()
            self.kernel_manager.shutdown_kernel()
            logger.info("shutdown successful.")

        widgets.Application.call_on_exit(stop)
        # self.exit_requested.connect(stop)

    def adjust_style_to_palette(self):
        """Adjust coloring of the terminal to current palette."""
        pal = widgets.Application.get_palette()
        style = "linux" if pal.is_dark() else "lightbg"
        self.set_default_style(style)

    def push_vars(self, var_dict):
        """Send python objects to IPYthon namespace.

        Given a dictionary containing name / value pairs, push those variables
        to the IPython console widget.
        """
        self.kernel_manager.kernel.shell.push(var_dict)
        for key in var_dict.keys():
            self._append_plain_text(f'\nadded "{key}" object to namespace\n', True)

    def eval(self, obj_name):
        """Pull object with name *obj_name from namespace."""
        try:
            data = self.kernel_manager.kernel.shell.ev(obj_name)
        except NameError as e:
            logger.exception(e)
            return None
        self._append_plain_text(f'\nread "{obj_name}" object to namespace\n', True)
        self.evaluated.emit(data)

    def clear(self):
        """Clear the terminal."""
        self._control.clear()

    def print_text(self, text):
        """Print some plain text to the console."""
        self._append_plain_text(text)

    def execute_command(self, command):
        """Execute a command in the frame of the console widget."""
        self._execute(command, False)


if __name__ == "__main__":
    app = widgets.app()
    app.set_style("fusion")
    console_widget = InProcessIPythonWidget(app)
    console_widget.print_text("hallo")
    console_widget.show()
    app.sleep(5)
    console_widget.clear()
    app.main_loop()
