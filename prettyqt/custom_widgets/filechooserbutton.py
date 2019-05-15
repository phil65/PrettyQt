# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import pathlib

from prettyqt import core, widgets


class FileChooserButton(widgets.Widget):

    value_changed = core.Signal(pathlib.Path)

    def __init__(self, extensions=None, parent=None):
        super().__init__(parent)
        self.path = None
        self.extensions = extensions
        layout = widgets.BoxLayout("horizontal", self)
        layout.set_margin(0)
        self.lineedit = widgets.LineEdit()
        layout += self.lineedit
        action = widgets.Action()
        action.set_icon("mdi.file-outline")
        action.triggered.connect(self.open_file)

        self.button = widgets.ToolButton()
        self.button.setDefaultAction(action)
        layout += self.button

    def __getstate__(self):
        return dict(path=self.path,
                    extensions=self.extensions,
                    enabled=self.isEnabled())

    def __setstate__(self, state):
        self.__init__(state["extensions"])
        self.set_path(state["path"])
        self.setEnabled(state.get("enabled", True))

    @core.Slot()
    def open_file(self):
        dialog = widgets.FileDialog(parent=self,
                                    path_id="file_path")
        if self.extensions:
            dialog.setNameFilter(self.extensions)
        if not dialog.open_file():
            return None
        self.set_path(dialog.selected_file())
        self.value_changed.emit(self.path)

    def set_path(self, path):
        self.path = path
        self.lineedit.setText(str(path))

    def get_value(self):
        return self.path

    def set_value(self, value):
        self.set_path(value)


if __name__ == "__main__":
    app = widgets.app()
    btn = FileChooserButton()
    btn.show()
    btn.value_changed.connect(print)
    app.exec_()
