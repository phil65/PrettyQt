from __future__ import annotations

from prettyqt import gui, iconprovider, widgets
from prettyqt.qt import QtCore, QtWidgets


class AmesomeFileIconProvider(widgets.FileIconProvider):
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
        if isinstance(icon, QtCore.QFileInfo):
            if icon.isDir():
                return self.folder_icon
            elif icon.isFile():
                return self.file_icon
        elif icon == widgets.FileIconProvider.Folder:
            return self.folder_icon
        # elif icon == widgets.FileIconProvider.File:
        #     return self.file_icon
        elif icon == widgets.FileIconProvider.Computer:
            return self.computer_icon
        elif icon == widgets.FileIconProvider.Desktop:
            return self.desktop_icon
        elif icon == widgets.FileIconProvider.Trashcan:
            return self.trashcan_icon
        elif icon == widgets.FileIconProvider.Network:
            return self.network_icon
        elif icon == widgets.FileIconProvider.Drive:
            return self.drive_icon
        return self.file_icon


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    app.load_language("de")
    model = widgets.FileSystemModel()
    model.set_root_path("root")
    prov = AmesomeFileIconProvider()
    model.setIconProvider(prov)
    tree = widgets.TreeView()
    tree.set_model(model)
    tree.show()
    app.main_loop()
