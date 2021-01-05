from __future__ import annotations

from prettyqt import widgets


class ProgressBarDelegate(widgets.StyledItemDelegate):
    def paint(self, painter, option, index):
        progress = index.data()
        progressBar_option = widgets.StyleOptionProgressBar()
        progressBar_option.rect = option.rect
        progressBar_option.minimum = 0
        progressBar_option.maximum = 100
        progressBar_option.progress = progress
        progressBar_option.text = f"{progress}%"
        progressBar_option.textVisible = True
        widgets.Application.style().drawControl(
            widgets.Style.CE_ProgressBar, progressBar_option, painter
        )


if __name__ == "__main__":
    """Run the application."""
    from prettyqt import widgets

    app = widgets.app()

    # Create and populate the tableWidget
    table_widget = widgets.TableWidget(1, 2)
    table_widget.set_delegate(ProgressBarDelegate(), column=1)
    table_widget.setEditTriggers(
        widgets.AbstractItemView.DoubleClicked | widgets.AbstractItemView.SelectedClicked
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
