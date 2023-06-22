from __future__ import annotations

from typing import Literal

from prettyqt.qt import QtCore
from prettyqt.utils import bidict

FlagStr = Literal["hidden_from_help", "short_option_style"]

FLAGS: bidict[FlagStr, QtCore.QCommandLineOption.Flag] = bidict(
    hidden_from_help=QtCore.QCommandLineOption.Flag.HiddenFromHelp,
    short_option_style=QtCore.QCommandLineOption.Flag.ShortOptionStyle,
)


class CommandLineOption(QtCore.QCommandLineOption):
    pass
