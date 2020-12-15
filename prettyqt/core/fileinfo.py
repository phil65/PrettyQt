import pathlib

from qtpy import QtCore

from prettyqt import core


class FileInfo(QtCore.QFileInfo):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], pathlib.Path):
            super().__init__(str(args[0]))
        else:
            super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"{type(self).__name__}({self.absoluteFilePath()!r})"

    def __str__(self):
        return self.absoluteFilePath()

    def __getattr__(self, attr: str):
        return getattr(self.get_absolute_file_path(), attr)

    def __reduce__(self):
        return self.__class__, (self.absoluteFilePath(),)

    def get_dir(self) -> pathlib.Path:
        return pathlib.Path(self.dir().absolutePath())

    def get_absolute_file_path(self) -> pathlib.Path:
        return pathlib.Path(self.absoluteFilePath())

    def get_birth_time(self) -> core.DateTime:
        return core.DateTime(self.birthTime())

    def get_metadata_change_time(self) -> core.DateTime:
        return core.DateTime(self.metadataChangeTime())

    def get_last_modified(self) -> core.DateTime:
        return core.DateTime(self.lastModified())

    def get_last_read(self) -> core.DateTime:
        return core.DateTime(self.lastRead())


if __name__ == "__main__":
    p = pathlib.Path.home()
    f = FileInfo(p)
