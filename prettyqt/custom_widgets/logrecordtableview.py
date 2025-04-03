from __future__ import annotations

import logging

from prettyqt import constants, core, custom_widgets, gui, itemmodels, widgets
from prettyqt.utils import signallogger


logger = logging.getLogger(__name__)


def color_log(x):
    match x:
        case "DEBUG":
            return gui.QColor("lightblue")
        case "INFO":
            return gui.QColor("lightgreen")
        case "WARNING":
            return gui.QColor("orange")
        case "ERROR":
            return gui.QColor("red")


class LogRecordTableView(widgets.TableView):
    """Table view showing a log table."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_selection_behavior("rows")
        self.handler = signallogger.SignalLogger()
        core.CoreApplication.call_on_exit(lambda: logger.removeHandler(self.handler))
        self.setWordWrap(True)

    def set_logger(self, logger, level=logging.DEBUG):
        model = itemmodels.LogRecordModel(parent=self)
        logger.addHandler(self.handler)
        self.handler.signals.log_record.connect(model.add)
        self.handler.setLevel(level)
        self.set_model(model)
        self.proxifier[0].modify(color_log, role=constants.BACKGROUND_ROLE)
        self.h_header = custom_widgets.FilterHeader(self)


if __name__ == "__main__":
    from prettyqt import debugging

    app = widgets.app()
    widget = widgets.LineEdit()
    widget.show()
    with app.debug_mode(), debugging.Stalker(widget, log_level=logging.INFO) as stalker:
        stalker.eventsignals.MouseButtonPress.connect(print)
        stalker.show()
        app.exec()
