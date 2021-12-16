from __future__ import annotations

import os
import pathlib
from typing import Literal

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import InvalidParamError, bidict, helpers, types


FILE_MODE = bidict(
    existing_file=QtWidgets.QFileDialog.FileMode.ExistingFile,
    existing_files=QtWidgets.QFileDialog.FileMode.ExistingFiles,
    any_file=QtWidgets.QFileDialog.FileMode.AnyFile,
    directory=QtWidgets.QFileDialog.FileMode.Directory,
)

FileModeStr = Literal["existing_file", "existing_files", "any_file", "directory"]

LABEL = bidict(
    look_in=QtWidgets.QFileDialog.DialogLabel.LookIn,
    filename=QtWidgets.QFileDialog.DialogLabel.FileName,
    filetype=QtWidgets.QFileDialog.DialogLabel.FileType,
    accept=QtWidgets.QFileDialog.DialogLabel.Accept,
    reject=QtWidgets.QFileDialog.DialogLabel.Reject,
)

LabelStr = Literal["look_in", "filename", "filetype", "accept"]

ACCEPT_MODE = bidict(
    save=QtWidgets.QFileDialog.AcceptMode.AcceptSave,
    open=QtWidgets.QFileDialog.AcceptMode.AcceptOpen,
)

AcceptModeStr = Literal["save", "open"]

VIEW_MODE = bidict(
    detail=QtWidgets.QFileDialog.ViewMode.Detail, list=QtWidgets.QFileDialog.ViewMode.List
)

ViewModeStr = Literal["detail", "list"]


QtWidgets.QFileDialog.__bases__ = (widgets.Dialog,)


class FileDialog(QtWidgets.QFileDialog):
    """Simple dialog used to display some widget."""

    def __init__(
        self,
        path: None | types.PathType = None,
        mode: AcceptModeStr = "open",
        caption: str | None = None,
        path_id: str | None = None,
        extension_filter: dict | None = None,
        file_mode: FileModeStr = "existing_files",
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(parent=parent)
        self.set_title(caption)
        self.path_id = path_id
        if extension_filter:
            self.set_extension_filter(extension_filter)
        if path_id is not None and path is None:
            settings = core.Settings()
            path = settings.get(path_id, "")
        if path is not None:
            self.set_directory(path)
        self.set_file_mode(file_mode)
        self.set_accept_mode(mode)

    def serialize_fields(self):
        return dict(
            file_mode=self.get_file_mode(),
            accept_mode=self.get_accept_mode(),
            filter=self.get_filter(),
            view_mode=self.get_view_mode(),
            name_filter=self.selectedNameFilter(),
            default_suffix=self.defaultSuffix(),
            name_filters=self.nameFilters(),
            supported_schemes=self.supportedSchemes(),
        )

    def __setstate__(self, state):
        self.set_file_mode(state["file_mode"])
        self.set_accept_mode(state["accept_mode"])
        self.set_view_mode(state["view_mode"])
        self.set_filter(*state["filter"])
        self.setNameFilters(state["name_filters"])
        self.setNameFilter(state["name_filter"])
        self.setDefaultSuffix(state["default_suffix"])
        self.setSupportedSchemes(state["supported_schemes"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def set_accept_mode(self, mode: AcceptModeStr):
        """Set accept mode.

        Args:
            mode: accept mode to use

        Raises:
            InvalidParamError: invalid accept mode
        """
        if mode not in ACCEPT_MODE:
            raise InvalidParamError(mode, ACCEPT_MODE)
        self.setAcceptMode(ACCEPT_MODE[mode])

    def get_accept_mode(self) -> AcceptModeStr:
        """Return accept mode.

        Returns:
            accept mode
        """
        return ACCEPT_MODE.inverse[self.acceptMode()]

    def set_view_mode(self, mode: ViewModeStr):
        """Set view mode.

        Args:
            mode: view mode to use

        Raises:
            InvalidParamError: invalid view mode
        """
        if mode not in VIEW_MODE:
            raise InvalidParamError(mode, VIEW_MODE)
        self.setViewMode(VIEW_MODE[mode])

    def get_view_mode(self) -> ViewModeStr:
        """Return view mode.

        Returns:
            view mode
        """
        return VIEW_MODE.inverse[self.viewMode()]

    def set_label_text(self, label: LabelStr, text: str):
        """Set the label text for button label.

        Args:
            label: button to set text for
            text: text to use
        """
        if label not in LABEL:
            raise InvalidParamError(label, LABEL)
        self.setLabelText(LABEL[label], text)

    def get_label_text(self, label: LabelStr) -> str:
        """Return label text.

        Returns:
            label text
        """
        return self.labelText(LABEL[label])

    def get_file_mode(self) -> FileModeStr:
        """Return file mode.

        Returns:
            file mode
        """
        return FILE_MODE.inverse[self.fileMode()]

    def set_file_mode(self, mode: FileModeStr):
        """Set the file mode of the dialog.

        Args:
            mode: mode to use
        """
        self.setFileMode(FILE_MODE[mode])

    def selected_files(self) -> list[pathlib.Path]:
        return [pathlib.Path(p) for p in self.selectedFiles()]

    def selected_file(self) -> pathlib.Path | None:
        selected = self.selectedFiles()
        return pathlib.Path(selected[0]) if selected else None

    def choose_folder(self) -> list[pathlib.Path] | None:
        self.set_file_mode("directory")
        return self.choose()

    def open_file(self) -> list[pathlib.Path] | None:
        self.set_file_mode("existing_file")
        return self.choose()

    def choose(self) -> list[pathlib.Path] | None:
        result = self.main_loop()
        if result != self.Accepted:
            return None
        paths = self.selected_files()
        folder_path = paths[0].parent
        if self.path_id:
            settings = core.Settings()
            settings.setValue(self.path_id, str(folder_path))
        return paths

    def set_extension_filter(self, extension_dict: dict[str, list[str]]):
        """Set filter based on given dictionary.

        dict must contain "'name': ['.ext1', '.ext2']" as key-value pairs

        Args:
            extension_dict: filter dictionary
        """
        items = [
            f"{k} ({' '.join(f'*{ext}' for ext in v)})" for k, v in extension_dict.items()
        ]
        filter_str = ";;".join(items)
        self.setNameFilter(filter_str)

    def get_directory(self) -> pathlib.Path:
        """Return current directory.

        returns current directory level as a Pathlib object

        Returns:
            Pathlib object
        """
        return pathlib.Path(self.directory().absolutePath())

    def set_directory(self, path: types.PathType):
        """Set start directory."""
        path = os.fspath(path)
        self.setDirectory(path)

    def set_filter(self, *filters: core.dir.FilterStr):
        for item in filters:
            if item not in core.dir.FILTERS:
                raise InvalidParamError(item, core.dir.FILTERS)
        flags = helpers.merge_flags(filters, core.dir.FILTERS)
        self.setFilter(flags)

    def get_filter(self) -> list[core.dir.FilterStr]:
        return [k for k, v in core.dir.FILTERS.items() if v & self.filter()]


if __name__ == "__main__":
    app = widgets.app()
    widget = FileDialog()
    widget.show()
    print(widget.__getstate__())
    app.main_loop()
