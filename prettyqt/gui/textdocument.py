from __future__ import annotations

from collections.abc import Iterator
import contextlib
import os
import pathlib
from typing import Literal

import qstylizer.parser
import qstylizer.style

from prettyqt import constants, core, gui
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import InvalidParamError, bidict, datatypes, get_repr


MARKDOWN_FEATURES = bidict(
    no_html=QtGui.QTextDocument.MarkdownFeature.MarkdownNoHTML,
    commonmark=QtGui.QTextDocument.MarkdownFeature.MarkdownDialectCommonMark,
    github=QtGui.QTextDocument.MarkdownFeature.MarkdownDialectGitHub,
)

MarkdownFeatureStr = Literal["no_html", "commonmark", "github"]

RESOURCE_TYPES = bidict(
    unknown=QtGui.QTextDocument.ResourceType.UnknownResource,
    html=QtGui.QTextDocument.ResourceType.HtmlResource,
    image=QtGui.QTextDocument.ResourceType.ImageResource,
    stylesheet=QtGui.QTextDocument.ResourceType.StyleSheetResource,
    markdown=QtGui.QTextDocument.ResourceType.MarkdownResource,
    user=QtGui.QTextDocument.ResourceType.UserResource,
)

ResourceTypeStr = Literal["unknown", "html", "image", "stylesheet", "markdown", "user"]

STACKS = bidict(
    undo=QtGui.QTextDocument.Stacks.UndoStack,
    redo=QtGui.QTextDocument.Stacks.RedoStack,
    undo_and_redo=QtGui.QTextDocument.Stacks.UndoAndRedoStacks,
)

StackStr = Literal["undo", "redo", "undo_and_redo"]

FIND_FLAGS = bidict(
    backward=QtGui.QTextDocument.FindFlag.FindBackward,
    case_sensitive=QtGui.QTextDocument.FindFlag.FindCaseSensitively,
    whole_words=QtGui.QTextDocument.FindFlag.FindWholeWords,
)

FindFlagStr = Literal["backward", "case_sensitive", "whole_words"]

META_INFORMATION = bidict(
    document_title=QtGui.QTextDocument.MetaInformation.DocumentTitle,
    document_url=QtGui.QTextDocument.MetaInformation.DocumentUrl,
    css_media=QtGui.QTextDocument.MetaInformation.CssMedia,
)

MetaInformationStr = Literal["document_title", "document_url", "css_media"]


