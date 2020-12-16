import pathlib
from typing import Iterator, Literal, Union

from qtpy import QtGui

from prettyqt import constants, core, gui
from prettyqt.utils import InvalidParamError, bidict


if core.VersionNumber.get_qt_version() >= (5, 14, 0):
    MARKDOWN_FEATURES = bidict(
        no_html=QtGui.QTextDocument.MarkdownNoHTML,
        commonmark=QtGui.QTextDocument.MarkdownDialectCommonMark,
        github=QtGui.QTextDocument.MarkdownDialectGitHub,
    )

MarkdownFeatureStr = Literal["no_html", "commonmark", "github"]

RESOURCE_TYPES = bidict(
    unknown=QtGui.QTextDocument.UnknownResource,
    html=QtGui.QTextDocument.HtmlResource,
    image=QtGui.QTextDocument.ImageResource,
    stylesheet=QtGui.QTextDocument.StyleSheetResource,
    markdown=QtGui.QTextDocument.MarkdownResource,
    user=QtGui.QTextDocument.UserResource,
)

ResourceTypeStr = Literal["unknown", "html", "image", "stylesheet", "markdown", "user"]

STACKS = bidict(
    undo=QtGui.QTextDocument.UndoStack,
    redo=QtGui.QTextDocument.RedoStack,
    undo_and_redo=QtGui.QTextDocument.UndoAndRedoStacks,
)

StackStr = Literal["undo", "redo", "undo_and_redo"]

QtGui.QTextDocument.__bases__ = (core.Object,)


class TextDocument(QtGui.QTextDocument):
    def __getitem__(self, index: int) -> gui.TextBlock:
        return gui.TextBlock(self.findBlockByNumber(index))

    def __len__(self) -> int:
        return self.blockCount()

    def __iter__(self) -> Iterator[gui.TextBlock]:
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

    def add_resource(
        self, resource_type: ResourceTypeStr, name: Union[str, pathlib.Path], resource
    ):
        if resource_type not in RESOURCE_TYPES:
            raise InvalidParamError(resource_type, RESOURCE_TYPES)
        url = core.Url(name)
        self.addResource(RESOURCE_TYPES[resource_type], url, resource)


if __name__ == "__main__":
    doc = TextDocument("This is a test\nHello")
    for i in doc:
        print(i)
