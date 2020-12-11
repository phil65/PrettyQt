from qtpy import QtCore


class MimeType(QtCore.QMimeType):
    def __bool__(self):
        return self.isValid()

    def __str__(self):
        return self.name()
