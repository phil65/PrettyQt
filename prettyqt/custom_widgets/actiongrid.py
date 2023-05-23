from __future__ import annotations

import dataclasses
import sys

from prettyqt import core, widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets


@dataclasses.dataclass
class ActionGridItem:
    button: widgets.ToolButton
    action: QtGui.QAction
    row: int
    column: int


PM = QtWidgets.QStyle.PixelMetric
CT = QtWidgets.QStyle.ContentsType
CC = QtWidgets.QStyle.ComplexControl


class AcionGrid(widgets.ToolButton):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._elided_text = ""
        self.set_size_policy("preferred", "preferred")

    def actionEvent(self, event):
        super().actionEvent(event)
        match event.type():
            case QtCore.QEvent.Type.ActionChanged | QtCore.QEvent.Type.ActionAdded:
                self._update_text()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_text()

    def _update_text(self):
        fm = self.get_font_metrics()
        text = self.defaultAction().text()
        words = text.split()

        option = widgets.StyleOptionToolButton()
        option.initFrom(self)

        margin = self.style().pixelMetric(PM.PM_ButtonMargin, option, self)
        min_width = self.width() - 2 * margin

        lines = []

        if fm.boundingRect(" ".join(words)).width() <= min_width or len(words) <= 1:
            lines = [" ".join(words)]
        else:
            best_w, best_l = sys.maxsize, ["", ""]
            for i in range(1, len(words)):
                l1 = " ".join(words[:i])
                l2 = " ".join(words[i:])
                width = max(fm.boundingRect(l1).width(), fm.boundingRect(l2).width())
                if width < best_w:
                    best_w = width
                    best_l = [l1, l2]
            lines = best_l

        # elide the end of each line if too long
        lines = [fm.elided_text(line, "right", self.width() - margin) for line in lines]
        self._elided_text = "\n".join(lines).replace("&", "&&")  # Need escaped ampersand

    # def paintEvent(self, event):
    #     with widgets.StylePainter(self) as p:
    #         opt = QtWidgets.QStyleOptionToolButton()
    #         self.initStyleOption(opt)
    #         p.drawComplexControl(CC.CC_ToolButton, opt)

    def initStyleOption(self, option):
        super().initStyleOption(option)
        if self._elided_text:
            option.text = self._elided_text

    def sizeHint(self):
        opt = QtWidgets.QStyleOptionToolButton()
        self.initStyleOption(opt)
        style = self.style()
        csize = opt.iconSize
        fm = opt.fontMetrics
        margin = style.pixelMetric(PM.PM_ButtonMargin)
        # content size is:
        #   * vertical: icon + margin + 2 * font ascent
        #   * horizontal: icon * 3 / 2

        csize.setHeight(csize.height() + margin + 2 * fm.lineSpacing())
        csize.setWidth(csize.width() * 3 // 2)
        return style.sizeFromContents(CT.CT_ToolButton, opt, csize, self)


class ActionGrid(widgets.Frame):
    """A widget containing a grid of actions/buttons, with a toolbar-like interface.

    Parameters:
        columns : Number of columns in the grid layout.
        button_size : Size of tool buttons in the grid.
        îcon_size : Size of icons in the buttons.
        tool_button_style : Tool button style.
    """

    actionTriggered = core.Signal(QtGui.QAction)
    actionHovered = core.Signal(QtGui.QAction)

    def __init__(
        self,
        columns: int = 4,
        button_size=None,
        icon_size=None,
        tool_button_style=QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon,
        **kwargs,
    ):
        super().__init__(**kwargs)

        if button_size is None:
            button_size = QtCore.QSize()
        if icon_size is None:
            icon_size = QtCore.QSize()

        self._columns = columns
        self._button_size = QtCore.QSize(button_size)
        self._icon_size = QtCore.QSize(icon_size)
        self._tool_button_style = tool_button_style

        self._grid_slots: list[ActionGridItem] = []
        self._mapper = core.SignalMapper()
        self._mapper.mappedObject.connect(self._on_clicked)

        self.set_layout("grid", margin=0, spacing=0)
        self.set_size_policy("fixed", "minimum_expanding")

    def setButtonSize(self, size):
        """Set the button size."""
        if self._button_size != size:
            self._button_size = QtCore.QSize(size)
            for slot in self._grid_slots:
                slot.button.setFixedSize(size)

    def button_size(self):
        """Return the button size."""
        return QtCore.QSize(self._button_size)

    def setIconSize(self, size):
        """Set the button icon size (The default icon size is style-defined)."""
        if self._icon_size != size:
            self._icon_size = QtCore.QSize(size)
            size = self._get_effective_icon_size()
            for slot in self._grid_slots:
                slot.button.setIconSize(size)

    def icon_size(self):
        """Return icon size. If no size is set a style defined size is returned."""
        return self._get_effective_icon_size()

    def _get_effective_icon_size(self):
        if self._icon_size.isValid():
            return QtCore.QSize(self._icon_size)
        opt = QtWidgets.QStyleOptionToolButton()
        opt.initFrom(self)
        s = self.style().pixelMetric(PM.PM_LargeIconSize, opt, None)
        return QtCore.QSize(s, s)

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.Type.StyleChange:
            size = self._get_effective_icon_size()
            for item in self._grid_slots:
                item.button.setIconSize(size)
        super().changeEvent(event)

    def set_tool_button_style(self, style):
        """Set the tool button style."""
        if self._tool_button_style != style:
            self._tool_button_style = style
            for slot in self._grid_slots:
                slot.button.setToolButtonStyle(style)

    def get_tool_button_style(self):
        """Return the tool button style."""
        return self._tool_button_style

    def set_column_count(self, columns: int):
        """Set the number of button/action columns."""
        if self._columns != columns:
            self._columns = columns
            self._relayout()

    def columns(self) -> int:
        """Return the number of columns in the grid."""
        return self._columns

    def clear(self):
        """Clear all actions/buttons."""
        for slot in reversed(list(self._grid_slots)):
            self.removeAction(slot.action)
        self._grid_slots = []

    def get_button_for_action(self, action):
        """Return the :class:`QToolButton` instance button for `action`."""
        actions = [slot.action for slot in self._grid_slots]
        index = actions.index(action)
        return self._grid_slots[index].button

    def create_button_for_action(self, action):
        """Create and return a :class:`QToolButton` for action."""
        button = AcionGrid(self)
        button.setDefaultAction(action)

        if self._button_size.isValid():
            button.setFixedSize(self._button_size)
        button.setIconSize(self._get_effective_icon_size())
        button.setToolButtonStyle(self._tool_button_style)
        button.setProperty("tool-grid-button", True)
        return button

    def count(self) -> int:
        """Return the number of buttons/actions in the grid."""
        return len(self._grid_slots)

    def actionEvent(self, event):
        super().actionEvent(event)
        match event.type():
            case QtCore.QEvent.Type.ActionAdded:
                # Note: the action is already in the self.actions() list.
                actions = list(self.actions())
                index = actions.index(event.action())
                self._insert_action_button(index, event.action())

            case QtCore.QEvent.Type.ActionRemoved:
                self._remove_action_button(event.action())

    def _insert_action_button(self, index, action):
        """Create a button for the action and add it to the layout at index."""
        self._shift_grid(index, 1)
        button = self.create_button_for_action(action)

        row = index // self._columns
        column = index % self._columns

        layout = self.layout()
        layout.addWidget(button, row, column)

        self._grid_slots.insert(index, ActionGridItem(button, action, row, column))

        self._mapper.setMapping(button, action)
        button.clicked.connect(self._mapper.map)
        button.installEventFilter(self)

    def _remove_action_button(self, action):
        """Remove the button for the action from the layout and delete it."""
        actions = [slot.action for slot in self._grid_slots]
        index = actions.index(action)
        slot = self._grid_slots.pop(index)

        slot.button.removeEventFilter(self)
        self._mapper.removeMappings(slot.button)

        self.layout().removeWidget(slot.button)
        self._shift_grid(index + 1, -1)

        slot.button.deleteLater()

    def _shift_grid(self, start: int, count: int = 1):
        """Shift all buttons starting at index `start` by `count` cells."""
        layout = self.layout()
        button_count = layout.count()
        columns = self._columns

        direction = 1 if count >= 0 else -1
        if direction == 1:
            start, end = button_count - 1, start - 1
        else:
            start, end = start, button_count

        for index in range(start, end, -direction):
            if item := layout.itemAtPosition(index // columns, index % columns):
                button = item.widget()
                new_index = index + count
                layout.addWidget(
                    button,
                    new_index // columns,
                    new_index % columns,
                )

    def _relayout(self):
        """Relayout the buttons."""
        layout = self.layout()
        layout.clear()
        cols = self._columns
        self._grid_slots = [
            ActionGridItem(slot.button, slot.action, i // cols, i % cols)
            for i, slot in enumerate(self._grid_slots)
        ]
        for slot in self._grid_slots:
            layout.addWidget(slot.button, slot.row, slot.column)

    def _index_of(self, button) -> int:
        """Return the index of button widget."""
        buttons = [slot.button for slot in self._grid_slots]
        return buttons.index(button)

    def _on_button_enter(self, button):
        action = button.defaultAction()
        self.actionHovered.emit(action)

    @core.Slot(QtCore.QObject)
    def _on_clicked(self, action):
        self.actionTriggered.emit(action)

    def eventFilter(self, obj, event) -> bool:
        match event.type():
            case QtCore.QEvent.Type.KeyPress if obj.hasFocus():
                combo = core.KeyCombination(event.keyCombination())
                if combo.is_moving() and self._focus_move(obj, combo.key()):
                    event.accept()
                    return True
            case QtCore.QEvent.Type.HoverEnter if obj.parent() is self:
                self._on_button_enter(obj)
        return super().eventFilter(obj, event)

    def _focus_move(self, focus: QtWidgets.QWidget, key: QtCore.Qt.Key) -> bool:
        assert focus is self.focusWidget()
        try:
            index = self._index_of(focus)
        except IndexError:
            return False
        match key:
            case QtCore.Qt.Key.Key_Down:
                index += self._columns
            case QtCore.Qt.Key.Key_Up:
                index -= self._columns
            case QtCore.Qt.Key.Key_Left:
                index -= 1
            case QtCore.Qt.Key.Key_Right:
                index += 1

        if 0 <= index < self.count():
            button = self._grid_slots[index].button
            button.setFocus(QtCore.Qt.FocusReason.TabFocusReason)
            return True
        else:
            return False


if __name__ == "__main__":
    app = widgets.app()
    toolbox = ActionGrid(columns=3)
    icon = app.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_FileIcon)
    actions = [
        QtGui.QAction("A", None, icon=icon),
        QtGui.QAction("B", None, icon=icon),
        QtGui.QAction("This one is longer.", icon=icon),
        QtGui.QAction("Not done yet!", icon=icon),
        QtGui.QAction("The quick brown fox ... does something I guess", icon=icon),
    ]

    toolbox.addActions(actions)
    toolbox.actionTriggered.connect(print)
    toolbox.show()
    app.exec()
