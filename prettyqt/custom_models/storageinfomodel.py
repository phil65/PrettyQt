from __future__ import annotations

from prettyqt import constants, core, custom_models


class RootPathColumn(custom_models.ColumnItem):
    name = "Root path"
    doc = "Root path"

    def get_data(self, item: core.QStorageInfo, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return item.rootPath()


class VolumeNameColumn(custom_models.ColumnItem):
    name = "Volume name"
    doc = "Volume name"

    def get_data(self, item: core.QStorageInfo, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return item.name()


class DeviceColumn(custom_models.ColumnItem):
    name = "Device"

    def get_data(self, item: core.QStorageInfo, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return item.device().data().decode()


class FileSystemColumn(custom_models.ColumnItem):
    name = "File system"

    def get_data(self, item: core.QStorageInfo, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return item.fileSystemType().data().decode()


class TotalColumn(custom_models.ColumnItem):
    name = "Total"
    precision = 2
    fmt: core._locale.DataSizeFormatStr = "iec"

    def get_data(self, item: core.QStorageInfo, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return core.Locale().get_formatted_data_size(
                    item.bytesTotal(), precision=self.precision, fmt=self.fmt
                )


class FreeColumn(custom_models.ColumnItem):
    name = "Free"
    precision = 2
    fmt: core._locale.DataSizeFormatStr = "iec"

    def get_data(self, item: core.QStorageInfo, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return core.Locale().get_formatted_data_size(
                    item.bytesFree(), precision=self.precision, fmt=self.fmt
                )


class AvailableColumn(custom_models.ColumnItem):
    name = "Available"
    precision = 2
    fmt: core._locale.DataSizeFormatStr = "iec"

    def get_data(self, item: core.QStorageInfo, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return core.Locale().get_formatted_data_size(
                    item.bytesAvailable(), precision=self.precision, fmt=self.fmt
                )


class ReadyColumn(custom_models.ColumnItem):
    name = "Is ready"

    def get_data(self, item: core.QStorageInfo, role: constants.ItemDataRole):
        match role:
            case constants.CHECKSTATE_ROLE:
                return self.to_checkstate(item.isReady())


class ReadOnlyColumn(custom_models.ColumnItem):
    name = "Read-only"

    def get_data(self, item: core.QStorageInfo, role: constants.ItemDataRole):
        match role:
            case constants.CHECKSTATE_ROLE:
                return self.to_checkstate(item.isReadOnly())


class ValidColumn(custom_models.ColumnItem):
    name = "Valid"

    def get_data(self, item: core.QStorageInfo, role: constants.ItemDataRole):
        match role:
            case constants.CHECKSTATE_ROLE:
                return self.to_checkstate(item.isValid())


class StorageInfoModel(custom_models.ColumnTableModel):
    COLUMNS = [
        RootPathColumn,
        VolumeNameColumn,
        DeviceColumn,
        FileSystemColumn,
        TotalColumn,
        FreeColumn,
        AvailableColumn,
        ReadyColumn,
        ReadOnlyColumn,
        ValidColumn,
    ]

    def __init__(self, volumes: list[core.QStorageInfo], parent=None):
        super().__init__(volumes, self.COLUMNS, parent=parent)

    @classmethod
    def supports(cls, instance) -> bool:
        match instance:
            case (core.QStorageInfo(), *_):
                return True
            case _:
                return False


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    view = widgets.TreeView()
    volumes = core.StorageInfo.get_mounted_volumes()
    model = StorageInfoModel(volumes, parent=view)
    view.setModel(model)
    view.resize(640, 480)
    view.set_selection_behavior("rows")
    view.adapt_sizes()
    view.show()
    app.exec()
