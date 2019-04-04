# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import pathlib

from qtpy import QtWidgets, QtCore

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

    def __init__(self, path=None, mode=None, caption="", path_id=None, parent=None):
        self.path_id = path_id
        settings = QtCore.QSettings()
        initial_path = settings.value(self.path_id, "")
        super().__init__(directory=initial_path, caption=caption, parent=parent)
        self.set_file_mode("existing_files")
        self.set_accept_mode(mode)

    def set_accept_mode(self, mode: str):
        if mode == "save":
            self.setAcceptMode(self.AcceptSave)
        else:
            self.setAcceptMode(self.AcceptOpen)

    def set_label_text(self, label):
        if label not in LABELS:
            raise ValueError(f"Invalid value. Valid values: {LABELS.keys()}")
        self.setLabelText(LABELS[label])

    def set_file_mode(self, mode: str):
        """sets the file mode of the dialog

        allowed values are 'existing_file', 'existing_files',
        'any_file' and 'directory'

        Args:
            mode: mode to use
        """
        self.setFileMode(MODES[mode])

    def selected_files(self):
        return [pathlib.Path(p) for p in self.selectedFiles()]

    def selected_file(self):
        selected = self.selectedFiles()
        if selected:
            return pathlib.Path(selected[0])

    def choose_folder(self):
        self.setFileMode(QtWidgets.QFileDialog.Directory)
        return self.choose()

    def open_file(self):
        self.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        return self.choose()

    def choose(self):
        result = super().exec_()
        if result != QtWidgets.QDialog.Accepted:
            return None
        paths = self.selected_files()
        folder_path = paths[0].parent
        if self.path_id:
            settings = QtCore.QSettings()
            settings.setValue(self.path_id, str(folder_path))
        return paths

    def set_filter(self, extension_dict):
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
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = FileDialog(path_id="test", caption="Some header")
    widget.show()
    app.exec_()
