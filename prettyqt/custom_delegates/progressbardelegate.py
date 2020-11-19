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
    table_widget = widgets.TableWidget(4, 2)
    table_widget.set_delegate(ProgressBarDelegate(), column=1)
    table_widget.setEditTriggers(
        widgets.AbstractItemView.DoubleClicked | widgets.AbstractItemView.SelectedClicked
    )
    table_widget.set_selection_behaviour("rows")
    table_widget.setHorizontalHeaderLabels(["Title", "Progress"])

    data = [
        ["Mass in B-Minor", 50],
        ["Three More Foxes", 40],
        ["Sex Bomb", 33],
        ["Barbie Girl", 5],
    ]

    for i, r in enumerate(data):
        table_widget[i, 0] = widgets.TableWidgetItem(r[0])
        item = widgets.TableWidgetItem()
        item.setData(0, r[1])
        table_widget[i, 1] = item

    table_widget.resizeColumnsToContents()
    table_widget.resize(500, 300)
    table_widget.show()

    app.main_loop()
