# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import sys
import pathlib

from prettyqt import core, widgets


class FileChooserButton(widgets.Widget):

    file_updated = core.Signal(pathlib.Path)

    def __init__(self, extensions=None, parent=None):
        super().__init__(parent)
        self.path = None
        self.extensions = extensions
        layout = widgets.BoxLayout("horizontal", self)
        layout.set_margin(0)
        self.lineedit = widgets.LineEdit(self)
        layout.addWidget(self.lineedit)
        action = widgets.Action()
        action.set_icon("mdi.file-outline")
        action.triggered.connect(self.open_file)

        self.button = widgets.ToolButton(self)
        self.button.setDefaultAction(action)
        layout.addWidget(self.button)

    def __getstate__(self):
        return dict(path=self.path,
                    enabled=self.isEnabled())

    def __setstate__(self, state):
        self.__init__()
        self.set_path(state["path"])
        self.setEnabled(state["enabled"])

    @core.Slot()
    def open_file(self):
        dialog = widgets.FileDialog(parent=self,
                                    path_id="file_path")
        if self.extensions:
            dialog.setNameFilter(self.extensions)
        if not dialog.open_file():
            return None
        self.set_path(dialog.selected_file())
        self.file_updated.emit(self.path)

    def set_path(self, path):
        self.path = path
        self.lineedit.setText(str(path))


if __name__ == "__main__":
    app = widgets.Application(sys.argv)
    btn = FileChooserButton()
    btn.show()
    btn.file_updated.connect(print)
    sys.exit(app.exec_())
