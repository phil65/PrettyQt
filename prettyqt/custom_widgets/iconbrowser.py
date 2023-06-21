from __future__ import annotations

import sys

from prettyqt import constants, core, custom_models, iconprovider, widgets
from prettyqt.eventfilters import listviewgridresizeeventfilter
from prettyqt.utils import colors, datatypes


# TODO: Set icon colour and copy code with color kwarg

ALL_COLLECTIONS = "All"


class IconBrowser(widgets.MainWindow):
    """A small browser window that allows the user to search through all icons.

    You can also copy the name and python code for the currently selected icon.
    """

    def __init__(self):
        super().__init__()
        self.setMinimumSize(500, 500)
        self.set_title("Icon Browser")
        font_maps = {k: v.charmap for k, v in iconprovider._instance().fonts.items()}
        icon_names = [
            f"{font_collection}.{icon_name}"
            for font_collection, font_data in font_maps.items()
            for icon_name in font_data
        ]
        model = IconModel(icon_color="text_role")
        model.setStringList(sorted(icon_names))

        self._proxy_model = custom_models.FuzzyFilterProxyModel()
        self._proxy_model.setSourceModel(model)
        self._proxy_model.set_filter_case_sensitive(True)
        self._proxy_model.set_match_color(None)

        self._listview = widgets.ListView(
            self,
            uniform_item_sizes=True,
            view_mode="icon",
            context_menu_policy="custom",
            double_clicked=self._copy_icon_text,
            vertical_scroll_bar_policy="always_on",
        )
        eventfilter = listviewgridresizeeventfilter.ListViewGridResizeEventFilter(
            parent=self._listview
        )
        self._listview.installEventFilter(eventfilter)
        self._listview.set_model(self._proxy_model)

        self._lineedit = widgets.LineEdit(
            parent=self, text_changed=self._trigger_instant_update
        )

        self._combobox = widgets.ComboBox(
            parent=self,
            minimum_width=75,
            current_index_changed=self._trigger_instant_update,
        )
        self._combobox.addItems([ALL_COLLECTIONS, *sorted(font_maps.keys())])

        search_bar_frame = widgets.Frame(self)
        layout = search_bar_frame.set_layout("horizontal", margin=0)
        layout.add(self._combobox)
        layout.add(self._lineedit)

        self._copy_button = widgets.PushButton("Copy Name", clicked=self._copy_icon_text)
        frame = widgets.Frame(self)
        layout = frame.set_layout("vertical")
        layout.add(search_bar_frame)
        layout.add(self._listview)
        layout.add(self._copy_button)
        self.setCentralWidget(frame)
        self.add_shortcut("return", self._copy_icon_text)
        self._lineedit.setFocus()
        self.position_on("screen")

    def _trigger_instant_update(self):
        """Stop timer used for committing search term and update proxy model instantly."""
        self._proxy_model.set_search_term(self._lineedit.text())

    def _copy_icon_text(self):
        """Copy the name of the currently selected icon to the clipboard."""
        if indexes := self._listview.selectedIndexes():
            widgets.Application.copy_to_clipboard(indexes[0].data())


class IconModel(core.StringListModel):
    def __init__(self, icon_color: datatypes.ColorType):
        super().__init__()
        self._icon_color = colors.get_color(icon_color).as_qt()

    def flags(self, index: core.ModelIndex):
        return constants.IS_ENABLED | constants.IS_SELECTABLE  # type: ignore

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if role == constants.DECORATION_ROLE:
            icon_string = self.data(index, role=constants.DISPLAY_ROLE)
            return iconprovider._icon(icon_string, color=self._icon_color)
        return super().data(index, role)


def run():
    app = widgets.app()
    browser = IconBrowser()
    browser.show()
    sys.exit(app.main_loop())


if __name__ == "__main__":
    run()
