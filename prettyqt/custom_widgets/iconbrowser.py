from __future__ import annotations

import sys

from prettyqt import constants, core, gui, iconprovider, widgets
from prettyqt.qt import QtGui, QtWidgets


# TODO: Set icon colour and copy code with color kwarg

AUTO_SEARCH_TIMEOUT = 500
ALL_COLLECTIONS = "All"


class IconBrowser(widgets.MainWindow):
    """A small browser window that allows the user to search through all icons.

    You can also copy the name and python code for the currently selected icon.
    """

    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 300)
        self.set_title("Icon Browser")
        from prettyqt import iconprovider

        iconprovider._instance()
        font_maps = iconprovider._instance().charmap

        icon_names = [
            f"{font_collection}.{icon_name}"
            for font_collection, font_data in font_maps.items()
            for icon_name in font_data
        ]
        self._filter_timer = core.Timer(self)
        self._filter_timer.setSingleShot(True)
        self._filter_timer.setInterval(AUTO_SEARCH_TIMEOUT)
        self._filter_timer.timeout.connect(self._update_filter)

        model = IconModel(self.get_palette().get_color("text"))
        model.setStringList(sorted(icon_names))

        self._proxy_model = core.SortFilterProxyModel()
        self._proxy_model.setSourceModel(model)
        self._proxy_model.set_filter_case_sensitive(True)

        self._listview = IconListView(self)
        self._listview.setUniformItemSizes(True)
        self._listview.set_view_mode("icon")
        self._listview.set_model(self._proxy_model)
        self._listview.set_contextmenu_policy("custom")
        self._listview.doubleClicked.connect(self._copy_icon_text)

        self._lineedit = widgets.LineEdit(parent=self)
        self._lineedit.textChanged.connect(self._filter_timer.restart)
        self._lineedit.returnPressed.connect(self._trigger_instant_update)

        self._combobox = widgets.ComboBox(parent=self)
        self._combobox.setMinimumWidth(75)
        self._combobox.currentIndexChanged.connect(self._trigger_instant_update)
        self._combobox.addItems([ALL_COLLECTIONS] + sorted(font_maps.keys()))

        lyt = widgets.BoxLayout("horizontal")
        lyt.set_margin(0)
        lyt.add(self._combobox)
        lyt.add(self._lineedit)

        search_bar_frame = widgets.Frame(self)
        search_bar_frame.setLayout(lyt)

        self._copy_button = widgets.PushButton("Copy Name", self)
        self._copy_button.clicked.connect(self._copy_icon_text)

        lyt = widgets.BoxLayout("vertical")
        lyt.add(search_bar_frame)
        lyt.add(self._listview)
        lyt.add(self._copy_button)
        frame = widgets.Frame(self)
        frame.set_layout(lyt)
        self.setCentralWidget(frame)
        widgets.Shortcut(gui.KeySequence("return"), self, self._copy_icon_text)
        self._lineedit.setFocus()
        self.center()

    def _update_filter(self):
        """Update filter string in the proxy model with current lineedit text."""
        re_string = ""
        if (group := self._combobox.currentText()) != ALL_COLLECTIONS:
            re_string += fr"^{group}\."
        if search_term := self._lineedit.text():
            re_string += f".*{search_term}.*$"

        self._proxy_model.setFilterRegularExpression(re_string)

    def _trigger_instant_update(self):
        """Stop timer used for committing search term and update proxy model instantly."""
        self._filter_timer.stop()
        self._update_filter()

    def _copy_icon_text(self):
        """Copy the name of the currently selected icon to the clipboard."""
        if indexes := self._listview.selectedIndexes():
            widgets.Application.copy_to_clipboard(indexes[0].data())


class IconListView(widgets.ListView):
    """A QListView that scales its grid size to always show same amount of items."""

    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self.set_vertical_scrollbar_policy("always_on")
        self.VIEW_COLUMNS = 5

    def resizeEvent(self, event):
        """Re-calculate the grid size to provide scaling icons."""
        width = self.viewport().width() - 30
        # The minus 30 above ensures we don't end up with an item width that
        # can't be drawn the expected number of times across the view without
        # being wrapped. Without this, the view can flicker during resize
        tile_width = int(width / self.VIEW_COLUMNS)
        icon_width = int(tile_width * 0.8)
        self.set_grid_size((tile_width, tile_width))
        self.set_icon_size((icon_width, icon_width))

        return super().resizeEvent(event)


class IconModel(core.StringListModel):
    def __init__(self, icon_color: QtGui.QColor):
        super().__init__()
        self._icon_color = icon_color

    def flags(self, index):
        return constants.IS_ENABLED | constants.IS_SELECTABLE  # type: ignore

    def data(self, index, role):
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
