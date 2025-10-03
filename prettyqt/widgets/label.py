from __future__ import annotations

import os
from typing import TYPE_CHECKING, Self

from prettyqt import constants, core, gui, widgets
from prettyqt.utils import colors, get_repr


if TYPE_CHECKING:
    from prettyqt.utils import datatypes


class Label(widgets.FrameMixin, widgets.QLabel):
    """Text or image display."""

    elision_changed = core.Signal(bool)
    clicked = core.Signal()

    def __init__(self, *args, **kwargs):
        self._elide_mode = constants.TextElideMode.ElideNone
        super().__init__(*args, **kwargs)
        self.openExternalLinks()
        self._is_elided = False

    def mouseReleaseEvent(self, ev: gui.QMouseEvent):
        if ev.button() == constants.MouseButton.LeftButton:
            self.clicked.emit()
        return super().mouseReleaseEvent(ev)

    def set_elide_mode(self, mode: constants.TextElideModeStr):
        self._elide_mode = constants.TEXT_ELIDE_MODE[mode]
        self.update()

    def get_elide_mode(self) -> constants.TextElideModeStr:
        return constants.TEXT_ELIDE_MODE.inverse[self._elide_mode]

    def _get_map(self):
        maps = super()._get_map()
        maps |= {"textFormat": constants.TEXT_FORMAT, "alignment": constants.ALIGNMENTS}
        return maps

    def __repr__(self):
        return get_repr(self, self.text())

    # # adapted from https://forum.qt.io/topic/24530/solved-shortening-a-label/3
    # def minimumSizeHint(self):
    #     if self._elide_mode != constants.TextElideMode.ElideNone:
    #         # TODO: tweak sizeHint
    #         # -> text should expand if user increases window size,
    #         #    but don't automatically adapt window size to label width on UI update!
    #         #    (somehow calculate minimumSizeHint + sizeHint with font metrics???)
    #         fm = self.fontMetrics()
    #         size = core.QSize(fm.width("..."), fm.height())
    #         return size
    #     else:
    #         size = self.minimumSizeHint()
    #         return core.QSize(size.width() + 13, size.height())

    # # adapted from https://www.mimec.org/blog/status-bar-and-elided-label
    # def paintEvent(self, event):
    #     with gui.Painter(self) as painter:
    #         self.drawFrame(painter)

    #         rect = self.contentsRect()
    #         rect.adjust(self.margin(), self.margin(), -self.margin(), -self.margin())

    #         elided_text = painter.fontMetrics().elidedText(
    #             self.text(), self._elide_mode, rect.width()
    #         )

    #         style_option = widgets.QStyleOption()
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
        if self._elide_mode == constants.TextElideMode.ElideNone:
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
                            core.QRect(0, current_y, self.width(), self.height()),
                            int(self.alignment()),
                            elided_line,
                        )
                        did_elide = True
                    else:
                        painter.drawText(
                            core.QRect(0, current_y, self.width(), self.height()),
                            int(self.alignment()),
                            line,
                        )
                    current_y += line_spacing

            if did_elide != self._is_elided:
                self._is_elided = did_elide
                self.elision_changed.emit(did_elide)

    def allow_links(self) -> Label:
        # self.setText("<a href=\"http://example.com/\">Click Here!</a>")
        self.setTextFormat(constants.TextFormat.RichText)
        self.setTextInteractionFlags(constants.TextInteractionFlag.TextBrowserInteraction)
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
        if align & constants.ALIGN_H_CENTER:  # type: ignore
            return "center"
        if align & constants.ALIGN_JUSTIFY:  # type: ignore
            return "justify"
        return "left"

    def get_vertical_alignment(self) -> constants.VerticalAlignmentStr:
        align = self.alignment()
        if align & constants.ALIGN_TOP:  # type: ignore
            return "top"
        if align & constants.ALIGN_BOTTOM:  # type: ignore
            return "bottom"
        if align & constants.ALIGN_BASELINE:  # type: ignore
            return "baseline"
        return "center"

    def set_indent(self, indent: int) -> Label:
        """Set the label's text indent in pixels."""
        self.setIndent(indent)
        return self

    def set_text_format(
        self, text_format: constants.TextFormatStr | constants.TextFormat
    ) -> Label:
        """Set the text format.

        Args:
            text_format: text format to use
        """
        self.setTextFormat(constants.TEXT_FORMAT.get_enum_value(text_format))
        return self

    def get_text_format(self) -> constants.TextFormatStr:
        """Return current text format.

        Returns:
            text format
        """
        return constants.TEXT_FORMAT.inverse[self.textFormat()]

    def set_text_interaction(self, *types: constants.TextInteractionStr) -> Label:
        """Set the text interaction mode.

        Args:
            types: text interaction mode to use
        """
        flags = constants.TEXT_INTERACTION.merge_flags(types)
        self.setTextInteractionFlags(flags)
        return self

    def get_text_interaction(self) -> list[constants.TextInteractionStr]:
        """Return current text interaction mode.

        Returns:
            list of text interaction modes
        """
        return constants.TEXT_INTERACTION.get_list(self.textInteractionFlags())

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

    def set_weight(self, weight: gui.font.WeightStr | gui.QFont.Weight) -> Label:
        """Set the font weight.

        Args:
            weight: font weight
        """
        font = self.font()
        font.setWeight(gui.font.WEIGHT.get_enum_value(weight))
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
        cls, path: datatypes.PathType, parent: widgets.QWidget | None = None
    ) -> Self:
        pixmap = gui.Pixmap.from_file(path)
        label = cls(parent=parent)
        label.setPixmap(pixmap)
        label.resize(pixmap.width(), pixmap.height())
        return label

    elideMode = core.Property(  # noqa: N815
        str,
        get_elide_mode,
        set_elide_mode,
        doc="Text Elide style",
    )


if __name__ == "__main__":
    app = widgets.app()
    widget = Label("http://www.test.fsdfsdfsfdsfsfdsfde\n" * 20, elide_mode="right")
    widget.show()
    app.exec()
