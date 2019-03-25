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


class FileDialog(QtWidgets.QFileDialog):
    """
    simple dialog used to display some widget
    """

    def __init__(self, path=None, mode=None, path_id=None, parent=None):
        self.path_id = path_id
        settings = QtCore.QSettings()
        initial_path = settings.value(self.path_id, "")
        super().__init__(directory=initial_path, parent=parent)
        self.set_file_mode("existing_files")
        self.set_accept_mode(mode)

    def set_accept_mode(self, mode: str):
        if mode == "save":
            self.setAcceptMode(self.AcceptSave)
        else:
            self.setAcceptMode(self.AcceptOpen)

    def set_file_mode(self, mode: str):
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
        # returns "Images (*.png *.xpm *.jpg);;Text files (*.txt);;XML files (*.xml)"
        items = [f"{k} ({' '.join(f'*{ext}' for ext in v)})"
                 for k, v in extension_dict.items()]
        filter_str = ";;".join(items)
        self.setNameFilter(filter_str)

    def directory(self):
        return pathlib.Path(super().directory())
