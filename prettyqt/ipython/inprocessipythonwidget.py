from __future__ import annotations

import importlib.util
import logging

from qtconsole.inprocess import QtInProcessKernelManager

from prettyqt import core, ipython, widgets


# import asyncio


logger = logging.getLogger(__name__)


class InProcessIPythonWidget(ipython.BaseIPythonWidget):
    """Convenience class for a live IPython console widget."""

    evaluated = core.Signal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

    def shutdown(self):
        logger.info("shutting down IPython kernel...")
        self.kernel_client.stop_channels()
        self.kernel_manager.shutdown_kernel()
        logger.info("shutdown successful.")

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
        return data


if __name__ == "__main__":
    app = widgets.app()
    app.set_style("fusion")
    console_widget = InProcessIPythonWidget(app)
    console_widget.print_text("hallo")
    console_widget.show()
    console_widget.evaluated.connect(print)
    app.sleep(5)
    console_widget.clear()
    app.main_loop()
