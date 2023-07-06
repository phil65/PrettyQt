from __future__ import annotations

import logging
import traceback

from prettyqt import constants, core, itemmodels, widgets
from prettyqt.utils import signallogger


logger = logging.getLogger(__name__)


class LevelNameColumn(itemmodels.ColumnItem):
    name = "Level"

    def get_data(self, item: logging.LogRecord, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return item.levelname


class FileNameColumn(itemmodels.ColumnItem):
    name = "File name"

    def get_data(self, item: logging.LogRecord, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return item.filename


class FunctionNameColumn(itemmodels.ColumnItem):
    name = "Function name"

    def get_data(self, item: logging.LogRecord, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return item.funcName


class LineNoColumn(itemmodels.ColumnItem):
    name = "Line number"

    def get_data(self, item: logging.LogRecord, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return str(item.lineno)


class ModuleColumn(itemmodels.ColumnItem):
    name = "Module"

    def get_data(self, item: logging.LogRecord, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return item.module


class CreatedColumn(itemmodels.ColumnItem):
    name = "Created"
    display_format = "yyyy-MM-dd hh:mm:ss.zzzzzz"

    def get_data(self, item: logging.LogRecord, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                dt = core.DateTime.from_seconds(item.created)
                return dt.fromString(self.display_format)
            case constants.USER_ROLE:
                return core.DateTime.from_seconds(item.created)


class ProcessColumn(itemmodels.ColumnItem):
    name = "Process"

    def get_data(self, item: logging.LogRecord, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return str(item.process)
            case constants.USER_ROLE:
                return item.process


class ThreadColumn(itemmodels.ColumnItem):
    name = "Thread"

    def get_data(self, item: logging.LogRecord, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return str(item.thread)
            case constants.USER_ROLE:
                return item.thread


class ProcessNameColumn(itemmodels.ColumnItem):
    name = "Process name"

    def get_data(self, item: logging.LogRecord, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return item.processName or ""


class ThreadNameColumn(itemmodels.ColumnItem):
    name = "Thread name"

    def get_data(self, item: logging.LogRecord, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return item.threadName or ""


class RelativeCreatedColumn(itemmodels.ColumnItem):
    name = "Relative created"

    def get_data(self, item: logging.LogRecord, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return str(item.relativeCreated)


class NameColumn(itemmodels.ColumnItem):
    name = "Name"

    def get_data(self, item: logging.LogRecord, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return item.name


class PathNameColumn(itemmodels.ColumnItem):
    name = "Path name"

    def get_data(self, item: logging.LogRecord, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return item.pathname


class MessageColumn(itemmodels.ColumnItem):
    name = "Message"

    def get_data(self, item: logging.LogRecord, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return (
                    traceback.format_exc()
                    if isinstance(item.msg, Exception)
                    else item.msg % item.args
                )


class LogRecordModel(itemmodels.ColumnTableModel):
    COLUMNS = [
        LevelNameColumn,
        FileNameColumn,
        FunctionNameColumn,
        LineNoColumn,
        ModuleColumn,
        CreatedColumn,
        ProcessColumn,
        ThreadColumn,
        ProcessNameColumn,
        ThreadNameColumn,
        RelativeCreatedColumn,
        NameColumn,
        PathNameColumn,
        MessageColumn,
    ]

    def __init__(self, logger, level=logging.DEBUG, *args, **kwargs):
        super().__init__(items=[], columns=self.COLUMNS, **kwargs)
        self.handler = signallogger.SignalLogger()
        self.handler.signals.log_record.connect(self.add)
        core.CoreApplication.call_on_exit(lambda: logger.removeHandler(self.handler))
        self.handler.setLevel(level)
        logger.addHandler(self.handler)

    @classmethod
    def supports(cls, instance) -> bool:
        match instance:
            case (logging.LogRecord(), *_):
                return True
            case _:
                return False


if __name__ == "__main__":
    from prettyqt import debugging
    from prettyqt.qt import QtGui

    logger = logging.getLogger()

    app = widgets.app()
    with app.debug_mode():
        widget = widgets.TableView()
        model = LogRecordModel(logger, parent=widget)

        def color_log(x):
            # print("fsfksj", x)
            match x:
                case "DEBUG":
                    return QtGui.QColor("lightblue")
                case "INFO":
                    return QtGui.QColor("lightgreen")
                case "WARNING":
                    return QtGui.QColor("orange")
                case "ERROR":
                    return QtGui.QColor("red")

        widget.set_model(model)
        widget.proxifier[0].modify(color_log, role=constants.BACKGROUND_ROLE)
        w = widgets.Widget()
        w.set_layout("vertical")
        widget.set_selection_behavior("rows")
        stalker = debugging.Stalker(widget)

        def raise_exc():
            try:
                raise Exception("test")
            except Exception as e:
                logger.exception(e)

        w.box += widgets.PushButton("Raise", clicked=raise_exc)
        w.box += widgets.PushButton("Debug", clicked=lambda: logger.debug("Debug"))
        w.box += widgets.PushButton("Info", clicked=lambda: logger.info("Info"))
        w.box += widgets.PushButton("Warning", clicked=lambda: logger.warning("Warning"))
        w.box += widgets.PushButton("Critical", clicked=lambda: logger.critical("Critic"))
        w.box += widget
        w.show()
        widget.show()
        app.exec()
