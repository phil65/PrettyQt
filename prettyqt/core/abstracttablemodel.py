from __future__ import annotations

from prettyqt import constants, core


class AbstractTableModelMixin(core.AbstractItemModelMixin):
    DEFAULT_FLAGS = (
        constants.DRAG_ENABLED
        | constants.IS_ENABLED
        | constants.IS_SELECTABLE
        | constants.NO_CHILDREN
    )

    def get_table_data(
        self,
        include_index: bool = False,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
        x_range: slice | int | None = None,
        y_range: slice | int | None = None,
    ):
        match x_range:
            case None:
                colrange = range(self.columnCount())
            case slice():
                stop = x_range.stop or self.columnCount()
                colrange = range(x_range.start or 0, stop, x_range.step or 1)
            case int():
                colrange = range(x_range, x_range + 1)

        match y_range:
            case None:
                rowrange = range(self.rowCount())
            case slice():
                stop = y_range.stop or self.rowCount()
                rowrange = range(y_range.start or 0, stop, y_range.step or 1)
            case int():
                rowrange = range(y_range, y_range + 1)

        data = [[self.index(i, j).data(role) for j in colrange] for i in rowrange]
        h_header = [self.headerData(i, constants.HORIZONTAL) for i in colrange]
        v_header = (
            [self.headerData(i, constants.VERTICAL) for i in rowrange]
            if include_index
            else None
        )
        return data, h_header, v_header

    def to_dataframe(self, **kwargs):
        import pandas as pd

        data, h_header, v_header = self.get_table_data(**kwargs)
        return pd.DataFrame(data=data, columns=h_header, index=v_header)

    def to_markdown(self, use_checkstate_role: bool = True, **kwargs):
        data, h_header, v_header = self.get_table_data(**kwargs)
        if use_checkstate_role:
            kwargs["role"] = constants.CHECKSTATE_ROLE
            check_data, _, __ = self.get_table_data(**kwargs)
            for i, row in enumerate(data):
                for j, _column in enumerate(row):
                    if check_data[i][j]:
                        data[i][j] = "x"

        lines = [f"|{'|'.join(h_header)}|", f"|{'--|--'.join('' for _ in h_header)}|"]
        for row in data:
            sections = [str(i) if i else "" for i in row]
            lines.append(f"|{'|'.join(sections)}|")
        return "\n".join(lines)


class AbstractTableModel(AbstractTableModelMixin, core.QAbstractTableModel):
    pass


if __name__ == "__main__":
    from prettyqt import itemmodels, widgets

    app = widgets.app()
    model = itemmodels.QObjectPropertiesModel(app)
    table = widgets.TableView()
    table.set_model(model)
    print(model.to_markdown())
