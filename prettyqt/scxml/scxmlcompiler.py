from __future__ import annotations

import pathlib

from prettyqt.qt import QtScxml


class ScxmlCompiler(QtScxml.QScxmlCompiler):
    def get_file_name(self) -> pathlib.Path:
        return pathlib.Path(self.fileName())


if __name__ == "__main__":
    from prettyqt.qt import QtCore

    reader = QtCore.QXmlStreamReader()
    compiler = ScxmlCompiler(reader)
