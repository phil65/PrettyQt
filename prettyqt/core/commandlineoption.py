from typing import Literal

from prettyqt import core
from prettyqt.utils import bidict


FlagStr = Literal["hidden_from_help", "short_option_style", "ignore_options_after"]

FLAGS: bidict[FlagStr, core.QCommandLineOption.Flag] = bidict(
    hidden_from_help=core.QCommandLineOption.Flag.HiddenFromHelp,
    short_option_style=core.QCommandLineOption.Flag.ShortOptionStyle,
    ignore_options_after=core.QCommandLineOption.Flag.IgnoreOptionsAfter,
)


class CommandLineOption(core.QCommandLineOption):
    """Defines a possible command-line option."""
