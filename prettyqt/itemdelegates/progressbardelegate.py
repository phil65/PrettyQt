from __future__ import annotations

from prettyqt import constants, core, gui, widgets


class ProgressBarDelegate(widgets.StyledItemDelegate):
    ID = "progress_bar"

    def __init__(self, role: constants.ItemDataRole = constants.DISPLAY_ROLE, **kwargs):
        self._role = role
        super().__init__(**kwargs)

    def paint(
        self,
        painter: gui.QPainter,
        option: widgets.QStyleOptionViewItem,
        index: core.ModelIndex,
    ):
        progress = index.data(self._role)
        opt = widgets.StyleOptionProgressBar()
        opt.rect = option.rect
        opt.minimum = 0
        opt.maximum = 100
        opt.progress = progress
        opt.text = f"{progress}%"
        opt.textVisible = True
        opt.state |= widgets.Style.StateFlag.State_Horizontal
        widgets.Application.style().drawControl(
            widgets.Style.ControlElement.CE_ProgressBar, opt, painter
        )


if __name__ == "__main__":
    """Run the application."""
    from prettyqt import widgets

    app = widgets.app()

    # Create and populate the tableWidget
    table_widget = widgets.TableWidget(1, 2)
    table_widget.set_delegate(ProgressBarDelegate(), column=1)
    table_widget.set_edit_triggers("all")
    table_widget.set_selection_behavior("rows")
    table_widget.setHorizontalHeaderLabels(["Title", "Progress"])
    item_1 = widgets.TableWidgetItem("Test1")
    item_2 = widgets.TableWidgetItem()
    item_2.setData(0, 50)
    table_widget[0, 0] = item_1
    table_widget[0, 1] = item_2
    table_widget.resizeColumnsToContents()
    table_widget.resize(500, 300)
    table_widget.show()

    app.exec()
