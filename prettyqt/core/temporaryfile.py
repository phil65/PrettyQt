from prettyqt import core


class TemporaryFile(core.FileMixin, core.QTemporaryFile):
    """I/O device that operates on temporary files."""
