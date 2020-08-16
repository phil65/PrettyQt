# -*- coding: utf-8 -*-

from typing import Union
import pathlib

from qtpy import QtGui, QtCore

from prettyqt import core, gui
from prettyqt.utils import bidict, InvalidParamError

if core.VersionNumber.get_qt_version() >= (5, 14, 0):
    MARKDOWN_FEATURES = bidict(
        no_html=QtGui.QTextDocument.MarkdownNoHTML,
        commonmark=QtGui.QTextDocument.MarkdownDialectCommonMark,
        github=QtGui.QTextDocument.MarkdownDialectGitHub,
    )

RESOURCE_TYPES = bidict(
    unknown=QtGui.QTextDocument.UnknownResource,
    html=QtGui.QTextDocument.HtmlResource,
    image=QtGui.QTextDocument.ImageResource,
    stylesheet=QtGui.QTextDocument.StyleSheetResource,
    markdown=QtGui.QTextDocument.MarkdownResource,
    user=QtGui.QTextDocument.UserResource,
)

STACKS = bidict(
    undo=QtGui.QTextDocument.UndoStack,
    redo=QtGui.QTextDocument.RedoStack,
    undo_and_redo=QtGui.QTextDocument.UndoAndRedoStacks,
)

CURSOR_MOVE_STYLES = bidict(
    logical=QtCore.Qt.LogicalMoveStyle, visual=QtCore.Qt.VisualMoveStyle
)

QtGui.QTextDocument.__bases__ = (core.Object,)


class TextDocument(QtGui.QTextDocument):
    def __getitem__(self, index: int):
        return gui.TextBlock(self.findBlockByNumber(index))

    def __len__(self) -> int:
        return self.blockCount()

    def __iter__(self):
        return iter(self[i] for i in range(self.blockCount()))

    def set_text(self, text: str):
        self.setPlainText(text)

    def serialize_fields(self):
        return dict(
            base_url=core.Url(self.baseUrl()),
            default_font=gui.Font(self.defaultFont()),
            default_stylesheet=self.defaultStyleSheet(),
            default_text_option=gui.TextOption(self.defaultTextOption()),
            document_margin=self.documentMargin(),
            maximum_block_count=self.maximumBlockCount(),
            is_modified=self.isModified(),
            page_size=self.pageSize(),
            text_width=self.textWidth(),
            indent_width=self.indentWidth(),
            undo_redo_enabled=self.isUndoRedoEnabled(),
            use_design_metrics=self.useDesignMetrics(),
        )

    def clear_stacks(self, stack: str):
        """Clear undo / redo stack.

        Allowed values are "undo", "redo", "undo_and_redo"

        Args:
            stack: stack to clear

        Raises:
            InvalidParamError: stack type does not exist
        """
        if stack not in STACKS:
            raise InvalidParamError(stack, STACKS)
        self.clearUndoRedoStacks(STACKS[stack])

    def set_default_cursor_move_style(self, style: str):
        """Set the cursor move style.

        Allowed values are "logical", "visual"

        Args:
            style: cursor move style

        Raises:
            InvalidParamError: cursor move style does not exist
        """
        if style not in CURSOR_MOVE_STYLES:
            raise InvalidParamError(style, CURSOR_MOVE_STYLES)
        self.setDefaultCursorMoveStyle(CURSOR_MOVE_STYLES[style])

    def get_default_cursor_move_style(self) -> str:
        """Return current cursor move style.

        Possible values: "logical", "visual"

        Returns:
            cursor move style
        """
        return CURSOR_MOVE_STYLES.inv[self.defaultCursorMoveStyle()]

    def add_resource(self, resource_type: str, name: Union[str, pathlib.Path], resource):
        if resource_type not in RESOURCE_TYPES:
            raise InvalidParamError(resource_type, RESOURCE_TYPES)
        url = core.Url(name)
        self.addResource(RESOURCE_TYPES[resource_type], url, resource)


if __name__ == "__main__":
    doc = TextDocument("This is a test\nHello")
    for i in doc:
        print(i)
