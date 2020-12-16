from qtpy import QtCore, QtGui, QtWidgets

from prettyqt import core, gui, widgets


OBSELETE = ["QPictureIO", "QDesktopWidget", "QDirModel"]

mapper = {gui: QtGui, widgets: QtWidgets, core: QtCore}

if __name__ == "__main__":
    for k, v in mapper.items():
        theirs = dir(v)
        ours = dir(k)
        print(f"Missing modules for {k.__name__}")
        for i in theirs:
            if i[1:] not in ours and i[0] == "Q" and i not in OBSELETE:
                print(f"{v.__name__}.{i}")
