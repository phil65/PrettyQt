from __future__ import annotations

import logging
import re
from typing import Callable

from prettyqt import gui


logger = logging.getLogger(__name__)

SEARCH_REGEX = re.compile(r"([^/]|\\/)+$")
SEARCH_FLAGS_REGEX = re.compile(r"([^/]|\\/)*?([^\\]/[biw]*)$")
REPLACE_REGEX = re.compile(
    r"""
    (?P<search>([^/]|\\/)*?[^\\])
    /
    (?P<replace>(([^/]|\\/)*[^\\])?)
    /
    (?P<flags>[abiw]*)
    $
""",
    re.VERBOSE,
)


class SearchAndReplaceMixin:
    textCursor: Callable
    find: Callable
    move_cursor: Callable
    setTextCursor: Callable

    def initialize_search_and_replace(self) -> None:
        self.search_buffer: str | None = None

    def search_and_replace(self, arg: str) -> None:
        """Main search and replace function.

        arg is a string with a vim-like s&r syntax (see the regexes below)
        """

        def generate_flags(flagstr: str) -> None:
            # self.search_flags is automatically generated and does not
            # need to be initialized in __init__()
            self.search_flags = gui.TextDocument.FindFlags()
            if "b" in flagstr:
                self.search_flags |= gui.TextDocument.FindBackward
            if "i" not in flagstr:
                self.search_flags |= gui.TextDocument.FindCaseSensitively
            if "w" in flagstr:
                self.search_flags |= gui.TextDocument.FindWholeWords

        if search_match := SEARCH_REGEX.match(arg):
            self.search_buffer = search_match[0]
            self.search_flags = gui.TextDocument.FindCaseSensitively
            self.search_next()
        elif search_flags_match := SEARCH_FLAGS_REGEX.match(arg):
            self.search_buffer, flags = search_flags_match[0].rsplit("/", 1)
            generate_flags(flags)
            self.search_next()
        elif replace_match := REPLACE_REGEX.match(arg):
            self.search_buffer = replace_match.group("search")
            generate_flags(replace_match.group("flags"))
            if "a" in replace_match.group("flags"):
                self._replace_all(replace_match.group("replace"))
            else:
                self._replace_next(replace_match.group("replace"))
        else:
            logger.error("Malformed search/replace expression")

    def _searching_backwards(self) -> bool:
        return bool(gui.TextDocument.FindBackward & self.search_flags)

    def search_next(self) -> None:
        """Go to the next string found.

        This does the same thing as running the same search-command again.
        """
        if self.search_buffer is None:
            logger.error("No previous searches")
            return
        temp_cursor = self.textCursor()
        found = self.find(self.search_buffer, self.search_flags)
        if not found:
            if not self.textCursor().atStart() or (
                self._searching_backwards() and not self.textCursor().atEnd()
            ):
                self.move_cursor("end" if self._searching_backwards() else "start")
                found = self.find(self.search_buffer, self.search_flags)
                if not found:
                    self.setTextCursor(temp_cursor)
                    logger.error("Text not found")
            else:
                self.setTextCursor(temp_cursor)
                logger.error("Text not found")

    def _replace_next(self, replace_buffer: str) -> None:
        """Go to the next string found and replace it with replace_buffer.

        While this technically can be called from outside this class, it is
        not recommended (and most likely needs some modifications of the code.)
        """
        if self.search_buffer is None:
            logger.error("No previous searches")
            return
        temp_cursor = self.textCursor()
        found = self.find(self.search_buffer, self.search_flags)
        if not found:
            if not self.textCursor().atStart() or (
                self._searching_backwards() and not self.textCursor().atEnd()
            ):
                self.move_cursor("end" if self._searching_backwards() else "start")
                found = self.find(self.search_buffer, self.search_flags)
                if not found:
                    self.setTextCursor(temp_cursor)
        if found:
            t = self.textCursor()
            t.insertText(replace_buffer)
            length = len(replace_buffer)
            t.setPosition(t.position() - length)
            t.setPosition(t.position() + length, gui.TextCursor.MoveMode.KeepAnchor)
            self.setTextCursor(t)
            logger.info(
                f"Replaced on line {t.blockNumber()}, " f"pos {t.positionInBlock()}"
            )
        else:
            logger.error("Text not found")

    def _replace_all(self, replace_buffer: str) -> None:
        """Replace all strings found with the replace_buffer.

        As with replace_next, you probably don't want to call this manually.
        """
        if self.search_buffer is None:
            logger.error("No previous searches")
            return
        temp_cursor = self.textCursor()
        times = 0
        self.move_cursor("start")
        while True:
            if self.find(self.search_buffer, self.search_flags):
                self.textCursor().insertText(replace_buffer)
                times += 1
            else:
                break
        if times:
            logger.info(f'{times} instance{"s" if times else ""} replaced')
        else:
            logger.error("Text not found")
        self.setTextCursor(temp_cursor)
