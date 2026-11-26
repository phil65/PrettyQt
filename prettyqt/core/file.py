from prettyqt import core


class FileMixin(core.FileDeviceMixin):
    pass


class File(FileMixin, core.QFile):
    """Interface for reading from and writing to files."""
