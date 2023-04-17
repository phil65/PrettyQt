from __future__ import annotations

import math

from prettyqt import core, custom_models
from prettyqt.qt import QtCore


def size_to_string(size: int) -> str:
    if size <= 0:
        return "0 b"
    units = ["b", "kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    power = int(math.log(size, 1024))
    try:
        unit = units[power]
    except IndexError:
        unit = units[-1]
        power = len(units) - 1
    decimals = 0 if power == 0 else 2
    normsize = size / math.pow(1024, power)
    #: this should expand to "1.23 GB"
    return "%0.*f %s" % (decimals, normsize, unit)


COL_ROOT_PATH = custom_models.ColumnItem(
    name="Root path",
    doc="Root path",
    label=lambda volume: str(volume.get_root_path()),
)

COL_VOLUME_NAME = custom_models.ColumnItem(
    name="Volume name",
    doc="Volume name",
    label=lambda volume: volume.name(),
)

COL_DEVICE = custom_models.ColumnItem(
    name="Device",
    doc="Device",
    label=lambda volume: volume.get_device(),
)

COL_FILE_SYSTEM = custom_models.ColumnItem(
    name="File system",
    doc="File system",
    label=lambda volume: volume.get_file_system_type(),
)

COL_TOTAL = custom_models.ColumnItem(
    name="Total",
    doc="Total",
    label=lambda volume: size_to_string(volume.bytesTotal()),
)

COL_FREE = custom_models.ColumnItem(
    name="Free",
    doc="Free",
    label=lambda volume: size_to_string(volume.bytesFree()),
)

COL_AVAILABLE = custom_models.ColumnItem(
    name="Available",
    doc="Available",
    label=lambda volume: size_to_string(volume.bytesAvailable()),
)

COL_READY = custom_models.ColumnItem(
    name="Available",
    doc="Available",
    label=None,
    checkstate=lambda volume: volume.isReady(),
)

COL_READ_ONLY = custom_models.ColumnItem(
    name="Read-only",
    doc="Read-only",
    label=None,
    checkstate=lambda volume: volume.isReadOnly(),
)

COL_VALID = custom_models.ColumnItem(
    name="Valid",
    doc="Valid",
    label=None,
    checkstate=lambda volume: volume.isValid(),
)

COLUMNS = [
    COL_ROOT_PATH,
    COL_VOLUME_NAME,
    COL_DEVICE,
    COL_FILE_SYSTEM,
    COL_TOTAL,
    COL_FREE,
    COL_AVAILABLE,
    COL_READY,
    COL_READ_ONLY,
    COL_VALID,
]


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    view = widgets.TreeView()
    volumes = core.StorageInfo.get_mounted_volumes()
    model = custom_models.ColumnTableModel(volumes, COLUMNS, parent=view)
    view.setModel(model)
    view.resize(640, 480)
    view.set_selection_behaviour("rows")
    view.adapt_sizes()
    view.show()
    app.main_loop()
