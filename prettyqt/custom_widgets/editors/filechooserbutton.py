from __future__ import annotations

import os
import pathlib
from typing import Any

from prettyqt import core, gui, widgets
from prettyqt.utils import datatypes


class FileChooserButton(widgets.Widget):
    value_changed = core.Signal(pathlib.Path)

    def __init__(
        self,
        extensions: dict[str, list[str]] | None = None,
        mode: widgets.filedialog.AcceptModeStr = "save",
        file_mode: widgets.filedialog.FileModeStr = "existing_files",
        root: None | str | pathlib.Path = None,
        object_name: str = "file_chooser_button",
        **kwargs: Any,
    ):
        """Initialize FileChooserButton.

        Args:
            extensions: dict allowed extensions
                        form: "'name': ['.ext1', '.ext2']"
            mode: Accept mode ("save" or "load")
            file_mode: File mode ("existing_files", "existing_file", "any_file",
                                  or "directory")
            root: Root path
            object_name: Object name
            kwargs: kwargs passed to parent
        """
        super().__init__(object_name=object_name, **kwargs)
        self._path: pathlib.Path | None = None
        self._extensions = extensions or []
        self.mode = mode
        self.file_mode = file_mode
        self.root = root
        layout = widgets.HBoxLayout(self)
        layout.set_margin(0)
        self.lineedit = widgets.LineEdit()
        self.lineedit.set_read_only()
        layout.add(self.lineedit)
        action = gui.Action(triggered=self.open_file)
        if self.file_mode == "directory":
            action.set_icon("mdi.folder-outline")
        else:
            action.set_icon("mdi.file-outline")

        self.button = widgets.ToolButton()
        self.button.setDefaultAction(action)
        layout.add(self.button)

    @classmethod
    def supports(cls, instance) -> bool:
        return isinstance(instance, pathlib.Path)

    @core.Slot()
    def open_file(self):
        dialog = widgets.FileDialog(
            parent=self,
            path_id="file_path",
            mode=self.mode,
            path=self.root,
            file_mode=self.file_mode,
        )
        if self._extensions:
            dialog.set_extension_filter(self._extensions)
        if not dialog.choose():
            return
        self.set_path(dialog.selected_file())
        self.value_changed.emit(self._path)

    def set_path(self, path: datatypes.PathType | None):
        if path is None:
            self._path = None
            self.lineedit.set_text("")
        else:
            self._path = pathlib.Path(path)
            self.lineedit.set_text(os.fspath(path))

    def get_value(self) -> pathlib.Path | None:
        return self._path

    def set_value(self, value: datatypes.PathType | None):
        self.set_path(value)

    def get_extensions(self) -> list[str]:
        return self._extensions

    def set_extensions(self, extensions: list[str]):
        self._extensions = extensions

    # path = core.Property(object, get_value, set_value)
    # extensions = core.Property(object, get_extensions, set_extensions)


if __name__ == "__main__":
    app = widgets.app()
    btn = FileChooserButton()
    btn.show()
    btn.value_changed.connect(print)
    app.exec()