class TextDocumentMixin(core.ObjectMixin):
    def __getitem__(self, index: int) -> gui.TextBlock:
        return gui.TextBlock(self.findBlockByNumber(index))

    def __len__(self) -> int:
        return self.blockCount()

    def __iter__(self) -> Iterator[gui.TextBlock]:
        return iter(
            gui.TextBlock(self.findBlockByNumber(i)) for i in range(self.blockCount())
        )

    def __repr__(self):
        return get_repr(self, self.toPlainText())

    def get_first_block(self) -> gui.TextBlock:
        return gui.TextBlock(self.firstBlock())

    def get_last_block(self) -> gui.TextBlock:
        return gui.TextBlock(self.lastBlock())

    def find_block_by_number(self, number: int) -> gui.TextBlock:
        block = self.findBlockByNumber(number)
        if not block.isValid():
            raise ValueError(
                f"{number} not a valid block index. Block count: {self.blockCount()}"
            )
        return gui.TextBlock(block)

    def find_block_by_line_number(self, line_number: int) -> gui.TextBlock:
        block = self.findBlockByLineNumber(line_number)
        if not block.isValid():
            raise ValueError(
                f"{line_number} not a valid line index. Line count: {self.lineCount()}"
            )
        return gui.TextBlock(block)

    def set_text(self, text: str):
        self.setPlainText(text)

    def get_base_url(self) -> core.Url:
        return core.Url(self.baseUrl())

    def get_default_font(self) -> gui.Font:
        return gui.Font(self.defaultFont())

    def set_default_text_option(self, opt: QtGui.QTextOption):
        self.setDefaultTextOption(gui.TextOption(opt))

    def get_default_text_option(self) -> gui.TextOption:
        return gui.TextOption(self.defaultTextOption())

    def set_flags(self, **flags):
        current = self.flags()
        for k, v in flags.items():
            if v:
                current |= gui.textoption.FLAG[k]
            else:
                current &= ~gui.textoption.FLAG[k]
        self.setFlags(current)
        # if show:
        #     self.setFlags(self.flags() | QtGui.QTextOption.ShowTabsAndSpaces)
        # else:
        #     self.setFlags(self.flags() & ~QtGui.QTextOption.ShowTabsAndSpaces)

    def clear_stacks(self, stack: StackStr):
        """Clear undo / redo stack.

        Args:
            stack: stack to clear

        Raises:
            InvalidParamError: stack type does not exist
        """
        if stack not in STACKS:
            raise InvalidParamError(stack, STACKS)
        self.clearUndoRedoStacks(STACKS[stack])

    def set_default_cursor_move_style(self, style: constants.CursorMoveStyleStr):
        """Set the cursor move style.

        Args:
            style: cursor move style

        Raises:
            InvalidParamError: cursor move style does not exist
        """
        if style not in constants.CURSOR_MOVE_STYLE:
            raise InvalidParamError(style, constants.CURSOR_MOVE_STYLE)
        self.setDefaultCursorMoveStyle(constants.CURSOR_MOVE_STYLE[style])

    def get_default_cursor_move_style(self) -> constants.CursorMoveStyleStr:
        """Return current cursor move style.

        Returns:
            cursor move style
        """
        return constants.CURSOR_MOVE_STYLE.inverse[self.defaultCursorMoveStyle()]

    def set_meta_information(self, info: MetaInformationStr, value: str):
        """Set meta information.

        Args:
            info: meta information type
            value: value to set

        Raises:
            InvalidParamError: meta information type does not exist
        """
        if info not in META_INFORMATION:
            raise InvalidParamError(info, META_INFORMATION)
        self.setMetaInformation(META_INFORMATION[info], value)

    def get_meta_information(self, info: MetaInformationStr) -> str:
        """Return specififed meta information.

        Args:
            info: meta information type

        Returns:
            meta information
        """
        if info not in META_INFORMATION:
            raise InvalidParamError(info, META_INFORMATION)
        return self.metaInformation(META_INFORMATION[info])

    def add_resource(
        self, resource_type: ResourceTypeStr, name: datatypes.PathType, resource
    ):
        if resource_type not in RESOURCE_TYPES:
            raise InvalidParamError(resource_type, RESOURCE_TYPES)
        url = core.Url(name)
        self.addResource(RESOURCE_TYPES[resource_type], url, resource)

    @contextlib.contextmanager
    def edit_default_stylesheet(self) -> Iterator[qstylizer.style.StyleSheet]:
        ss = self.get_default_stylesheet()
        yield ss
        self.set_default_stylesheet(ss)

    def set_default_stylesheet(
        self, ss: None | qstylizer.style.StyleSheet | datatypes.PathType
    ):
        match ss:
            case os.PathLike():
                ss = pathlib.Path(ss).read_text()
            case None:
                ss = ""
            case qstylizer.style.StyleSheet():
                pass
            case _:
                raise TypeError(ss)
        self.setDefaultStyleSheet(str(ss))

    def get_default_stylesheet(self) -> qstylizer.style.StyleSheet:
        return qstylizer.parser.parse(self.defaultStyleSheet())

    def find_line_position(self, line_no: int) -> int:
        """Return index of the TextBlock corresponding to given line number."""
        lines = self.blockCount()
        assert 1 <= line_no <= lines
        return self.findBlockByLineNumber(line_no - 1).position()

    def write_to_file(
        self,
        path: datatypes.PathType,
        fmt: gui.textdocumentwriter.FormatStr | bytes | QtCore.QByteArray = "plaintext",
    ) -> bool:
        writer = gui.TextDocumentWriter()
        writer.set_format(fmt)
        writer.set_file_name(path)
        return writer.write(self)

    def get_bytes(
        self, fmt: Literal["plaintext", "HTML", "markdown", "ODF"] = "ODF"
    ) -> bytes:
        return gui.TextDocumentWriter.serialize_document(self, fmt)

    def show_whitespace_and_tabs(self, show: bool):
        """Set show white spaces flag."""
        options = self.get_default_text_option()
        flag = QtGui.QTextOption.Flag.ShowTabsAndSpaces
        if show:
            options.setFlags(options.flags() | flag)
        else:
            options.setFlags(options.flags() & ~flag)
        self.setDefaultTextOption(options)

    def get_pixel_height(self, exact: bool = True) -> int:
        if exact:  # sourcery skip: extract-method
            layout = self.documentLayout()
            h = 0
            b = self.begin()
            while b != self.end():
                h += layout.blockBoundingRect(b).height()
                b = b.next()
            h += self.documentMargin()
            return h
        else:
            line_count = self.document().blockCount()
            font_metrics = gui.FontMetrics(self.defaultFont())
            return (max(line_count, 1) * font_metrics.height()) + self.documentMargin()


class TextDocument(TextDocumentMixin, QtGui.QTextDocument):
    pass


if __name__ == "__main__":
    doc = TextDocument("This is a test\nHello")
    doc.set_default_text_option(QtGui.QTextOption())
    a = doc.get_bytes()
    print(a)
