import logging
from typing import Iterator, Mapping, MutableMapping, Optional, Union

from qtpy import QtCore, QtWidgets

from prettyqt import constants, core, gui, widgets
from prettyqt.utils import InvalidParamError


logger = logging.getLogger(__name__)


SAVE_STATES = dict(
    splitters=QtWidgets.QSplitter,
    mainwindows=QtWidgets.QMainWindow,
    headerviews=QtWidgets.QHeaderView,
)

QtWidgets.QApplication.__bases__ = (gui.GuiApplication,)


class Application(QtWidgets.QApplication):
    def __class_getitem__(cls, name: str) -> QtWidgets.QWidget:
        widget = cls.get_widget(name)
        if widget is None:
            raise ValueError(f"Widget {name!r} does not exist.")
        return widget

    def __iter__(self) -> Iterator[QtWidgets.QWidget]:
        return iter(self.topLevelWidgets())

    def serialize_fields(self):
        return dict(
            auto_sip_enabled=self.autoSipEnabled(),
            cursor_flash_time=self.cursorFlashTime(),
            double_click_interval=self.doubleClickInterval(),
            keyboard_input_interval=self.keyboardInputInterval(),
            start_drag_distance=self.startDragDistance(),
            start_drag_time=self.startDragTime(),
            style_sheet=self.styleSheet(),
            wheel_scroll_lines=self.wheelScrollLines(),
            icon=gui.Icon(self.windowIcon()),
        )

    def store_widget_states(
        self, settings: Optional[MutableMapping] = None, key: str = "states"
    ):
        settings = core.Settings() if settings is None else settings
        result = dict()
        for k, v in SAVE_STATES.items():
            result[k] = {
                i.objectName(): i.saveState()
                for i in self.find_children(v)
                if i.objectName()
            }
        settings[key] = result

    def restore_widget_states(
        self, settings: Optional[Mapping] = None, key: str = "states"
    ):
        settings = core.Settings() if settings is None else settings
        for category, v in SAVE_STATES.items():
            items = settings[key].get(category)
            if items is None:
                continue
            for name, state in items.items():
                w = self.find_child(v, name=name)
                if w is not None:
                    w.restoreState(state)

    def about_popup(self, title: str = "About"):
        text = (
            f"{self.applicationName()}\n\n"
            f"{self.organizationName()}\n"
            f"{self.applicationVersion()}\n"
            f"{self.organizationDomain()}"
        )
        popup = widgets.MessageBox(
            widgets.MessageBox.NoIcon, title, text, buttons=widgets.MessageBox.Ok
        )
        popup.set_icon("mdi.information-outline")
        popup.exec_()

    @classmethod
    def get_mainwindow(cls) -> Optional[QtWidgets.QMainWindow]:
        widget_list = cls.instance().topLevelWidgets()
        for widget in widget_list:
            if isinstance(widget, QtWidgets.QMainWindow):
                return widget
        return None

    @classmethod
    def get_widget(cls, name: str) -> Optional[QtWidgets.QWidget]:
        mw = cls.get_mainwindow()
        if mw is None:
            logger.warning("Trying to get widget from nonexistent mainwindow")
            return None
        return mw.findChild(QtWidgets.QWidget, name)
        # widget_list = cls.instance().allWidgets()
        # for widget in widget_list:
        #     if isinstance(widget, QtWidgets.QWidget) and widget.objectName() == name:
        #         return widget
        # return None

    def send_event(self, obj_or_str: Union[str, QtCore.QObject], event: QtCore.QEvent):
        obj = self.get_widget(obj_or_str) if isinstance(obj_or_str, str) else obj_or_str
        if obj is None:
            raise ValueError(obj)
        return self.sendEvent(obj, event)

    def post_event(
        self,
        obj_or_str: Union[str, QtCore.QObject],
        event: QtCore.QEvent,
        priority: Union[int, constants.EventPriorityStr] = "normal",
    ):
        obj = self.get_widget(obj_or_str) if isinstance(obj_or_str, str) else obj_or_str
        if obj is None:
            raise ValueError(obj)
        super().post_event(obj, event, priority)

    @classmethod
    def get_style_icon(cls, icon: str) -> gui.Icon:
        style = cls.style()
        # icon_size = style.pixelMetric(QtWidgets.QStyle.PM_MessageBoxIconSize)
        if icon not in widgets.style.STANDARD_PIXMAP:
            raise InvalidParamError(icon, widgets.style.STANDARD_PIXMAP)
        icon = style.standardIcon(widgets.style.STANDARD_PIXMAP[icon])
        return gui.Icon(icon)

    def set_effect_enabled(self, effect: constants.UiEffectStr, enabled: bool = True):
        """Set the enabled state of a desktop effect.

        Args:
            effect: desktop effect to set
            enabled: new state

        Raises:
            InvalidParamError: invalid desktop effect
        """
        if effect not in constants.UI_EFFECTS:
            raise InvalidParamError(effect, constants.UI_EFFECTS)
        self.setEffectEnabled(constants.UI_EFFECTS[effect])

    def is_effect_enabled(self, effect: constants.UiEffectStr) -> str:
        """Return desktop effect state.

        Returns:
            desktop effect state
        """
        return self.isEffectEnabled(constants.UI_EFFECTS[effect])

    def set_navigation_mode(self, mode: constants.NavigationModeStr):
        """Set the navigation mode.

        Args:
            mode: navigation mode to use

        Raises:
            InvalidParamError: invalid navigation mode
        """
        if mode not in constants.NAVIGATION_MODES:
            raise InvalidParamError(mode, constants.NAVIGATION_MODES)
        self.setNavigationMode(constants.NAVIGATION_MODES[mode])

    def get_navigation_mode(self) -> constants.NavigationModeStr:
        """Return navigation mode.

        Returns:
            navigation mode
        """
        return constants.NAVIGATION_MODES.inverse[self.navigationMode()]


if __name__ == "__main__":
    app = Application([])
    app.load_language_file("de")
