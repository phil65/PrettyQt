from __future__ import annotations

import logging

import numpy as np
import pandas as pd

from prettyqt import constants, core, custom_models
from prettyqt.utils import helpers

logger = logging.getLogger(__name__)


class PandasCategoryListModel(custom_models.ModelMixin, core.AbstractTableModel):
    MIME_TYPE = "mime_categories"
    HEADER = ["Name", "Code"]

    def __init__(self, df: pd.DataFrame | None = None, col=None, parent=None):
        super().__init__(parent=parent)
        self.df = df
        self.col = col

    @property
    def series(self):
        return self.df[self.col]

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        if role == constants.EDIT_ROLE:
            if index.column() == 0:
                if value in self.series.cat.categories:
                    logger.error("Error: Category names must be unique.")
                    return False
                rename_dct = {index.data(constants.NAME_ROLE): value}
                with self.change_layout():
                    self.series = self.series.rename_categories(new_categories=rename_dct)
                return True
        return False

    def flags(self, index):
        if not index.isValid():
            return constants.DROP_ENABLED
        return self.DEFAULT_FLAGS | constants.IS_EDITABLE

    def data(self, index, role=constants.DISPLAY_ROLE):
        if not index.isValid():
            return None
        # if role == constants.DECORATION_ROLE:
        #     if index.column() == 0:
        #         return iconprovider.get_icon(iconnames.CATEGORY, as_qicon=True)
        cat_name = self.series.cat.categories[index.row()]
        match role, index.column():
            case constants.DISPLAY_ROLE | constants.EDIT_ROLE, 0:
                return helpers.format_name(cat_name)
            case constants.DISPLAY_ROLE | constants.EDIT_ROLE, 1:
                return str(self.series.cat.codes[index.row()])
            case constants.NAME_ROLE, _:
                if isinstance(cat_name, np.number):
                    return cat_name.item()
                return cat_name
            case constants.TOOLTIP_ROLE, _:
                num_items = len(self.df[self.series == cat_name])
                return f"<b>{cat_name}</b><br>Items: {num_items}"
            case constants.USER_ROLE, _:
                self.df = self.df[self.series == cat_name]
                return self.df

    def rowCount(self, parent=None):
        if not self.col or not hasattr(self.series, "cat"):
            return 0
        return len(self.series.cat.categories)

    def mimeData(self, indexes):
        mime_data = core.MimeData()
        data = [i.row() for i in indexes if i.column() == 0]
        mime_data.set_json_data(self.MIME_TYPE, data)
        return mime_data

    def mimeTypes(self):
        return [self.MIME_TYPE]

    def dropMimeData(self, mime_data, action, row, column, parent_index):
        if parent_index.isValid():
            return False

        if mime_data.hasFormat(self.MIME_TYPE):
            indexes = mime_data.get_json_data(self.MIME_TYPE)
            cats = self.series.cat.categories.tolist()
            cats = helpers.move_in_list(cats, indexes, row)
            self.reorder_categories(cats)
            return False

    def sort(self, ncol, order):
        if ncol != 0:
            return None
        is_ascending = order == constants.ASCENDING
        order = sorted(self.series.cat.categories, reverse=is_ascending)
        self.reorder_categories(order)

    def reorder_categories(self, order):
        with self.change_layout():
            self.series = self.series.cat.reorder_categories(new_categories=order)

    def add_category(self, new_categories):
        with self.append_rows(1):
            self.series = self.series.cat.add_categories(new_categories=new_categories)

    def toggle_ordered(self):
        with self.change_layout():
            if self.series.cat.ordered:
                self.series = self.series.cat.set_unordered()
            else:
                self.series = self.series.cat.set_ordered()

    def remove_unused(self):
        with self.change_layout():
            self.series = self.series.cat.remove_unused()


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    # Prepare data
    df = pd.DataFrame({"A": ["a", "b", "c", "a"]})

    df["B"] = df["A"].astype("category")
    model = PandasCategoryListModel(df, "B")
    tableview = widgets.TreeView()
    tableview.setup_dragdrop_move()
    # tableview.set_delegate("variant")
    tableview.set_model(model)

    tableview.show()
    app.main_loop()
