from __future__ import annotations

import os
import pathlib

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import types


class FileChooserButton(widgets.Widget):

    value_changed = core.Signal(pathlib.Path)

    def __init__(
        self,
        extensions: dict[str, list[str]] | None = None,
        mode: widgets.filedialog.AcceptModeStr = "save",
        file_mode: widgets.filedialog.FileModeStr = "existing_files",
        root: None | str | pathlib.Path = None,
        parent: QtWidgets.QWidget | None = None,
    ):
        """Initialize FileChooserButton.

        Args:
            extensions: dict allowed extensions
                        form: "'name': ['.ext1', '.ext2']"
            mode: Accept mode ("save" or "load")
            file_mode: File mode ("existing_files", "existing_file", "any_file",
                                  or "directory")
            root: Root path
            parent: parent widget
        """
        super().__init__(parent)
        self.path: pathlib.Path | None = None
        self.extensions = extensions
        self.mode: widgets.filedialog.AcceptModeStr = mode
        self.file_mode: widgets.filedialog.FileModeStr = file_mode
        self.root = root
        layout = widgets.BoxLayout("horizontal", self)
        layout.set_margin(0)
        self.lineedit = widgets.LineEdit()
        self.lineedit.set_read_only()
        layout.add(self.lineedit)
        action = widgets.Action()
        if self.file_mode == "directory":
            action.set_icon("mdi.folder-outline")
        else:
            action.set_icon("mdi.file-outline")
        action.triggered.connect(self.open_file)

        self.button = widgets.ToolButton()
        self.button.setDefaultAction(action)
        layout.add(self.button)

    def serialize_fields(self):
        return dict(path=self.path, extensions=self.extensions, enabled=self.isEnabled())

    def __setstate__(self, state):
        self.set_path(state["path"])
        self.set_enabled(state.get("enabled", True))

    def __reduce__(self):
        return type(self), (self.extensions,), self.__getstate__()

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
            return
        self.set_path(dialog.selected_file())
        self.value_changed.emit(self.path)

    def set_path(self, path: types.PathType | None):
        if path is None:
            self.path = None
            self.lineedit.set_text("")
        else:
            self.path = pathlib.Path(path)
            self.lineedit.set_text(os.fspath(path))

    def get_value(self) -> pathlib.Path | None:
        return self.path

    def set_value(self, value: types.PathType | None):
        self.set_path(value)


if __name__ == "__main__":
    app = widgets.app()
    btn = FileChooserButton()
    btn.show()
    btn.value_changed.connect(print)
    app.main_loop()
