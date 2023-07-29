from __future__ import annotations

from collections.abc import Sequence
import inspect
import logging

from prettyqt import constants, core, gui, itemmodels


logger = logging.getLogger(__name__)

SOURCE_FONT = gui.Font.mono(as_qt=True)


class FrameInfoModel(itemmodels.ListMixin, core.AbstractTableModel):
    """Model to display a list of inspect.Frameinfos / inspect.Tracebacks."""

    HEADER = ["Filename", "Line number", "Function", "Code context", "Index", "Positions"]
    SUPPORTS = Sequence[inspect.FrameInfo | inspect.Traceback]

    @classmethod
    def supports(cls, instance) -> bool:
        match instance:
            case (inspect.FrameInfo(), *_) | (inspect.Traceback(), *_):
                return True
            case _:
                return False

    def columnCount(self, parent=None) -> int:
        return len(self.HEADER)

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> str | None:
        match orientation, role:
            case constants.HORIZONTAL, constants.DISPLAY_ROLE:
                return self.HEADER[section]
            case constants.VERTICAL, constants.DISPLAY_ROLE:
                return str(section)

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if not index.isValid():
            return None
        field = self.items[index.row()]
        match role, index.column():
            case constants.DISPLAY_ROLE, 0:
                return field.filename
            case constants.DISPLAY_ROLE, 1:
                return field.lineno
            case constants.DISPLAY_ROLE, 2:
                return field.function
            case constants.DISPLAY_ROLE, 3:
                lines = []
                pretty = ""
                for line in field.code_context:
                    while line.startswith(" "):
                        pretty += "·"
                        line = line[1:]
                    pretty += line
                    lines.append(pretty)
                return "\n".join(lines)
            case constants.FONT_ROLE, 3:
                return SOURCE_FONT
            case constants.DISPLAY_ROLE, 4:
                return field.index
            case constants.DISPLAY_ROLE, 5:
                p = field.positions
                return f"{p.lineno} - {p.end_lineno}, {p.col_offset} {p.end_col_offset}"
            case constants.ALIGNMENT_ROLE, _:
                return constants.ALIGN_CENTER_LEFT


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    view = widgets.TableView()
    view.set_word_wrap(True)
    view.set_icon("mdi.folder")
    with app.debug_mode():
        stack = inspect.stack()
        model = FrameInfoModel(items=stack)
        view.set_model(model)
        view.set_selection_behavior("rows")
        view.set_edit_triggers("all")
        view.set_delegate("editor", column=1)
        view.show()
        view.resize(500, 300)
        app.exec()
