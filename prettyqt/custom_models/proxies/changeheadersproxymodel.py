from __future__ import annotations

from typing import Any

from prettyqt import constants, core


class ChangeHeadersProxyModel(core.IdentityProxyModel):
    ID = "change_headers"

    def __init__(
        self,
        header: list[Any] | dict[int, Any],
        orientation: constants.Orientation
        | constants.OrientationStr = constants.HORIZONTAL,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._orientation = constants.ORIENTATION.get_enum_value(orientation)
        self._header = header
        self._role = role

    def setSourceModel(self, model):
        header_len = (
            model.columnCount()
            if self._orientation == constants.HORIZONTAL
            else model.rowCount()
        )
        if isinstance(self._header, list) and len(self._header) != header_len:
            raise ValueError("list needs to be same list as header")
        super().setSourceModel(model)

    def get_header(self) -> list[int]:
        return self._header

    def set_header(
        self,
        header: list[str] | dict[int, str],
        orientation: constants.Orientation | constants.OrientationStr,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        with self.reset_model():
            self._header = header
            self._orientation = constants.ORIENTATION.get_enum_value(orientation)
            self._role = role

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole,
    ):
        if orientation == self._orientation and role == self._role:
            if isinstance(self._header, dict) and section in self._header:
                return self._header[section]
            elif isinstance(self._header, list):
                return self._header[section]
        return self.sourceModel().headerData(section, orientation, role)

    header = core.Property(object, get_header, set_header)


if __name__ == "__main__":
    from prettyqt import gui, widgets

    data = dict(
        a=["abcdedf", "abcdedf", "abcdedf", "abcdedf", "abcdedf", "abcdedfaa"],
        b=[10000000, 2, 3, 4, 5, 6],
        c=[1, 2, 3, 4, 5, 6],
        d=[100000000, 2, 3, 4, 5, 6],
        e=[1000000, 2, 3, 4, 5, 6],
    )
    source_model = gui.StandardItemModel.from_dict(data)
    app = widgets.app()
    table = widgets.TableView()
    model = ChangeHeadersProxyModel(
        {0: constants.ALIGN_RIGHT}, role=constants.ALIGNMENT_ROLE, parent=table
    )
    model.setSourceModel(source_model)
    table.set_model(model)
    table.show()
    with app.debug_mode():
        app.exec()
