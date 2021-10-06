from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import InvalidParamError, bidict


mod = QtCore.QCommandLineParser
op = mod.OptionsAfterPositionalArgumentsMode

OPTIONS_AFTER_POS_ARG = bidict(
    options=op.ParseAsOptions,
    positional_arguments=op.ParseAsPositionalArguments,
)

OptionsAfterPosArgStr = Literal["options", "positional_arguments"]

SINGLE_DASH_WORD = bidict(
    compacted_short=mod.SingleDashWordOptionMode.ParseAsCompactedShortOptions,
    long=mod.SingleDashWordOptionMode.ParseAsLongOptions,
)

SingleDashWordStr = Literal["compacted_short", "long"]


class CommandLineParser(QtCore.QCommandLineParser):
    def set_single_dash_word_option_mode(self, mode: SingleDashWordStr):
        """Set the single dash word option mode.

        Args:
            mode: single dash word option mode

        Raises:
            InvalidParamError: single dash word option mode does not exist
        """
        if mode not in SINGLE_DASH_WORD:
            raise InvalidParamError(mode, SINGLE_DASH_WORD)
        self.setSingleDashWordOptionMode(SINGLE_DASH_WORD[mode])

    def set_options_after_positional_arguments_mode(self, mode: SingleDashWordStr):
        """Set the options after positional arguments mode.

        Args:
            mode: options after positional arguments mode

        Raises:
            InvalidParamError: options after positional arguments mode does not exist
        """
        if mode not in OPTIONS_AFTER_POS_ARG:
            raise InvalidParamError(mode, OPTIONS_AFTER_POS_ARG)
        self.setOptionsAfterPositionalArgumentsMode(OPTIONS_AFTER_POS_ARG[mode])

    def add_option(
        self,
        name: str,
        description: str | None = None,
        value_name: str | None = None,
        default_value: str | None = None,
    ) -> core.CommandLineOption:
        if description is None:
            description = ""
        if value_name is None:
            value_name = ""
        if default_value is None:
            default_value = ""
        option = core.CommandLineOption(name, description, value_name, default_value)
        self.addOption(option)
        return option
