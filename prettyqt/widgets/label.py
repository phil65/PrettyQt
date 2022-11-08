from __future__ import annotations

import os
from typing import Literal

from prettyqt import constants, gui, widgets
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import InvalidParamError, bidict, colors, helpers, types


TEXT_INTERACTION = bidict(
    none=QtCore.Qt.TextInteractionFlag.NoTextInteraction,
    by_mouse=QtCore.Qt.TextInteractionFlag.TextSelectableByMouse,
    by_keyboard=QtCore.Qt.TextInteractionFlag.TextSelectableByKeyboard,
    accessible_by_mouse=QtCore.Qt.TextInteractionFlag.LinksAccessibleByMouse,
    accessible_by_keyboard=QtCore.Qt.TextInteractionFlag.LinksAccessibleByKeyboard,
    text_editable=QtCore.Qt.TextInteractionFlag.TextEditable,
    like_text_editor=QtCore.Qt.TextInteractionFlag.TextEditorInteraction,
    like_text_browser=QtCore.Qt.TextInteractionFlag.TextBrowserInteraction,
)

TextInteractionStr = Literal[
    "none",
    "by_mouse",
    "by_keyboard",
    "accessible_by_mouse",
    "accessible_by_keyboard",
    "text_editable",
    "like_text_editor",
    "like_text_browser",
]

TEXT_FORMAT = bidict(
    rich=QtCore.Qt.TextFormat.RichText,
    plain=QtCore.Qt.TextFormat.PlainText,
    auto=QtCore.Qt.TextFormat.AutoText,
    markdown=QtCore.Qt.TextFormat.MarkdownText,
)


TextFormatStr = Literal["rich", "plain", "auto", "markdown"]


QtWidgets.QLabel.__bases__ = (widgets.Frame,)


