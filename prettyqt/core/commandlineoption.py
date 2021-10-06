from __future__ import annotations

from prettyqt.qt import QtCore
from prettyqt.utils import bidict


FLAGS = bidict(
    hidden_from_help=QtCore.QCommandLineOption.Flag.HiddenFromHelp,
    short_option_style=QtCore.QCommandLineOption.Flag.ShortOptionStyle,
)


class CommandLineOption(QtCore.QCommandLineOption):
    pass
