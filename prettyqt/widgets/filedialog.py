# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import pathlib
from typing import List, Optional, Union

from qtpy import QtWidgets

from prettyqt import core, widgets
from prettyqt.utils import bidict

MODES = bidict(existing_file=QtWidgets.QFileDialog.ExistingFile,
               existing_files=QtWidgets.QFileDialog.ExistingFiles,
               any_file=QtWidgets.QFileDialog.AnyFile,
               directory=QtWidgets.QFileDialog.Directory)

LABELS = bidict(look_in=QtWidgets.QFileDialog.LookIn,
                filename=QtWidgets.QFileDialog.FileName,
                filetype=QtWidgets.QFileDialog.FileType,
                accept=QtWidgets.QFileDialog.Accept,
                reject=QtWidgets.QFileDialog.Reject)

ACCEPT_MODES = bidict(save=QtWidgets.QFileDialog.AcceptSave,
                      open=QtWidgets.QFileDialog.AcceptOpen)

VIEW_MODES = bidict(detail=QtWidgets.QFileDialog.Detail,
                    list=QtWidgets.QFileDialog.List)

FILTERS = bidict(dirs=core.Dir.Dirs,
                 all_dirs=core.Dir.AllDirs,
                 files=core.Dir.Files)


QtWidgets.QFileDialog.__bases__ = (widgets.BaseDialog,)


class FileDialog(QtWidgets.QFileDialog):
    """
    simple dialog used to display some widget
    """

    def __init__(self,
                 path: Union[None, str, pathlib.Path] = None,
                 mode: str = "open",
                 caption: Optional[str] = None,
                 path_id: Optional[str] = None,
                 extension_filter: Optional[dict] = None,
                 file_mode: str = "existing_files",
                 parent=None):
        super().__init__(parent=parent)
        self.title = caption
        self.path_id = path_id
        if extension_filter:
            self.set_extension_filter(extension_filter)
        if path_id and path is None:
            settings = core.Settings()
            path = settings.value(self.path_id, "")
        self.set_directory(path)
        self.set_file_mode(file_mode)
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
        """set accept mode

        possible values are "save", "open"

        Args:
            mode: accept mode to use

        Raises:
            ValueError: invalid accept mode
        """
        if mode not in ACCEPT_MODES:
            raise ValueError(f"Invalid value. Valid values: {ACCEPT_MODES.keys()}")
        self.setAcceptMode(ACCEPT_MODES[mode])

    def get_accept_mode(self) -> str:
        """returns accept mode

        possible values are "save", "open"

        Returns:
            accept mode
        """
        return ACCEPT_MODES.inv[self.acceptMode()]

    def set_view_mode(self, mode: str):
        """set view mode

        possible values are "detail", "list"

        Args:
            mode: view mode to use

        Raises:
            ValueError: invalid view mode
        """
        if mode not in VIEW_MODES:
            raise ValueError(f"Invalid value. Valid values: {VIEW_MODES.keys()}")
        self.setViewMode(VIEW_MODES[mode])

    def get_view_mode(self) -> str:
        """returns view mode

        possible values are "detail", "list"

        Returns:
            view mode
        """
        return VIEW_MODES.inv[self.viewMode()]

    def set_label_text(self, label: str, text: str):
        """sets the label text for button label

        possible values for label are "look_in", "filename", "filetype",
        "accept", "reject"

        Args:
            label: button to set text for
            text: text to use
        """
        if label not in LABELS:
            raise ValueError(f"Invalid value. Valid values: {LABELS.keys()}")
        self.setLabelText(LABELS[label], text)

    def get_label_text(self, label) -> str:
        """returns label text

        possible values are "look_in", "filename", "filetype", "accept", "reject"

        Returns:
            label text
        """
        return self.labelText(LABELS.inv[label])

    def get_file_mode(self) -> str:
        """returns file mode

        possible values are "existing_file", "existing_files", "any_file", "directory"

        Returns:
            file mode
        """
        return MODES.inv[self.fileMode()]

    def set_file_mode(self, mode: str):
        """sets the file mode of the dialog

        allowed values are "existing_file", "existing_files", "any_file" "directory"

        Args:
            mode: mode to use
        """
        self.setFileMode(MODES[mode])

    def set_filter(self, to_filter):
        if to_filter not in FILTERS:
            raise ValueError(f"Invalid filter. Valid values: {FILTERS.keys()}")
        self.setFilter(FILTERS[to_filter])

    def selected_files(self) -> List[pathlib.Path]:
        return [pathlib.Path(p) for p in self.selectedFiles()]

    def selected_file(self) -> Optional[pathlib.Path]:
        selected = self.selectedFiles()
        return pathlib.Path(selected[0]) if selected else None

    def choose_folder(self) -> Optional[List[pathlib.Path]]:
        self.set_file_mode("directory")
        return self.choose()

    def open_file(self) -> Optional[List[pathlib.Path]]:
        self.set_file_mode("existing_file")
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

    def set_extension_filter(self, extension_dict: dict):
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

    def set_directory(self, path: Union[None, str, pathlib.Path]):
        """set start directory
        """
        if isinstance(path, pathlib.Path):
            path = str(path)
        self.setDirectory(path)


if __name__ == "__main__":
    app = widgets.app()
    widget = FileDialog()
    widget.show()
    print(widget.__getstate__())
    app.exec_()
