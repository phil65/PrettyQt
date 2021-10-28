from __future__ import annotations

from prettyqt import constants, core, gui, widgets
from prettyqt.qt import QtCore


class RenderLinkDelegate(widgets.StyledItemDelegate):
    def paint(self, painter, option, index):
        text = index.data()
        if not text:
            return

        painter.save()

        # I only wanted it for mouse over, but you'll probably want to remove
        # this condition
        if option.state and widgets.Style.StateFlag.State_MouseOver:
            font = option.font
            font.setUnderline(True)
            painter.setFont(font)
            painter.setPen(option.palette.link().color())
        painter.drawText(
            option.rect,
            constants.ALIGN_LEFT | constants.ALIGN_V_CENTER,  # type: ignore
        )
        painter.restore()

    def editorEvent(self, event, model, option, index):
        text = index.data()
        font = index.data(constants.FONT_ROLE)
        # alignment = index.data(constants.ALIGNMENT_ROLE)
        if font is None:
            font = gui.GuiApplication.get_font()
        fm = gui.FontMetricsF(font)
        rect = fm.get_bounding_rect(
            core.RectF(option.rect),
            constants.ALIGN_LEFT | constants.ALIGN_V_CENTER,  # type: ignore
            text,
        )
        if (
            event.type() == QtCore.QEvent.Type.MouseButtonPress
            and event.button() == QtCore.Qt.MouseButton.LeftButton
            and event.localPos() in rect
        ):
            text = index.data()
            gui.DesktopServices.open_url(text)
            return True
        return False


if __name__ == "__main__":
    """Run the application."""
    from prettyqt import widgets

    app = widgets.app()

    # Create and populate the tableWidget
    table_widget = widgets.TableWidget(4, 2)
    table_widget.set_delegate(RenderLinkDelegate(), column=1)
    table_widget.set_selection_behaviour("rows")
    table_widget.setHorizontalHeaderLabels(["Title", "Progress"])

    data = [
        ["Mass in B-Minor", "http://www.google.de"],
        ["Three More Foxes", "http://www.google.com"],
        ["Sex Bomb", "http://www.google.de"],
        ["Barbie Girl", "http://www.google.de"],
    ]

    for i, r in enumerate(data):
        table_widget[i, 0] = widgets.TableWidgetItem(r[0])
        item = widgets.TableWidgetItem()
        item.setData(0, r[1])
        item.set_text_alignment("left")
        table_widget[i, 1] = item

    table_widget.resizeColumnsToContents()
    table_widget.resize(500, 300)
    table_widget.show()

    app.main_loop()
