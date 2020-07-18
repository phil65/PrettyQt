# -*- coding: utf-8 -*-
"""
"""

import pathlib
from typing import Optional, Union, List, Dict

from qtpy import QtWidgets

from prettyqt import core, widgets


class FileChooserButton(widgets.Widget):

    value_changed = core.Signal(pathlib.Path)

    def __init__(
        self,
        extensions: Optional[Dict[str, List[str]]] = None,
        mode: str = "save",
        file_mode: str = "existing_files",
        root: Union[None, str, pathlib.Path] = None,
        parent: Optional[QtWidgets.QWidget] = None,
    ):
        """initialize FileChooserButton

        Args:
            extensions: dict allowed extensions
                        form: "'name': ['.ext1', '.ext2']"
            mode: Accept mode ("save" or "load")
            file_mode: File mode ("existing_files", "existing_file", "any_file",
                                  or "directory")
            parent: parent widget
        """
        super().__init__(parent)
        self.path: Optional[pathlib.Path] = None
        self.extensions = extensions
        self.mode = mode
        self.file_mode = file_mode
        self.root = root
        layout = widgets.BoxLayout("horizontal", self)
        layout.set_margin(0)
        self.lineedit = widgets.LineEdit()
        self.lineedit.set_read_only()
        layout += self.lineedit
        action = widgets.Action()
        if self.file_mode == "directory":
            action.set_icon("mdi.folder-outline")
        else:
            action.set_icon("mdi.file-outline")
        action.triggered.connect(self.open_file)

        self.button = widgets.ToolButton()
        self.button.setDefaultAction(action)
        layout += self.button

    def __getstate__(self):
        return dict(path=self.path, extensions=self.extensions, enabled=self.isEnabled())

    def __setstate__(self, state):
        self.__init__(state["extensions"])
        self.set_path(state["path"])
        self.set_enabled(state.get("enabled", True))

    @core.Slot()
    def open_file(self):
        dialog = widgets.FileDialog(
            parent=self,
            path_id="file_path",
            mode=self.mode,
            path=self.root,
            file_mode=self.file_mode,
        )
        if self.extensions:
            dialog.set_extension_filter(self.extensions)
        if not dialog.choose():
            return None
        self.set_path(dialog.selected_file())
        self.value_changed.emit(self.path)

    def set_path(self, path: Union[str, pathlib.Path, None]):
        if isinstance(path, str):
            self.path = pathlib.Path(path)
        else:
            self.path = path
        self.lineedit.set_text(str(path) if path is not None else "")

    def get_value(self) -> Optional[pathlib.Path]:
        return self.path

    def set_value(self, value: Union[str, pathlib.Path]):
        self.set_path(value)


if __name__ == "__main__":
    app = widgets.app()
    btn = FileChooserButton()
    btn.show()
    btn.value_changed.connect(print)
    app.exec_()
