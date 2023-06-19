from __future__ import annotations

import logging
import traceback

from prettyqt import core, custom_models, widgets
from prettyqt.utils import signallogger


logger = logging.getLogger(__name__)


# class LevelNameColumn(custom_models.ColumnItem):
#     name = "Level"

#     def get_data(self, item, role):
#         match role:
#             case constants.DISPLAY_ROLE:
#                 return item.levelname


# class FileNameColumn(custom_models.ColumnItem):
#     name = "File name"

#     def get_data(self, item, role):
#         match role:
#             case constants.DISPLAY_ROLE:
#                 return item.filename


# class FunctionNameColumn(custom_models.ColumnItem):
#     name = "Function name"

#     def get_data(self, item, role):
#         match role:
#             case constants.DISPLAY_ROLE:
#                 return item.funcName


# class FunctionNameColumn(custom_models.ColumnItem):
#     name = "Function name"

#     def get_data(self, item, role):
#         match role:
#             case constants.DISPLAY_ROLE:
#                 return item.funcName


# class ModuleColumn(custom_models.ColumnItem):
#     name = "Module"

#     def get_data(self, item, role):
#         match role:
#             case constants.DISPLAY_ROLE:
#                 return item.module


# class CreatedColumn(custom_models.ColumnItem):
#     name = "Created"

#     def get_data(self, item, role):
#         match role:
#             case constants.DISPLAY_ROLE:
#                 return str(core.DateTime.from_seconds(item.created))
#             case constants.USER_ROLE:
#                 return core.DateTime.from_seconds(item.created)


# class ProcessColumn(custom_models.ColumnItem):
#     name = "Process"

#     def get_data(self, item, role):
#         match role:
#             case constants.DISPLAY_ROLE:
#                 return str(item.process)
#             case constants.USER_ROLE:
#                 return item.process


# class ThreadColumn(custom_models.ColumnItem):
#     name = "Thread"

#     def get_data(self, item, role):
#         match role:
#             case constants.DISPLAY_ROLE:
#                 return str(x.thread)
#             case constants.USER_ROLE:
#                 return x.thread


# class ProcessNameColumn(custom_models.ColumnItem):
#     name = "Process name"

#     def get_data(self, item, role):
#         match role:
#             case constants.DISPLAY_ROLE:
#                 return item.processName or ""


# class ThreadNameColumn(custom_models.ColumnItem):
#     name = "Thread name"

#     def get_data(self, item, role):
#         match role:
#             case constants.DISPLAY_ROLE:
#                 return item.threadName or ""


# class RelativeCreatedColumn(custom_models.ColumnItem):
#     name = "Relative created"

#     def get_data(self, item, role):
#         match role:
#             case constants.DISPLAY_ROLE:
#                 return str(item.relativeCreated)


# class NameColumn(custom_models.ColumnItem):
#     name = "Name"

#     def get_data(self, item, role):
#         match role:
#             case constants.DISPLAY_ROLE:
#                 return item.name


# class PathNameColumn(custom_models.ColumnItem):
#     name = "Path name"

#     def get_data(self, item, role):
#         match role:
#             case constants.DISPLAY_ROLE:
#                 return x.pathname


# class MessageColumn(custom_models.ColumnItem):
#     name = "Message"

#     def get_data(self, item, role):
#         match role:
#             case constants.DISPLAY_ROLE:
#                 return (
#                     traceback.format_exc()
#                     if isinstance(item.msg, Exception)
#                     else item.msg % item.args
#                 )


COL_LEVEL_NAME = custom_models.ColumnItem(
    name="Level.",
    doc="Level.",
    label=lambda x: x.levelname,
)
COL_FILENAME = custom_models.ColumnItem(
    name="Filename",
    doc="Filename.",
    label=lambda x: x.filename,
)
COL_FUNCTION_NAME = custom_models.ColumnItem(
    name="Function name",
    doc="Function name.",
    label=lambda x: x.funcName,
)
COL_MODULE = custom_models.ColumnItem(
    name="Module",
    doc="Module",
    label=lambda x: x.module,
)
COL_CREATED = custom_models.ColumnItem(
    name="Created",
    doc="Created.",
    label=lambda x: str(core.DateTime.from_seconds(x.created)),
)
COL_LINE_NO = custom_models.ColumnItem(
    name="Line no",
    doc="Line number.",
    label=lambda x: str(x.lineno),
)
# COL_MSECS = custom_models.ColumnItem(
#     name="Msecs",
#     doc="Millisecons",
#     label=lambda x: str(x.msecs),
# )
COL_PROCESS = custom_models.ColumnItem(
    name="Process",
    doc="Process",
    label=lambda x: str(x.process),
)
COL_THREAD = custom_models.ColumnItem(
    name="Thread",
    doc="Thread.",
    label=lambda x: str(x.thread),
)
COL_THREAD_NAME = custom_models.ColumnItem(
    name="Thread name",
    doc="Thread name.",
    label=lambda x: x.threadName or "",
)
COL_PROCESS_NAME = custom_models.ColumnItem(
    name="Process name",
    doc="Process name.",
    label=lambda x: x.processName or "",
)
COL_RELATIVE_CREATED = custom_models.ColumnItem(
    name="Relative created",
    doc="Relative created.",
    label=lambda x: str(x.relativeCreated),
)
COL_NAME = custom_models.ColumnItem(
    name="Name",
    doc="Name",
    label=lambda x: x.name,
)
COL_PATH_NAME = custom_models.ColumnItem(
    name="Path Name",
    doc="Path name",
    label=lambda x: x.pathname,
)

COL_MESSAGE = custom_models.ColumnItem(
    name="Message",
    doc="Message",
    label=lambda x: traceback.format_exc()
    if isinstance(x.msg, Exception)
    else x.msg % x.args,
)


COLUMNS = [
    COL_CREATED,
    COL_LEVEL_NAME,
    COL_MESSAGE,
    COL_FILENAME,
    COL_FUNCTION_NAME,
    COL_MODULE,
    COL_LINE_NO,
    # COL_MSECS,
    COL_PROCESS,
    COL_THREAD,
    COL_THREAD_NAME,
    COL_PROCESS_NAME,
    # COL_RELATIVE_CREATED,
    COL_NAME,
    COL_PATH_NAME,
]


class LogRecordModel(custom_models.ColumnTableModel):
    def __init__(self, logger, level=logging.DEBUG, *args, **kwargs):
        super().__init__(items=[], columns=COLUMNS, **kwargs)
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
    from prettyqt import constants, debugging
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
        widget.proxifier[1].modify(color_log, role=constants.BACKGROUND_ROLE)
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
        app.main_loop()
