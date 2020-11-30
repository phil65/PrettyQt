# -*- coding: utf-8 -*-

from typing import Optional

from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import bidict, InvalidParamError

OPTIONS_AFTER_POS_ARG = bidict(
    options=QtCore.QCommandLineParser.ParseAsOptions,
    positional_arguments=QtCore.QCommandLineParser.ParseAsPositionalArguments,
)

SINGLE_DASH_WORD = bidict(
    compacted_short=QtCore.QCommandLineParser.ParseAsCompactedShortOptions,
    long=QtCore.QCommandLineParser.ParseAsLongOptions,
)


class CommandLineParser(QtCore.QCommandLineParser):
    def set_single_dash_word_option_mode(self, mode: str):
        """Set the single dash word option mode.

        Allowed values are "compacted_short", "long"

        Args:
            mode: single dash word option mode

        Raises:
            InvalidParamError: single dash word option mode does not exist
        """
        if mode not in SINGLE_DASH_WORD:
            raise InvalidParamError(mode, SINGLE_DASH_WORD)
        self.setSingleDashWordOptionMode(SINGLE_DASH_WORD[mode])

    def set_options_after_positional_arguments_mode(self, mode: str):
        """Set the options after positional arguments mode.

        Allowed values are "options", "positional_arguments"

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
        description: Optional[str] = None,
        value_name: Optional[str] = None,
        default_value: Optional[str] = None,
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
