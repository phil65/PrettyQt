from __future__ import annotations

import logging
import enum

import numpy as np
import pandas as pd

from prettyqt import constants, core, custom_models
from prettyqt.utils import helpers

logger = logging.getLogger(__name__)


class PandasColumnListModel(custom_models.ModelMixin, core.AbstractTableModel):
    HEADER = ["Name", "Type", "Size"]
    MIME_TYPE = "mime_columns"
    content_type = "features"

    class Roles(enum.IntEnum):
        """Role names."""

        DTypeRole = constants.USER_ROLE + 4555
        ColumnNameRole = constants.USER_ROLE + 4556

    def __init__(self, df: pd.DataFrame = None, **kwargs):
        super().__init__(**kwargs)
        self.df = df

    def mimeData(self, indexes):
        mime_data = core.MimeData()
        data = [i.row() for i in indexes if i.column() == 0]
        mime_data.set_json_data(self.MIME_TYPE, data)
        return mime_data

    def dropMimeData(self, mime_data, action, row, column, parent_index):
        if parent_index.isValid():
            # Since we only drop in between items, parent_index must be invalid
            return False
        if mime_data.hasFormat(self.MIME_TYPE):
            data = mime_data.get_json_data(self.MIME_TYPE)
            cols = self.df.columns.tolist()
            cols = helpers.move_in_list(cols, data, row)
            with self.change_layout():
                self.df = self.df[cols]
            self.update_all()
            return False

        elif mime_data.hasFormat("mime_indexes"):
            data = mime_data.get_json_data("mime_indexes")
            names = list(self.df.index.names)
            with self.reset_model():
                self.df = self.df.reset_index(level=[names[i] for i in data])
            self.update_all()
            return False

    def mimeTypes(self):
        return [self.MIME_TYPE]

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        match role:
            case constants.EDIT_ROLE:
                colname = index.data(constants.NAME_ROLE)
                if value not in self.df.columns:
                    self.df = self.df.rename(mapper={colname: value}, axis="columns")
                    self.update_all()
                    return True

            case constants.USER_ROLE:
                name = self.data_by_index(index).name
                self.df = self.df.assign(**{name: value})
                self.update_all()
                return True

            case self.Roles.DTypeRole:
                name = index.data(constants.NAME_ROLE)
                try:
                    self.df = self.df.as_type(dtype=value)
                except TypeError as e:
                    logger.exception(e)
                else:
                    self.update_all()
                return True

        return False

    def flags(self, index):
        if not index.isValid():
            return constants.DROP_ENABLED
        if index.column() in [0, 1]:
            return self.DEFAULT_FLAGS | constants.IS_EDITABLE
        return self.DEFAULT_FLAGS

    def removeRows(self, row, count, parent):
        colnames = self.df.columns[row : row + count].tolist()
        with self.remove_rows(row, row + count, parent):
            self.df = self.df.drop(labels=colnames, axis=1, errors="ignore")
        self.update_all()
        return True

    def data(self, index, role=constants.DISPLAY_ROLE):
        if not index.isValid():
            return None

        match role:
            # case constants.DECORATION_ROLE:
            #     if index.column() == 0:
            #         dtype = self.data_by_index(index).dtype
            #         return icons.icon_for_dtype(dtype)

            case constants.DISPLAY_ROLE | constants.EDIT_ROLE:
                match index.column():
                    case 0:
                        return str(self.data_by_index(index).name)
                    case 1:
                        return str(self.data_by_index(index).dtype)
                    case 2:
                        nbytes = self.data_by_index(index).nbytes
                        locale = core.Locale()
                        return locale.get_formatted_data_size(nbytes)

            case self.Roles.DTypeRole:
                return self.data_by_index(index).dtype

            case constants.USER_ROLE:
                return self.data_by_index(index)

            case self.Roles.ColumnNameRole:
                return self.data_by_index(index).name

    def rowCount(self, parent=None):
        return len(self.df.columns)

    def sort(self, ncol, order):
        is_ascending = order == constants.ASCENDING
        match ncol:
            case 0:
                order = sorted(self.df.columns, reverse=is_ascending)

            case 1:
                maps = [(col, str(self.df[col].dtype)) for col in self.df.columns]
                maps.sort(key=lambda x: x[1], reverse=is_ascending)
                order = [c[0] for c in maps]

            case 2:
                maps = [(col, str(self.df[col].nbytes)) for col in self.df.columns]
                maps.sort(key=lambda x: x[1], reverse=is_ascending)
                order = [c[0] for c in maps]
            case _:
                return

        with self.change_layout():
            self.df = self.df.reindex(labels=order, axis="columns")

    def data_by_index(self, index: core.ModelIndex):
        return self.df.iloc[:, index.row()]

    def add_feature(self, series):
        with self.append_rows(1):
            self.df = self.df.assign(**{series.name: series})


def label_for_index(index: pd.Index) -> str:
    match index:
        case pd.RangeIndex():
            return "Range"
        case pd.DatetimeIndex():
            return "Datetime"
        case pd.CategoricalIndex():
            return "Categorical"
        case pd.IntervalIndex():
            return "Interval"
        case pd.TimedeltaIndex():
            return "Timedelta"
        case pd.MultiIndex():
            return "Multi-index"
        case pd.PeriodIndex():
            return "Period"
        case _:
            return "Regular"


