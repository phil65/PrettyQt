# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import pathlib

from qtpy import QtCore, QtWidgets

from prettyqt import core


class FileSystemModel(QtWidgets.QFileSystemModel):
    """
    Class to populate a filesystem treeview
    """
    DATA_ROLE = QtCore.Qt.UserRole + 33
    content_type = "files"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setReadOnly(False)
        self.setRootPath(QtCore.QDir.rootPath())

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == self.DATA_ROLE:
            path = index.data(self.FilePathRole)
            return pathlib.Path(path)
        return super().data(index, role)

    def yield_child_indexes(self, index):
        if not self.hasChildren(index):
            return None
        path = self.filePath(index)
        flags = self.filter() | QtCore.QDir.NoDotAndDotDot
        it = core.DirIterator(path, flags)
        while it.hasNext():
            yield self.index(it.next())
