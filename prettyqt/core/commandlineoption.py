from qtpy import QtCore

from prettyqt.utils import bidict


FLAGS = bidict(
    hidden_from_help=QtCore.QCommandLineOption.HiddenFromHelp,
    short_option_style=QtCore.QCommandLineOption.ShortOptionStyle,
)


class CommandLineOption(QtCore.QCommandLineOption):
    pass
