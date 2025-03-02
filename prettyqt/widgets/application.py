from __future__ import annotations

import contextlib
import logging
import os
import pathlib
import sys
import timeit
from typing import TYPE_CHECKING

import qstylizer.parser
import qstylizer.style

from prettyqt import constants, core, gui, iconprovider, paths, widgets
from prettyqt.utils import datatypes, listdelegators


if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Iterator, Mapping, MutableMapping


logger = logging.getLogger(__name__)


SAVE_STATES = dict(
    splitters=widgets.QSplitter,
    mainwindows=widgets.QMainWindow,
    headerviews=widgets.QHeaderView,
)


def setup_runner():
    import inspect

    from prettyqt.qt.QtCore import SignalInstance
    from prettyqt.utils import asyncrunner

    old_connect = SignalInstance.connect
    runner = asyncrunner.AsyncRunner()

    def connect(self, slot):
        if inspect.iscoroutinefunction(slot):
            return old_connect(self, runner.to_sync(slot))
        return old_connect(self, slot)

    SignalInstance.connect = connect
    return runner


class ApplicationMixin(gui.GuiApplicationMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._debug = False
        self.runner = setup_runner()

    def __iter__(self) -> Iterator[widgets.QWidget]:
        return iter(self.topLevelWidgets())

    def run_parallel(self, fns: Iterable[Callable]):
        self.runner.run_parallel(fns)

    def is_debug(self) -> bool:
        return self._debug

    @contextlib.contextmanager
    def debug_mode(self, log_level: int = logging.DEBUG):
        from prettyqt.debugging import ErrorMessageBox, MessageHandler
        from prettyqt.eventfilters import debugmode

        handler = logging.StreamHandler(sys.stdout)
        f_format = logging.Formatter(
            "%(asctime)s: %(filename)s:%(lineno)d - %(levelname)s - %(message)s"
        )
        handler.setFormatter(f_format)
        handler.setLevel(log_level)
        root_logger = logging.getLogger()
        root_logger.addHandler(handler)
        root_logger.setLevel(log_level)
        _original_excepthook = sys.excepthook
        sys.excepthook = ErrorMessageBox._excepthook
        eventfilter = debugmode.DebugMode(self)
        self._debug = True
        self.installEventFilter(eventfilter)
        with MessageHandler(root_logger):
            yield self
        self._debug = False
        self.removeEventFilter(eventfilter)
        sys.excepthook = _original_excepthook

    def store_widget_states(
        self, settings: MutableMapping | None = None, key: str = "states"
    ):
        settings = core.Settings() if settings is None else settings
        result = {
            k: {
                i.objectName(): i.saveState()
                for i in self.find_children(v)
                if i.objectName()
            }
            for k, v in SAVE_STATES.items()
        }
        settings[key] = result

    def restore_widget_states(self, settings: Mapping | None = None, key: str = "states"):
        settings = core.Settings() if settings is None else settings
        for category, v in SAVE_STATES.items():
            items = settings[key].get(category)
            if items is None:
                continue
            for name, state in items.items():
                w = self.find_child(v, name=name)
                if w is not None:
                    new_state = state.encode() if isinstance(state, str) else state
                    w.restoreState(new_state)

    @classmethod
    def widget_at(
        cls, pos: datatypes.PointType, typ: type | None = None
    ) -> widgets.QWidget:
        if typ is None:
            return super().widgetAt(pos)
        for widget in cls.widgets_at(pos):
            if isinstance(widget, typ):
                return widget
        return None

    @classmethod
    def widgets_at(
        cls, pos: datatypes.PointType
    ) -> listdelegators.ListDelegator[widgets.QWidget]:
        """Return ALL widgets at `pos`.

        Arguments:
            pos: Position at which to get widgets

        Returns:
            list of widgets at given position

        """
        widgets = []
        while widget_at := cls.widgetAt(datatypes.to_point(pos)):
            widgets.append(widget_at)
            # Make widget invisible to further enquiries
            widget_at.setAttribute(constants.WidgetAttribute.WA_TransparentForMouseEvents)
        # Restore attribute
        for widget in widgets:
            widget.setAttribute(
                constants.WidgetAttribute.WA_TransparentForMouseEvents, False
            )

        return widgets

    @classmethod
    def get_mainwindow(cls) -> widgets.QMainWindow | None:
        app = cls.instance()
        if app is None:
            return None
        return next(
            (w for w in app.topLevelWidgets() if isinstance(w, widgets.QMainWindow)),
            None,
        )

    @classmethod
    def get_widget(cls, name: str) -> widgets.QWidget | None:
        mw = cls.get_mainwindow()
        if mw is None:
            logger.warning("Trying to get widget from nonexistent mainwindow")
            return None
        return mw.findChild(widgets.QWidget, name)  # type: ignore
        # widget_list = cls.instance().allWidgets()
        # for widget in widget_list:
        #     if isinstance(widget, widgets.QWidget) and widget.objectName() == name:
        #         return widget
        # return None

    @contextlib.contextmanager
    def edit_stylesheet(self) -> Iterator[qstylizer.style.StyleSheet]:
        ss = self.get_stylesheet()
        yield ss
        self.set_stylesheet(ss)

    def set_stylesheet(
        self, ss: None | str | qstylizer.style.StyleSheet | datatypes.PathType
    ):
        match ss:
            case str():
                pass
            case os.PathLike():
                ss = pathlib.Path(ss).read_text()
            case None:
                ss = ""
            case qstylizer.style.StyleSheet():
                ss = str(ss)
            case _:
                raise TypeError(ss)
        self.setStyleSheet(ss)

    def set_style(self, style: str):
        self.setStyle(widgets.QStyleFactory.create(style))
        icon_color = self.get_palette().get_color("highlighted_text")
        iconprovider.set_defaults(color=icon_color)

    def get_stylesheet(self) -> qstylizer.style.StyleSheet:
        return qstylizer.parser.parse(self.styleSheet())

    def set_theme(self, theme: constants.ThemeStr):
        self.set_palette(theme)
        match theme:
            case "default":
                self.set_stylesheet("")
                color = self.get_palette().get_color("highlighted_text")
            case "dark":
                ss = (paths.THEMES_PATH / "darktheme.qss").read_text()
                self.set_stylesheet(ss)
                color = gui.Color("lightblue")
        iconprovider.set_defaults(color=color)

    @classmethod
    def get_available_themes(cls) -> dict[constants.ThemeStr, str]:
        return dict(default="Default", dark="Dark")

    def send_event(self, obj_or_str: str | core.QObject, event: core.QEvent) -> bool:
        obj = self.get_widget(obj_or_str) if isinstance(obj_or_str, str) else obj_or_str
        if obj is None:
            raise ValueError(obj)
        return self.sendEvent(obj, event)

    def post_event(
        self,
        obj_or_str: str | core.QObject,
        event: core.QEvent,
        priority: int | constants.EventPriorityStr = "normal",
    ):
        obj = self.get_widget(obj_or_str) if isinstance(obj_or_str, str) else obj_or_str
        if obj is None:
            raise ValueError(obj)
        super().post_event(obj, event, priority)

    @classmethod
    def get_style_icon(
        cls, icon: widgets.style.StandardPixmapStr | widgets.QStyle.StandardPixmap
    ) -> gui.Icon:
        style = cls.style()
        # icon_size = style.pixelMetric(widgets.QStyle.PM_MessageBoxIconSize)
        icon = style.standardIcon(widgets.style.STANDARD_PIXMAP.get_enum_value(icon))
        return gui.Icon(icon)

    def set_effect_enabled(
        self, effect: constants.UiEffectStr | constants.UIEffect, enabled: bool = True
    ):
        """Set the enabled state of a desktop effect.

        Args:
            effect: desktop effect to set
            enabled: new state
        """
        self.setEffectEnabled(constants.UI_EFFECTS.get_enum_value(effect))

    def is_effect_enabled(self, effect: constants.UiEffectStr) -> bool:
        """Return desktop effect state.

        Returns:
            desktop effect state
        """
        return self.isEffectEnabled(constants.UI_EFFECTS[effect])

    def set_navigation_mode(
        self, mode: constants.NavigationModeStr | constants.NavigationMode
    ):
        """Set the navigation mode.

        Args:
            mode: navigation mode to use
        """
        self.setNavigationMode(constants.NAVIGATION_MODES.get_enum_value(mode))

    def get_navigation_mode(self) -> constants.NavigationModeStr:
        """Return navigation mode.

        Returns:
            navigation mode
        """
        return constants.NAVIGATION_MODES.inverse[self.navigationMode()]

    @classmethod
    def sleep(cls, secs: float):
        """Pause application (non-blocking).

        Args:
            secs: seconds to sleep
        """
        start = timeit.default_timer()
        while timeit.default_timer() - start < secs:
            cls.processEvents()

    @classmethod
    def process_events(
        cls,
        user_input: bool = True,
        socket_notifiers: bool = True,
        wait_for_more: bool = True,
        msecs: int = 0,
    ):
        flag = core.EventLoop.ProcessEventsFlag.AllEvents
        if not user_input:
            flag |= core.EventLoop.ProcessEventsFlag.ExcludeUserInputEvents
        if not socket_notifiers:
            flag |= core.EventLoop.ProcessEventsFlag.ExcludeSocketNotifiers
        if wait_for_more:  # doesnt seem to work? Could use this for sleep() otherwise.
            flag |= core.EventLoop.ProcessEventsFlag.WaitForMoreEvents
        cls.processEvents(flag, msecs)


class Application(ApplicationMixin, widgets.QApplication):
    """Manages the GUI application's control flow and main settings."""

    # def __init__(self, *args, **kwargs):
    #     super().__init__()


# Application.setStyle(widgets.Style())

if __name__ == "__main__":
    app = widgets.app()

    container = widgets.Widget()
    container.set_layout("horizontal")
    w = widgets.PlainTextEdit(parent=container)
    w2 = widgets.PlainTextEdit(parent=container)
    container.box.add(w)
    container.box.add(w2)
    container.show()
    # editor = widgeteditor.WidgetEditor(w)
    # editor.show()
    with app.debug_mode():
        app.sleep(1)
        app.exec()
