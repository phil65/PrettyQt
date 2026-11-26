# based on https://stackoverflow.com/questions/58891116/delegate-with-radio-buttons
# credits to musicamante

from typing import TYPE_CHECKING, cast

from prettyqt import constants, core, gui, widgets


if TYPE_CHECKING:
    from collections.abc import Iterable


class _RadioEditor(widgets.Widget):
    button_group: widgets.ButtonGroup


class RadioDelegate(widgets.StyledItemDelegate):
    ID = "radio"

    def __init__(self, parent: widgets.QWidget, items: Iterable[str]):
        super().__init__(parent)
        self.items = list(items)
        self.choices: list[int | None] = [None for _ in self.items]

    def createEditor(
        self,
        parent: widgets.QWidget,
        option: widgets.QStyleOptionViewItem,
        index: core.ModelIndex,
    ) -> widgets.Widget:
        editor = _RadioEditor(parent=parent, margin=0, auto_fill_background=True)
        # create a button group to keep track of the checked radio
        editor.button_group = widgets.ButtonGroup()
        # adding the widget as an argument to the layout constructor automatically
        # applies it to the widget
        layout = editor.set_layout("horizontal", margin=0)
        for i, k in enumerate(self.items):
            rb = widgets.RadioButton(k)
            layout.addWidget(rb)
            # prevent the radio to get focus from keyboard or mouse
            rb.set_focus_policy("none")
            rb.installEventFilter(self)
            editor.button_group.addButton(rb, i)
        # add a stretch to always align contents to the left
        layout.addStretch(1)

        # set a property that will be used for the mask
        editor.setProperty("offMask", gui.Region(editor.rect()))
        editor.installEventFilter(self)
        return editor

    def eventFilter(self, source: core.QObject, event: core.QEvent) -> bool:
        if not isinstance(source, widgets.QWidget):
            return super().eventFilter(source, event)
        match event.type():
            case core.Event.Type.MouseButtonPress:
                if isinstance(source, widgets.QRadioButton):
                    container = source.parentWidget()
                    if container is not None and not container.hasFocus():
                        # the parent has no focus, set it and ignore the click
                        container.setFocus()
                        return True
                elif not source.hasFocus():
                    # the container has been clicked, check
                    source.setFocus()
            case core.Event.Type.FocusIn:
                # event received as a consequence of setFocus
                # clear the mask to show it completely
                source.clearMask()
            case core.Event.Type.FocusOut:
                # another widget has requested focus, set the mask
                source.setMask(source.property("offMask"))
                # update the table viewport to get rid of possible
                # grid lines left after masking
                if (container := source.parentWidget()) is not None:
                    container.update()
        return super().eventFilter(source, event)

    def updateEditorGeometry(
        self,
        editor: widgets.QWidget,
        option: widgets.QStyleOptionViewItem,
        index: core.ModelIndex,
    ):
        rect = core.Rect(option.rect)
        min_width = editor.minimumSizeHint().width()
        if rect.width() < min_width:
            rect.setWidth(min_width)
        editor.setGeometry(rect)
        # create a new mask based on the option rectangle, then apply it
        mask = gui.Region(0, 0, option.rect.width(), option.rect.height())
        editor.setProperty("offMask", mask)
        editor.setMask(mask)

    def setEditorData(self, editor: widgets.QWidget, index: core.ModelIndex):
        value = index.data(constants.DISPLAY_ROLE)
        if value in self.items:
            group = cast("_RadioEditor", editor).button_group
            if (button := group.button(self.items.index(value))) is not None:
                button.setChecked(True)

    def setModelData(
        self,
        editor: widgets.QWidget,
        model: core.QAbstractItemModel,
        index: core.ModelIndex,
    ):
        button = cast("_RadioEditor", editor).button_group.checkedId()
        if button >= 0:
            model.setData(
                index,
                self.items[button],
                constants.DISPLAY_ROLE,
            )
            self.choices[button] = index.row()


if __name__ == "__main__":
    app = widgets.app()
    widget = widgets.TableWidget()
    widget.setColumnCount(3)
    widget.insertRow(0)
    widget.insertRow(0)
    widget.setHorizontalHeaderLabels(["LIB", "CELL", "area"])
    item = widgets.TableWidgetItem("test")
    widget[0, 0] = item
    widget[1, 1] = widgets.TableWidgetItem("test")
    widget[1, 2] = widgets.TableWidgetItem("test")
    widget[2, 1] = widgets.TableWidgetItem("test")
    delegate = RadioDelegate(widget, ["a", "b"])
    widget.setItemDelegateForColumn(0, delegate)
    widget.openPersistentEditor(item)
    widget.show()
    app.exec()
