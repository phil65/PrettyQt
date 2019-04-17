# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import pathlib
from typing import List, Optional

from qtpy import QtWidgets

from prettyqt import core, widgets

MODES = dict(existing_file=QtWidgets.QFileDialog.ExistingFile,
             existing_files=QtWidgets.QFileDialog.ExistingFiles,
             any_file=QtWidgets.QFileDialog.ExistingFiles,
             directory=QtWidgets.QFileDialog.ExistingFiles)

LABELS = dict(look_in=QtWidgets.QFileDialog.LookIn,
              filename=QtWidgets.QFileDialog.FileName,
              filetype=QtWidgets.QFileDialog.FileType,
              accept=QtWidgets.QFileDialog.Accept,
              reject=QtWidgets.QFileDialog.Reject)


class FileDialog(QtWidgets.QFileDialog):
    """
    simple dialog used to display some widget
    """

    def __init__(self, path=None, mode="open", caption="", path_id=None, parent=None):
        self.path_id = path_id
        if path_id and path is None:
            settings = core.Settings()
            path = settings.value(self.path_id, "")
        super().__init__(directory=path, caption=caption, parent=parent)
        self.set_file_mode("existing_files")
        self.set_accept_mode(mode)

    def set_accept_mode(self, mode: str):
        if mode == "save":
            self.setAcceptMode(self.AcceptSave)
        else:
            self.setAcceptMode(self.AcceptOpen)

    def set_label_text(self, label: str, text: str):
        if label not in LABELS:
            raise ValueError(f"Invalid value. Valid values: {LABELS.keys()}")
        self.setLabelText(LABELS[label], text)

    def set_file_mode(self, mode: str):
        """sets the file mode of the dialog

        allowed values are 'existing_file', 'existing_files',
        'any_file' and 'directory'

        Args:
            mode: mode to use
        """
        self.setFileMode(MODES[mode])

    def selected_files(self) -> List[pathlib.Path]:
        return [pathlib.Path(p) for p in self.selectedFiles()]

    def selected_file(self) -> Optional[pathlib.Path]:
        selected = self.selectedFiles()
        if selected:
            return pathlib.Path(selected[0])

    def choose_folder(self) -> Optional[List[pathlib.Path]]:
        self.setFileMode(self.Directory)
        return self.choose()

    def open_file(self) -> Optional[List[pathlib.Path]]:
        self.setFileMode(self.ExistingFile)
        return self.choose()

    def choose(self) -> Optional[List[pathlib.Path]]:
        result = super().exec_()
        if result != self.Accepted:
            return None
        paths = self.selected_files()
        folder_path = paths[0].parent
        if self.path_id:
            settings = core.Settings()
            settings.setValue(self.path_id, str(folder_path))
        return paths

    def set_filter(self, extension_dict: dict):
        """set filter based on given dictionary

        dict must contain "'name': ['.ext1', '.ext2']" as key-value pairs

        Args:
            extension_dict: filter dictionary
        """
        items = [f"{k} ({' '.join(f'*{ext}' for ext in v)})"
                 for k, v in extension_dict.items()]
        filter_str = ";;".join(items)
        self.setNameFilter(filter_str)

    def directory(self) -> pathlib.Path:
        """return current directory

        returns current directory level as a Pathlib object

        Returns:
            Pathlib object
        """
        return pathlib.Path(super().directory())


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    widget = FileDialog(path_id="test", caption="Some header")
    widget.show()
    app.exec_()
