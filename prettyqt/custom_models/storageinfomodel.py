from __future__ import annotations

import math

from prettyqt import constants, core, custom_models
from prettyqt.qt import QtCore


def size_to_string(size: int) -> str:
    if size <= 0:
        return "0 b"
    decimals = 2
    units = ["b", "kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    power = int(math.log(size, 1024))
    try:
        unit = units[power]
    except IndexError:
        unit = units[-1]
        power = len(units) - 1
    if power == 0:
        decimals = 0
    normsize = size / math.pow(1024, power)
    #: this should expand to "1.23 GB"
    return "%0.*f %s" % (decimals, normsize, unit)


class StorageInfoModel(core.AbstractTableModel):
    (
        ColumnRootPath,
        ColumnName,
        ColumnDevice,
        ColumnFileSystemName,
        ColumnTotal,
        ColumnFree,
        ColumnAvailable,
        ColumnIsReady,
        ColumnIsReadOnly,
        ColumnIsValid,
        ColumnCount,
    ) = range(11)

    columnFuncMap = {
        ColumnRootPath: lambda volume: str(volume.get_root_path()),
        ColumnName: lambda volume: volume.name(),
        ColumnDevice: lambda volume: volume.get_device(),
        ColumnFileSystemName: lambda volume: volume.get_file_system_type(),
        ColumnTotal: lambda volume: size_to_string(volume.bytesTotal()),
        ColumnFree: lambda volume: size_to_string(volume.bytesFree()),
        ColumnAvailable: lambda volume: size_to_string(volume.bytesAvailable()),
        ColumnIsReady: lambda volume: volume.isReady(),
        ColumnIsReadOnly: lambda volume: volume.isReadOnly(),
        ColumnIsValid: lambda volume: volume.isValid(),
    }

    columnNameMap = {
        ColumnRootPath: "Root path",
        ColumnName: "Volume Name",
        ColumnDevice: "Device",
        ColumnFileSystemName: "File system",
        ColumnTotal: "Total",
        ColumnFree: "Free",
        ColumnAvailable: "Available",
        ColumnIsReady: "Ready",
        ColumnIsReadOnly: "Read-only",
        ColumnIsValid: "Valid",
    }

    def __init__(self, parent: QtCore.QObject | None = None):
        super().__init__(parent)
        self.volumes = core.StorageInfo.get_mounted_volumes()

    def columnCount(self, parent=None):
        return self.ColumnCount

    def rowCount(self, parent):
        if parent.isValid():
            return 0
        return len(self.volumes)

    def data(self, index, role):
        if not index.isValid():
            return None
        if role == constants.DISPLAY_ROLE:
            volume = self.volumes[index.row()]
            func = self.columnFuncMap.get(index.column())
            if func is not None:
                return func(volume)

        elif role == constants.TOOLTIP_ROLE:
            volume = self.volumes[index.row()]
            tooltip = []
            for column in range(self.ColumnCount):
                label = self.columnNameMap.get(column)
                value = self.columnFuncMap[column](volume)
                tooltip.append(f"{label}: {value}")
            return "\n".join(tooltip)

    def headerData(self, section, orientation, role):
        if orientation != constants.HORIZONTAL:
            return None
        if role != constants.DISPLAY_ROLE:
            return None
        return self.columnNameMap.get(section)


column_root_path = custom_models.ColumnItem(
    name="Root path",
    doc="Root path",
    label=lambda volume: str(volume.get_root_path()),
)

column_volume_name = custom_models.ColumnItem(
    name="Volume name",
    doc="Volume name",
    label=lambda volume: volume.name(),
)

column_volume_name = custom_models.ColumnItem(
    name="Volume name",
    doc="Volume name",
    label=lambda volume: volume.name(),
)

column_volume_name = custom_models.ColumnItem(
    name="Volume name",
    doc="Volume name",
    label=lambda volume: volume.name(),
)

column_device = custom_models.ColumnItem(
    name="Device",
    doc="Device",
    label=lambda volume: volume.get_device(),
)

column_file_system_name = custom_models.ColumnItem(
    name="File system",
    doc="File system",
    label=lambda volume: volume.get_file_system_type(),
)

column_total = custom_models.ColumnItem(
    name="Total",
    doc="Total",
    label=lambda volume: size_to_string(volume.bytesTotal()),
)

column_free = custom_models.ColumnItem(
    name="Free",
    doc="Free",
    label=lambda volume: size_to_string(volume.bytesFree()),
)

column_available = custom_models.ColumnItem(
    name="Available",
    doc="Available",
    label=lambda volume: size_to_string(volume.bytesAvailable()),
)

column_ready = custom_models.ColumnItem(
    name="Available",
    doc="Available",
    label=None,
    checkstate=lambda volume: volume.isReady(),
)

column_readonly = custom_models.ColumnItem(
    name="Read-only",
    doc="Read-only",
    label=None,
    checkstate=lambda volume: volume.isReadOnly(),
)

if __name__ == "__main__":
    import sys

    from prettyqt import widgets

    app = widgets.Application(sys.argv)
    view = widgets.TreeView()
    view.setModel(StorageInfoModel(view))
    view.resize(640, 480)
    view.set_selection_behaviour("rows")
    for column in range(view.model().columnCount()):
        view.resizeColumnToContents(column)
    view.show()
    app.main_loop()
