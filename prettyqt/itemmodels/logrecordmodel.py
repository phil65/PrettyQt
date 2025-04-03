from __future__ import annotations

from collections.abc import Sequence
import datetime
import logging
import traceback
from typing import ClassVar

from prettyqt import constants, core, itemmodels


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
                return dt.toString(self.display_format)
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
                return str(datetime.timedelta(milliseconds=item.relativeCreated))


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
    """Model to display a list of logging.LogRecords."""

    COLUMNS: ClassVar = [
        LevelNameColumn,
        FileNameColumn,
        FunctionNameColumn,
        LineNoColumn,
        MessageColumn,
        ModuleColumn,
        CreatedColumn,
        ProcessColumn,
        ThreadColumn,
        ProcessNameColumn,
        ThreadNameColumn,
        RelativeCreatedColumn,
        NameColumn,
        PathNameColumn,
    ]
    SUPPORTS = Sequence[logging.LogRecord]

    def __init__(self, **kwargs):
        super().__init__(items=[], columns=self.COLUMNS, **kwargs)

    @classmethod
    def supports(cls, instance) -> bool:
        match instance:
            case (logging.LogRecord(), *_):
                return True
            case _:
                return False


if __name__ == "__main__":
    from prettyqt import debugging, widgets

    logger = logging.getLogger()

    app = widgets.app()
    with app.debug_mode():
        with debugging.Stalker(app) as stalker:
            stalker.show()
        app.exec()
        # def raise_exc():
        #     try:
        #         raise Exception("test")
        #     except Exception as e:
        #         logger.exception(e)
