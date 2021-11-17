from __future__ import annotations

from prettyqt import widgets


class ProgressBarDelegate(widgets.StyledItemDelegate):
    def paint(self, painter, option, index):
        progress = index.data()
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
    table_widget.setEditTriggers(
        widgets.AbstractItemView.EditTrigger.DoubleClicked  # type: ignore
        | widgets.AbstractItemView.EditTrigger.SelectedClicked
    )
    table_widget.set_selection_behaviour("rows")
    table_widget.setHorizontalHeaderLabels(["Title", "Progress"])
    item_1 = widgets.TableWidgetItem("Test1")
    item_2 = widgets.TableWidgetItem()
    item_2.setData(0, 50)
    table_widget[0, 0] = item_1
    table_widget[0, 1] = item_2
    table_widget.resizeColumnsToContents()
    table_widget.resize(500, 300)
    table_widget.show()

    app.main_loop()