class PandasIndexListModel(custom_models.ModelMixin, core.AbstractTableModel):
    HEADER = ["Name", "Index type", "Monotonic"]
    MIME_TYPE = "mime_indexes"

    def __init__(self, ds: pd.DataFrame | None = None, **kwargs):
        super().__init__(**kwargs)
        self.df = ds

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        match role:
            case constants.EDIT_ROLE:
                if index.column() == 0:
                    level = (
                        index.row() if isinstance(self.df.index, pd.MultiIndex) else None
                    )
                    self.df.index = self.df.index.set_names(names=value, level=level)
                    return True
            case constants.USER_ROLE:
                if not isinstance(self.df.index, pd.MultiIndex):
                    with self.change_layout():
                        self.df.index = value
                    return True
            case self.DTYPE_ROLE:
                try:
                    with self.change_layout():
                        self.df.index = self.df.index.astype(value)
                    return True
                except TypeError as e:
                    logger.exception(e)
                    return False

    def removeRows(self, row, count, parent):
        with self.remove_rows(row, row + count, parent):
            self.df = self.df.drop(labels=self.df.columns[row : row + count], axis=1)
        return True

    def flags(self, index):
        if not index.isValid():
            return constants.DROP_ENABLED
        is_range = self.df.index.name is None and isinstance(self.df.index, pd.RangeIndex)
        match index.column(), is_range:
            case 0, True:
                # do not allow moving the "default" RangeIndex.
                return (
                    constants.IS_ENABLED | constants.IS_SELECTABLE | constants.IS_EDITABLE
                )
            case _, True:
                return constants.IS_ENABLED | constants.IS_SELECTABLE
            case 0 | 1, False:
                return self.DEFAULT_FLAGS | constants.IS_EDITABLE
            case _, False:
                return self.DEFAULT_FLAGS

    def data(self, index, role=constants.DISPLAY_ROLE):
        if not index.isValid():
            return None
        match role, index.column():
            # case constants.DECORATION_ROLE, 0:
            #     index = self.get_index(index.row())
            #     return icons.icon_for_index(index)

            case constants.TOOLTIP_ROLE, _:
                index = self.get_index(index.row())
                return (
                    f"<b>{index.name}</b><br>"
                    f"{'Contains NaNs'}: {index.hasnans}<br>"
                    # f"{_('Monotonic')}: {index.is_monotonic}"
                )

            case constants.DISPLAY_ROLE | constants.EDIT_ROLE, 0:
                index_name = self.df.index.names[index.row()]
                return index_name or "[Unnamed]"

            case constants.DISPLAY_ROLE | constants.EDIT_ROLE, 1:
                return label_for_index(self.get_index(index.row()))

            case constants.DISPLAY_ROLE | constants.EDIT_ROLE, 2:
                index = self.get_index(index.row())
                if index.is_monotonic_increasing:
                    return "Increasing"
                elif index.is_monotonic_decreasing:
                    return "Decreasing"

            case constants.USER_ROLE, _:
                name = self.df.index.names[index.row()]
                return self.df.index.get_level_values(name)

            case constants.NAME_ROLE, _:
                return self.df.index.names[index.row()]

            case self.DTYPE_ROLE, _:
                return self.get_index(index.row()).dtype

    def rowCount(self, parent=None):
        return self.df.index.nlevels

    def mimeData(self, indexes):
        mime_data = core.MimeData()
        data = [i.row() for i in indexes if i.column() == 0]
        mime_data.set_json_data(self.MIME_TYPE, data)
        return mime_data

    def dropMimeData(self, mime_data, action, row, column, parent_index):
        if parent_index.isValid():
            return False

        if mime_data.hasFormat(self.MIME_TYPE):
            data = mime_data.get_json_data(self.MIME_TYPE)
            names = list(self.df.index.names)
            names = helpers.move_in_list(names, data, row)
            with self.change_layout():
                self.df = self.df.reorder_levels(order=names)
        elif mime_data.hasFormat("mime_columns"):
            data = mime_data.get_json_data("mime_columns")
            cols = self.df.columns.tolist()
            to_append = [cols[i] for i in data]
            # TODO: make sure drop offset is taken into account
            with self.reset_model():
                self.df = self.df.set_index(keys=to_append, append=True)
        return False

    def mimeTypes(self):
        return [self.MIME_TYPE]

    def get_index(self, row=None):
        idx = self.df.index
        # using get_level_values() is too slow for large datasets with multiindex
        return idx.levels[row] if isinstance(idx, pd.MultiIndex) else idx

    def to_datetime(self, level=None, fmt: str | None = None):
        with self.change_layout():
            self.df.index = self.df.index.pt.to_datetime(level=level, fmt=fmt)

    def filter_range(self, start: int, end: int):
        with self.change_layout():
            self.df = self.df.iloc[start:end]
        return True


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    # Prepare data
    tuples = [
        ("bar", "one", "q"),
        ("bar", "two", "q"),
        ("baz", "one", "q"),
        ("baz", "two", "q"),
        ("foo", "one", "q"),
        ("foo", "two", "q"),
        ("qux", "one", "q"),
        ("qux", "two", "q"),
    ]
    index = pd.MultiIndex.from_tuples(tuples, names=["first", "second", "third"])
    df = pd.DataFrame(np.random.randn(6, 6), index=index[:6], columns=index[:6])
    model = PandasColumnListModel(df)
    tableview = widgets.TreeView()
    tableview.setup_dragdrop_move()
    tableview.set_delegate("variant")
    tableview.set_model(model)

    tableview.show()
    app.main_loop()
