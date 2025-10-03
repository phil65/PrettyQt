from __future__ import annotations

import contextlib
import os
import pathlib
from typing import TYPE_CHECKING, Literal

import qstylizer.parser
import qstylizer.style

from prettyqt import constants, core, gui
from prettyqt.utils import bidict, get_repr


if TYPE_CHECKING:
    from collections.abc import Iterator

    from prettyqt.utils import datatypes


MarkdownFeatureStr = Literal["no_html", "commonmark", "github"]

MARKDOWN_FEATURES: bidict[MarkdownFeatureStr, gui.QTextDocument.MarkdownFeature] = bidict(
    no_html=gui.QTextDocument.MarkdownFeature.MarkdownNoHTML,
    commonmark=gui.QTextDocument.MarkdownFeature.MarkdownDialectCommonMark,
    github=gui.QTextDocument.MarkdownFeature.MarkdownDialectGitHub,
)

ResourceTypeStr = Literal["unknown", "html", "image", "stylesheet", "markdown", "user"]

RESOURCE_TYPES: bidict[ResourceTypeStr, gui.QTextDocument.ResourceType] = bidict(
    unknown=gui.QTextDocument.ResourceType.UnknownResource,
    html=gui.QTextDocument.ResourceType.HtmlResource,
    image=gui.QTextDocument.ResourceType.ImageResource,
    stylesheet=gui.QTextDocument.ResourceType.StyleSheetResource,
    markdown=gui.QTextDocument.ResourceType.MarkdownResource,
    user=gui.QTextDocument.ResourceType.UserResource,
)

StackStr = Literal["undo", "redo", "undo_and_redo"]

STACKS: bidict[StackStr, gui.QTextDocument.Stacks] = bidict(
    undo=gui.QTextDocument.Stacks.UndoStack,
    redo=gui.QTextDocument.Stacks.RedoStack,
    undo_and_redo=gui.QTextDocument.Stacks.UndoAndRedoStacks,
)

FindFlagStr = Literal["backward", "case_sensitive", "whole_words"]

FIND_FLAGS: bidict[FindFlagStr, gui.QTextDocument.FindFlag] = bidict(
    backward=gui.QTextDocument.FindFlag.FindBackward,
    case_sensitive=gui.QTextDocument.FindFlag.FindCaseSensitively,
    whole_words=gui.QTextDocument.FindFlag.FindWholeWords,
)

MetaInformationStr = Literal["document_title", "document_url", "css_media"]

META_INFORMATION: bidict[MetaInformationStr, gui.QTextDocument.MetaInformation] = bidict(
    document_title=gui.QTextDocument.MetaInformation.DocumentTitle,
    document_url=gui.QTextDocument.MetaInformation.DocumentUrl,
    css_media=gui.QTextDocument.MetaInformation.CssMedia,
)


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
        # starts with 0-index
        block = self.findBlockByNumber(number)
        if not block.isValid():
            msg = f"{number} not a valid block index. Block count: {self.blockCount()}"
            raise ValueError(msg)
        return gui.TextBlock(block)

    def find_block_by_line_number(self, line_number: int) -> gui.TextBlock:
        # starts with 0-index
        block = self.findBlockByLineNumber(line_number)
        if not block.isValid():
            msg = f"{line_number} not a valid line index. Line count: {self.lineCount()}"
            raise ValueError(msg)
        return gui.TextBlock(block)

    def set_text(self, text: str):
        self.setPlainText(text)

    def get_base_url(self) -> core.Url:
        return core.Url(self.baseUrl())

    def get_default_font(self) -> gui.Font:
        return gui.Font(self.defaultFont())

    def set_default_text_option(self, opt: gui.QTextOption):
        self.setDefaultTextOption(gui.TextOption(opt))

    def get_default_text_option(self) -> gui.TextOption:
        return gui.TextOption(self.defaultTextOption())

    def clear_stacks(self, stack: StackStr | gui.QTextDocument.Stacks):
        """Clear undo / redo stack.

        Args:
            stack: stack to clear
        """
        self.clearUndoRedoStacks(STACKS.get_enum_value(stack))

    def set_default_cursor_move_style(
        self, style: constants.CursorMoveStyleStr | constants.CursorMoveStyle
    ):
        """Set the cursor move style.

        Args:
            style: cursor move style
        """
        self.setDefaultCursorMoveStyle(constants.CURSOR_MOVE_STYLE.get_enum_value(style))

    def get_default_cursor_move_style(self) -> constants.CursorMoveStyleStr:
        """Return current cursor move style.

        Returns:
            cursor move style
        """
        return constants.CURSOR_MOVE_STYLE.inverse[self.defaultCursorMoveStyle()]

    def set_meta_information(
        self, info: MetaInformationStr | gui.QTextDocument.MetaInformation, value: str
    ):
        """Set meta information.

        Args:
            info: meta information type
            value: value to set
        """
        self.setMetaInformation(META_INFORMATION.get_enum_value(info), value)

    def get_meta_information(
        self, info: MetaInformationStr | gui.QTextDocument.MetaInformation
    ) -> str:
        """Return specififed meta information.

        Args:
            info: meta information type

        Returns:
            meta information
        """
        return self.metaInformation(META_INFORMATION.get_enum_value(info))

    def add_resource(
        self,
        resource_type: ResourceTypeStr | gui.QTextDocument.ResourceType,
        name: datatypes.PathType,
        resource,
    ):
        url = core.Url(name)
        self.addResource(RESOURCE_TYPES.get_enum_value(resource_type), url, resource)

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
        fmt: gui.textdocumentwriter.FormatStr | bytes | core.QByteArray = "plaintext",
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
        flag = gui.QTextOption.Flag.ShowTabsAndSpaces
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
        line_count = self.document().blockCount()
        font_metrics = gui.FontMetrics(self.defaultFont())
        return (max(line_count, 1) * font_metrics.height()) + self.documentMargin()


class TextDocument(TextDocumentMixin, gui.QTextDocument):
    pass


if __name__ == "__main__":
    doc = TextDocument("This is a test\nHello")
    doc.set_default_text_option(gui.QTextOption())
    a = doc.get_bytes()
    print(a)
