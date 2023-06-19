from __future__ import annotations

from prettyqt import core, custom_models


# class RootPathColumn(custom_models.ColumnItem):
#     name="Root path"
#     doc="Root path"

#     def get_data(self, item, role):
#         match role:
#             case constants.DISPLAY_ROLE:
#                 return str(item.get_root_path())


# class VolumeNameColumn(custom_models.ColumnItem):
#     name="Volume name"
#     doc="Volume name"

#     def get_data(self, item, role):
#         match role:
#             case constants.DISPLAY_ROLE:
#                 return item.name()


# class DeviceColumn(custom_models.ColumnItem):
#     name="Device"

#     def get_data(self, item, role):
#         match role:
#             case constants.DISPLAY_ROLE:
#                 return item.get_device()


# class FileSystemColumn(custom_models.ColumnItem):
#     name="File system"

#     def get_data(self, item, role):
#         match role:
#             case constants.DISPLAY_ROLE:
#                 return item.get_file_system_type()


# class TotalColumn(custom_models.ColumnItem):
#     name = "Total"

#     def get_data(self, item, role):
#         match role:
#             case constants.DISPLAY_ROLE:
#                 return core.Locale().get_formatted_data_size(item.bytesTotal())


# class FreeColumn(custom_models.ColumnItem):
#     name = "Free"

#     def get_data(self, item, role):
#         match role:
#             case constants.DISPLAY_ROLE:
#                 return core.Locale().get_formatted_data_size(item.bytesFree())


# class AvailableColumn(custom_models.ColumnItem):
#     name = "Available"

#     def get_data(self, item, role):
#         match role:
#             case constants.DISPLAY_ROLE:
#                 return core.Locale().get_formatted_data_size(item.bytesAvailable())


# class ReadyColumn(custom_models.ColumnItem):
#     name = "Is ready"

#     def get_data(self, item, role):
#         match role:
#             case constants.CHECKSTATE_ROLE:
#                 return item.isReady()


# class ReadOnlyColumn(custom_models.ColumnItem):
#     name = "Read-only"

#     def get_data(self, item, role):
#         match role:
#             case constants.CHECKSTATE_ROLE:
#                 return item.isReadOnly()


# class ValidColumn(custom_models.ColumnItem):
#     name = "Valid"

#     def get_data(self, item, role):
#         match role:
#             case constants.CHECKSTATE_ROLE:
#                 return item.isValid()


# COLUMNS = [
#     RootPathColumn,
#     VolumeNameColumn,
#     DeviceColumn,
#     FileSystemColumn,
#     TotalColumn,
#     FreeColumn,
#     AvailableColumn,
#     ReadyColumn,
#     ReadOnlyColumn,
#     ValidColumn,
# ]


loc = core.Locale()

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
    label=lambda volume: loc.get_formatted_data_size(volume.bytesTotal()),
)

COL_FREE = custom_models.ColumnItem(
    name="Free",
    doc="Free",
    label=lambda volume: loc.get_formatted_data_size(volume.bytesFree()),
)

COL_AVAILABLE = custom_models.ColumnItem(
    name="Available",
    doc="Available",
    label=lambda volume: loc.get_formatted_data_size(volume.bytesAvailable()),
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


class StorageInfoModel(custom_models.ColumnTableModel):
    def __init__(self, volumes, parent=None):
        super().__init__(volumes, COLUMNS, parent=parent)

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
    app.main_loop()
