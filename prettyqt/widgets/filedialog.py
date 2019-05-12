# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import pathlib
from typing import List, Optional

from bidict import bidict
from qtpy import QtWidgets

from prettyqt import core, widgets

MODES = bidict(dict(existing_file=QtWidgets.QFileDialog.ExistingFile,
                    existing_files=QtWidgets.QFileDialog.ExistingFiles,
                    any_file=QtWidgets.QFileDialog.AnyFile,
                    directory=QtWidgets.QFileDialog.Directory))

LABELS = bidict(dict(look_in=QtWidgets.QFileDialog.LookIn,
                     filename=QtWidgets.QFileDialog.FileName,
                     filetype=QtWidgets.QFileDialog.FileType,
                     accept=QtWidgets.QFileDialog.Accept,
                     reject=QtWidgets.QFileDialog.Reject))

ACCEPT_MODES = bidict(dict(save=QtWidgets.QFileDialog.AcceptSave,
                           open=QtWidgets.QFileDialog.AcceptOpen))

VIEW_MODES = bidict(dict(detail=QtWidgets.QFileDialog.Detail,
                         list=QtWidgets.QFileDialog.List))

FILTERS = bidict(dict(dirs=core.Dir.Dirs,
                      all_dirs=core.Dir.AllDirs,
                      files=core.Dir.Files))


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

    def __getstate__(self):
        return dict(file_mode=self.get_file_mode(),
                    accept_mode=self.get_accept_mode(),
                    filter=int(self.filter()),
                    view_mode=self.get_view_mode(),
                    name_filter=self.selectedNameFilter(),
                    default_suffix=self.defaultSuffix(),
                    name_filters=self.nameFilters(),
                    supported_schemes=self.supportedSchemes())

    def __setstate__(self, state):
        self.__init__()
        self.set_file_mode(state["file_mode"])
        self.set_accept_mode(state["accept_mode"])
        self.set_view_mode(state["view_mode"])
        self.setFilter(core.Dir.Filters(state["filter"]))
        self.setNameFilters(state["name_filters"])
        self.setNameFilter(state["name_filter"])
        self.setDefaultSuffix(state["default_suffix"])
        self.setSupportedSchemes(state["supported_schemes"])

    def set_accept_mode(self, mode: str):
        if mode not in ACCEPT_MODES:
            raise ValueError(f"Invalid value. Valid values: {ACCEPT_MODES.keys()}")
        self.setAcceptMode(ACCEPT_MODES[mode])

    def get_accept_mode(self):
        return ACCEPT_MODES.inv[self.acceptMode()]

    def set_view_mode(self, mode: str):
        if mode not in VIEW_MODES:
            raise ValueError(f"Invalid value. Valid values: {VIEW_MODES.keys()}")
        self.setViewMode(VIEW_MODES[mode])

    def get_view_mode(self):
        return VIEW_MODES.inv[self.viewMode()]

    def set_label_text(self, label: str, text: str):
        if label not in LABELS:
            raise ValueError(f"Invalid value. Valid values: {LABELS.keys()}")
        self.setLabelText(LABELS[label], text)

    def get_label_text(self, label):
        return self.labelText(LABELS.inv[label])

    def get_file_mode(self):
        return MODES.inv[self.fileMode()]

    def set_file_mode(self, mode: str):
        """sets the file mode of the dialog

        allowed values are 'existing_file', 'existing_files',
        'any_file' and 'directory'

        Args:
            mode: mode to use
        """
        self.setFileMode(MODES[mode])

    # def set_filter(self, to_filter):
    #     if to_filter not in FILTERS:
    #         raise ValueError(f"Invalid value. Valid values: {FILTERS.keys()}")
    #     self.setFilter(FILTERS[to_filter])

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
    print(widget.__getstate__())
    app.exec_()
