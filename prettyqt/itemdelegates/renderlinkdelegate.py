from __future__ import annotations

from prettyqt import constants, core, gui, widgets


class RenderLinkDelegate(widgets.StyledItemDelegate):
    ID = "render_link"

    def paint(
        self,
        painter: gui.QPainter,
        option: widgets.QStyleOptionViewItem,
        index: core.ModelIndex,
    ):
        text = index.data()
        if not text:
            return
        option = widgets.StyleOptionViewItem(option)
        self.initStyleOption(option, index)
        painter.save()

        if option.state and widgets.Style.StateFlag.State_MouseOver:
            font = option.font
            font.setUnderline(True)
            painter.setFont(font)
            painter.setPen(option.palette.link().color())
        rect = option.rect.toRectF()
        painter.drawText(rect, constants.ALIGN_CENTER_LEFT, text)
        painter.restore()

    def editorEvent(
        self,
        event,
        model: core.QAbstractItemModel,
        option: widgets.QStyleOptionViewItem,
        index: core.ModelIndex,
    ):
        text = index.data()
        font = index.data(constants.FONT_ROLE) or gui.GuiApplication.font()
        # alignment = index.data(constants.ALIGNMENT_ROLE)
        fm = gui.FontMetricsF(font)
        rect = option.rect.toRectF()
        b_rect = fm.get_bounding_rect(rect, constants.ALIGN_CENTER_LEFT, text)
        if (
            event.type() == core.QEvent.Type.MouseButtonPress
            and event.button() == constants.MouseButton.LeftButton  # type: ignore
            and b_rect.contains(event.position())  # type: ignore
        ):
            text = index.data()
            gui.DesktopServices.open_url(text)
            return True
        return False


if __name__ == "__main__":
    app = widgets.app()

    # Create and populate the tableWidget
    table_widget = widgets.TableWidget(4, 2)
    table_widget.set_delegate(RenderLinkDelegate(), column=1)
    table_widget.set_selection_behavior("rows")
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

    app.exec()
