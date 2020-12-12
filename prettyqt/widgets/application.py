from typing import Optional, Iterator, MutableMapping, Mapping
import logging

from qtpy import QtCore, QtWidgets

from prettyqt import core, gui, widgets
from prettyqt.utils import bidict, InvalidParamError

logger = logging.getLogger(__name__)


UI_EFFECTS = bidict(
    animate_menu=QtCore.Qt.UI_AnimateMenu,
    fade_menu=QtCore.Qt.UI_FadeMenu,
    animate_combo=QtCore.Qt.UI_AnimateCombo,
    animate_tooltip=QtCore.Qt.UI_AnimateTooltip,
    fade_tooltip=QtCore.Qt.UI_FadeTooltip,
    animate_toolbox=QtCore.Qt.UI_AnimateToolBox,
)

NAVIGATION_MODES = bidict(
    none=QtCore.Qt.NavigationModeNone,
    keypad_tab_order=QtCore.Qt.NavigationModeKeypadTabOrder,
    keypad_directional=QtCore.Qt.NavigationModeKeypadDirectional,
    cursor_auto=QtCore.Qt.NavigationModeCursorAuto,
    cursor_force_visible=QtCore.Qt.NavigationModeCursorForceVisible,
)

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

    @classmethod
    def get_style_icon(cls, icon: str) -> gui.Icon:
        style = cls.style()
        # icon_size = style.pixelMetric(QtWidgets.QStyle.PM_MessageBoxIconSize)
        if icon not in widgets.style.STANDARD_PIXMAPS:
            raise InvalidParamError(icon, widgets.style.STANDARD_PIXMAPS)
        icon = style.standardIcon(widgets.style.STANDARD_PIXMAPS[icon])
        return gui.Icon(icon)

    def set_effect_enabled(self, effect: str, enabled: bool = True):
        """Set the enabled state of a desktop effect.

        valid values are: "animate_menu", "fade_menu", "animate_combo",
        "animate_tooltip", "fade_tooltip", "animate_toolbox"

        Args:
            effect: desktop effect to set
            enabled: new state

        Raises:
            InvalidParamError: invalid desktop effect
        """
        if effect not in UI_EFFECTS:
            raise InvalidParamError(effect, UI_EFFECTS)
        self.setEffectEnabled(UI_EFFECTS[effect])

    def is_effect_enabled(self, effect: str) -> str:
        """Return desktop effect state.

        possible values are "animate_menu", "fade_menu", "animate_combo",
        "animate_tooltip", "fade_tooltip", "animate_toolbox"

        Returns:
            desktop effect state
        """
        return self.isEffectEnabled(UI_EFFECTS[effect])

    def set_navigation_mode(self, mode: str):
        """Set the navigation mode.

        valid values: "none", "keypad_tab_order", "keypad_directional", "cursor_auto",
        "cursor_force_visible"

        Args:
            mode: navigation mode to use

        Raises:
            InvalidParamError: invalid navigation mode
        """
        if mode not in NAVIGATION_MODES:
            raise InvalidParamError(mode, NAVIGATION_MODES)
        self.setNavigationMode(NAVIGATION_MODES[mode])

    def get_navigation_mode(self) -> str:
        """Return navigation mode.

        possible values: "none", "keypad_tab_order", "keypad_directional", "cursor_auto",
        "cursor_force_visible"

        Returns:
            navigation mode
        """
        return NAVIGATION_MODES.inverse[self.navigationMode()]


if __name__ == "__main__":
    app = Application([])
    app.load_language_file("de")
