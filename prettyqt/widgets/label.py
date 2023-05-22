from __future__ import annotations

import os
from typing import Literal

from typing_extensions import Self

from prettyqt import constants, core, gui, widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets
from prettyqt.utils import InvalidParamError, bidict, colors, datatypes, get_repr


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


class Label(widgets.FrameMixin, QtWidgets.QLabel):
    elision_changed = core.Signal(bool)
    clicked = core.Signal()

    def __init__(self, *args, **kwargs):
        self._elide_mode = QtCore.Qt.TextElideMode.ElideNone
        super().__init__(*args, **kwargs)
        self.openExternalLinks()
        self._is_elided = False

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent):
        if ev.button() == QtCore.Qt.MouseButton.LeftButton:
            self.clicked.emit()
        return super().mouseReleaseEvent(ev)

    def set_elide_mode(self, mode: constants.ElideModeStr):
        self._elide_mode = constants.ELIDE_MODE[mode]
        self.update()

    def get_elide_mode(self) -> constants.ElideModeStr:
        return constants.ELIDE_MODE.inverse[self._elide_mode]

    def _get_map(self):
        maps = super()._get_map()
        maps |= {"textFormat": TEXT_FORMAT, "alignment": constants.ALIGNMENTS}
        return maps

    def __repr__(self):
        return get_repr(self, self.text())

    # # adapted from https://forum.qt.io/topic/24530/solved-shortening-a-label/3
    # def minimumSizeHint(self):
    #     if self._elide_mode != QtCore.Qt.TextElideMode.ElideNone:
    #         # TODO: tweak sizeHint
    #         # -> text should expand if user increases window size,
    #         #    but don't automatically adapt window size to label width on UI update!
    #         #    (somehow calculate minimumSizeHint + sizeHint with font metrics???)
    #         fm = self.fontMetrics()
    #         size = QtCore.QSize(fm.width("..."), fm.height())
    #         return size
    #     else:
    #         size = self.minimumSizeHint()
    #         return QtCore.QSize(size.width() + 13, size.height())

    # # adapted from https://www.mimec.org/blog/status-bar-and-elided-label
    # def paintEvent(self, event):
    #     with gui.Painter(self) as painter:
    #         self.drawFrame(painter)

    #         rect = self.contentsRect()
    #         rect.adjust(self.margin(), self.margin(), -self.margin(), -self.margin())

    #         elided_text = painter.fontMetrics().elidedText(
    #             self.text(), self._elide_mode, rect.width()
    #         )

    #         style_option = QtWidgets.QStyleOption()
    #         style_option.initFrom(self)

    #         self.style().drawItemText(
    #             painter,
    #             rect,
    #             self.alignment(),
    #             style_option.palette,
    #             self.isEnabled(),
    #             elided_text,
    #             self.foregroundRole(),
    #         )

    def paintEvent(self, event):
        if self._elide_mode == QtCore.Qt.TextElideMode.ElideNone:
            super().paintEvent(event)
            return
        did_elide = False

        with gui.Painter(self) as painter:
            font_metrics = painter.fontMetrics()
            text_lines = self.text().split("\n")
            text_width = font_metrics.horizontalAdvance(self.text())
            line_spacing = font_metrics.lineSpacing()

            # layout phase
            text_layout = gui.TextLayout(self.text(), painter.font())
            current_y = 0
            with text_layout.process_layout():
                for line in text_lines:
                    text_width = font_metrics.horizontalAdvance(line)
                    # if self.height() >= next_line_y + line_spacing:
                    #     line.draw(painter, core.PointF(0, y))
                    #     y = next_line_y
                    # else:
                    #     last_line = self._text[line.textStart() :]
                    #     elided_line = metrics.elided_text(
                    #         last_line, "right", self.width()
                    #     )
                    #     painter.drawText(0, y + metrics.ascent(), elided_line)
                    #     line = layout.createLine()
                    #     did_elide = line.isValid()
                    #     break
                    if text_width >= self.width():
                        elided_line = font_metrics.elidedText(
                            line, self._elide_mode, self.width()
                        )
                        painter.drawText(
                            QtCore.QRect(0, current_y, self.width(), self.height()),
                            int(self.alignment()),
                            elided_line,
                        )
                        did_elide = True
                    else:
                        painter.drawText(
                            QtCore.QRect(0, current_y, self.width(), self.height()),
                            int(self.alignment()),
                            line,
                        )
                    current_y += line_spacing

            if did_elide != self._is_elided:
                self._is_elided = did_elide
                self.elision_changed.emit(did_elide)

    def allow_links(self) -> Label:
        # self.setText("<a href=\"http://example.com/\">Click Here!</a>")
        self.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextBrowserInteraction)
        self.setOpenExternalLinks(True)
        return self

    def set_alignment(
        self,
        horizontal: constants.HorizontalAlignmentStr | None = None,
        vertical: constants.VerticalAlignmentStr | None = None,
    ):
        """Set the alignment of the label's contents."""
        match horizontal, vertical:
            case None, None:
                return self
            case None, _:
                flag = constants.V_ALIGNMENT[vertical]
            case _, None:
                flag = constants.H_ALIGNMENT[horizontal]
            case _, _:
                flag = constants.V_ALIGNMENT[vertical] | constants.H_ALIGNMENT[horizontal]
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
        flags = TEXT_INTERACTION.merge_flags(types)
        self.setTextInteractionFlags(flags)
        return self

    def get_text_interaction(self) -> list[TextInteractionStr]:
        """Return current text interaction mode.

        Returns:
            list of text interaction modes
        """
        return TEXT_INTERACTION.get_list(self.textInteractionFlags())

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

    def set_color(self, color: datatypes.ColorType) -> Label:
        with self.edit_stylesheet() as ss:
            if color is None:
                ss.color.setValue("")
            else:
                color = colors.get_color(color)
                ss.color.setValue(color.name())
        return self

    def set_image(self, path: datatypes.PathType, width: int = 300) -> Label:
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
        cls, path: datatypes.PathType, parent: QtWidgets.QWidget | None = None
    ) -> Self:
        pixmap = gui.Pixmap.from_file(path)
        label = cls(parent=parent)
        label.setPixmap(pixmap)
        label.resize(pixmap.width(), pixmap.height())
        return label

    elideMode = core.Property(str, get_elide_mode, set_elide_mode)


if __name__ == "__main__":
    app = widgets.app()
    widget = Label("http://www.test.fsdfsdfsfdsfsfdsfde\n" * 20, elide_mode="right")
    widget.show()
    app.main_loop()