class Label(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.openExternalLinks()

    def __repr__(self):
        return f"{type(self).__name__}({self.text()!r})"

    def serialize_fields(self):
        pixmap = gui.Pixmap(self.pixmap())
        return dict(
            text=self.text(),
            scaled_contents=self.hasScaledContents(),
            indent=self.indent(),
            margin=self.margin(),
            text_format=self.get_text_format(),
            pixmap=pixmap if pixmap else None,
            open_external_links=self.openExternalLinks(),
            has_selected_text=self.hasSelectedText(),
            selected_text=self.selectedText(),
            alignment=(self.get_horizontal_alignment(), self.get_vertical_alignment()),
            word_wrap=self.wordWrap(),
            text_interaction_flags=self.get_text_interaction(),
        )

    def __setstate__(self, state):
        self.setText(state.get("text", ""))
        self.setIndent(state.get("indent", -1))
        self.setMargin(state.get("margin", 0))
        self.setWordWrap(state.get("word_wrap", 0))
        self.set_text_format(state.get("text_format", 0))
        # self.setPixmap(state.get("pixmap"))
        self.setOpenExternalLinks(state.get("open_external_links", False))
        self.set_alignment(*state.get("alignment"))
        self.setScaledContents(state["scaled_contents"])
        self.setWordWrap(state["word_wrap"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def allow_links(self) -> Label:
        # self.setText("<a href=\"http://example.com/\">Click Here!</a>")
        self.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.setTextInteractionFlags(
            QtCore.Qt.TextInteractionFlag.TextBrowserInteraction  # type: ignore
        )
        self.setOpenExternalLinks(True)
        return self

    def set_alignment(
        self,
        horizontal: constants.HorizontalAlignmentStr | None = None,
        vertical: constants.VerticalAlignmentStr | None = None,
    ):
        """Set the alignment of the label's contents."""
        if horizontal is None and vertical is not None:
            flag = constants.V_ALIGNMENT[vertical]
        elif vertical is None and horizontal is not None:
            flag = constants.H_ALIGNMENT[horizontal]
        elif vertical is not None and horizontal is not None:
            flag = constants.V_ALIGNMENT[vertical] | constants.H_ALIGNMENT[horizontal]
        else:
            return
        self.setAlignment(flag)
        return self

    def get_horizontal_alignment(self) -> constants.HorizontalAlignmentStr:
        align = self.alignment()
        if align & constants.ALIGN_RIGHT:  # type: ignore
            return "right"
        elif align & constants.ALIGN_H_CENTER:  # type: ignore
            return "center"
        elif align & constants.ALIGN_JUSTIFY:  # type: ignore
            return "justify"
        else:
            return "left"

    def get_vertical_alignment(self) -> constants.VerticalAlignmentStr:
        align = self.alignment()
        if align & constants.ALIGN_TOP:  # type: ignore
            return "top"
        elif align & constants.ALIGN_BOTTOM:  # type: ignore
            return "bottom"
        elif align & constants.ALIGN_BASELINE:  # type: ignore
            return "baseline"
        else:
            return "center"

    def set_indent(self, indent: int) -> Label:
        """Set the label's text indent in pixels."""
        self.setIndent(indent)
        return self

    def set_text_format(self, text_format: TextFormatStr) -> Label:
        """Set the text format.

        Args:
            text_format: text format to use

        Raises:
            InvalidParamError: text format does not exist
        """
        if text_format not in TEXT_FORMAT:
            raise InvalidParamError(text_format, TEXT_FORMAT)
        self.setTextFormat(TEXT_FORMAT[text_format])
        return self

    def get_text_format(self) -> TextFormatStr:
        """Return current text format.

        Returns:
            text format
        """
        return TEXT_FORMAT.inverse[self.textFormat()]

    def set_text_interaction(self, *types: TextInteractionStr) -> Label:
        """Set the text interaction mode.

        Args:
            types: text interaction mode to use

        Raises:
            InvalidParamError: text interaction mode does not exist
        """
        for item in types:
            if item not in TEXT_INTERACTION:
                raise InvalidParamError(item, TEXT_INTERACTION)
        flags = helpers.merge_flags(types, TEXT_INTERACTION)
        self.setTextInteractionFlags(flags)
        return self

    def get_text_interaction(self) -> list[TextInteractionStr]:
        """Return current text interaction mode.

        Returns:
            list of text interaction modes
        """
        return [k for k, v in TEXT_INTERACTION.items() if v & self.textInteractionFlags()]

    def set_text(self, text: str) -> Label:
        """Set the label's text."""
        self.setText(text)
        return self

    def set_bold(self, bold: bool = True) -> Label:
        font = self.font()
        font.setBold(bold)
        self.setFont(font)
        return self

    def set_italic(self, italic: bool = True) -> Label:
        font = self.font()
        font.setItalic(italic)
        self.setFont(font)
        return self

    def set_point_size(self, size: int) -> Label:
        font = self.font()
        font.setPointSize(size)
        self.setFont(font)
        return self

    def set_weight(self, weight: gui.font.WeightStr) -> Label:
        """Set the font weight.

        Args:
            weight: font weight

        Raises:
            InvalidParamError: invalid font weight
        """
        if weight not in gui.font.WEIGHT:
            raise InvalidParamError(weight, gui.font.WEIGHT)
        font = self.font()
        font.setWeight(gui.font.WEIGHT[weight])
        self.setFont(font)
        return self

    def set_color(self, color: types.ColorType) -> Label:
        with self.edit_stylesheet() as ss:
            if color is None:
                ss.color.setValue("")
            else:
                color = colors.get_color(color)
                ss.color.setValue(color.name())
        return self

    def set_image(self, path: types.PathType, width: int = 300) -> Label:
        self.setScaledContents(True)
        self.set_alignment(horizontal="center")
        self.setText(
            "<html><head/><body><p>"
            f"<img src={os.fspath(path)!r} width={str(width)!r}/>"
            "</p></body></html>"
        )
        return self

    @classmethod
    def image_from_path(
        cls, path: types.PathType, parent: QtWidgets.QWidget | None = None
    ) -> Label:
        pixmap = gui.Pixmap.from_file(path)
        label = cls(parent=parent)
        label.setPixmap(pixmap)
        label.resize(pixmap.width(), pixmap.height())
        return label


if __name__ == "__main__":
    app = widgets.app()
    widget = Label("http://www.test.de")
    widget.show()
    app.main_loop()
