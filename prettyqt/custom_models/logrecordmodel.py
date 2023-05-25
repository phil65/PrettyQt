from __future__ import annotations

import logging
import traceback

from prettyqt import core, custom_models, widgets
from prettyqt.utils import signallogger


logger = logging.getLogger(__name__)


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
        super().__init__(items=[], columns=COLUMNS)
        self.handler = signallogger.SignalLogger()
        self.handler.signals.log_record.connect(self.add)
        core.CoreApplication.call_on_exit(lambda: logger.removeHandler(self.handler))
        self.handler.setLevel(level)
        logger.addHandler(self.handler)


if __name__ == "__main__":
    from prettyqt.utils import debugging

    logger = logging.getLogger()

    app = widgets.app()
    widget = widgets.TableView()
    model = LogRecordModel(logger, parent=widget)
    w = widgets.Widget()
    w.set_layout("vertical")
    widget.set_model(model)
    widget.set_selection_behavior("rows")
    stalker = debugging.Stalker(widget)

    def raise_exc():
        try:
            raise Exception("test")
        except Exception as e:
            logger.exception(e)

    w.box.add(widgets.PushButton("Raise", clicked=raise_exc))
    w.box.add(widgets.PushButton("Debug", clicked=lambda: logger.debug("Debug")))
    w.box.add(widgets.PushButton("Info", clicked=lambda: logger.info("Info")))
    w.box.add(widgets.PushButton("Warning", clicked=lambda: logger.warning("Warning")))
    w.box.add(widgets.PushButton("Critical", clicked=lambda: logger.critical("Critical")))
    w.box.add(widget)
    w.show()
    with app.debug_mode():
        app.main_loop()
