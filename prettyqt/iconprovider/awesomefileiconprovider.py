from __future__ import annotations

import mimetypes
from typing import TYPE_CHECKING

from prettyqt import gui, iconprovider, widgets
from prettyqt.qt import QtCore


if TYPE_CHECKING:
    from prettyqt.qt import QtWidgets


class AwesomeFileIconProvider(widgets.FileIconProvider):
    def __init__(self):
        super().__init__()
        self.folder_icon = iconprovider.get_icon("mdi.folder")
        self.text_icon = iconprovider.get_icon("mdi.file-document")
        self.file_icon = iconprovider.get_icon("mdi.file")
        self.desktop_icon = iconprovider.get_icon("mdi.desktop-mac-dashboard")
        self.computer_icon = iconprovider.get_icon("mdi.desktop-classic")
        self.trashcan_icon = iconprovider.get_icon("mdi.trash-can")
        self.drive_icon = iconprovider.get_icon("mdi.harddisk")
        self.network_icon = iconprovider.get_icon("mdi.folder-network")

    def icon(
        self, icon: QtWidgets.QFileIconProvider.IconType | QtCore.QFileInfo
    ) -> gui.Icon:
        match icon:
            case QtCore.QFileInfo():
                if icon.isDir():
                    return self.folder_icon
                elif icon.isFile():
                    return self.file_icon
            case widgets.FileIconProvider.IconType.Folder:
                return self.folder_icon
            # case widgets.FileIconProvider.IconType.File:
            #     return self.file_icon
            case widgets.FileIconProvider.IconType.Computer:
                return self.computer_icon
            case widgets.FileIconProvider.IconType.Desktop:
                return self.desktop_icon
            case widgets.FileIconProvider.IconType.Trashcan:
                return self.trashcan_icon
            case widgets.FileIconProvider.IconType.Network:
                return self.network_icon
            case widgets.FileIconProvider.IconType.Drive:
                return self.drive_icon
            case _:
                return self.file_icon

    @staticmethod
    def mimetype_icon(path, fallback=None):
        """Try to create an icon from theme using the file mimetype.

        E.g.::

            return self.mimetype_icon(
                path, fallback=':/icons/text-x-python.png')

        :param path: file path for which the icon must be created
        :param fallback: fallback icon path (qrc or file system)
        :returns: QIcon or None if the file mimetype icon could not be found.
        """
        if mime := mimetypes.guess_type(path)[0]:
            icon = mime.replace("/", "-")
            # if system.WINDOWS:
            #     return icons.file()
            if gui.Icon.hasThemeIcon(icon):
                icon = gui.Icon.fromTheme(icon)
                if not icon.isNull():
                    return icon
        return gui.Icon(fallback) if fallback else gui.Icon.fromTheme("text-x-generic")


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    app.load_language("de")
    model = widgets.FileSystemModel()
    model.set_root_path("root")
    prov = AwesomeFileIconProvider()
    model.setIconProvider(prov)
    tree = widgets.TreeView()
    tree.set_model(model)
    tree.show()
    app.main_loop()
