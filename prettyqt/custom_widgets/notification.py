from __future__ import annotations

from queue import Empty, Queue
from typing import Callable, Literal

from prettyqt import core, gui, widgets
from prettyqt.qt import QtWidgets


CURSOR_MARGIN_TOP = 10
CURSOR_MARGIN_BOTTOM = 50
CURSOR_MARGIN_LEFT = 10
CURSOR_MARGIN_RIGHT = 10

DEFAULT_NOTIFICATION_STYLES = """
    Notification {
        font-size: 16px;
        padding: 0px;
        margin: 0px;
        border-radius: 6px;
    }
    Notification #message{
        color: #FFFFFF;
        padding: 0px;
        margin: 0px;
        width: 100%;
    }
    Notification #closeButton{
        color: #FFFFFF;
        padding: 0px;
        margin: 0px;
    }
    Notification#primary {
        background-color: #337ab7;
        border-color: #2e6da4;
    }
    Notification#success {
        background-color: #5cb85c;
        border-color: #4cae4c;
    }
    Notification#info {
        background-color: #5bc0de;
        border-color: #46b8da;
    }
    Notification#warning {
        background-color: #f0ad4e;
        border-color: #eea236;
    }
    Notification#danger {
        background-color: #d9534f;
        border-color: #d43f3a;
    }
    """

CategoryStr = Literal["primary", "success", "info", "warning", "danger"]
FadeOutValue = Literal[None, "fade_out"]
FadeInValue = Literal[None, "fade_in"]


class MessageLabel(widgets.Label):
    """Subclass of QLabel, which reimplements the resizeEvent() function.

    This is necessary because otherwise the notifications take up too much vertical
    space when texts they display become longer. This is because normally the height
    of a notification is calculated as the minimum height necessary for the text
    when the widget is horizontally resized to its minimum.
    """

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if (
            self.wordWrap()
            and self.sizePolicy().verticalPolicy() == widgets.SizePolicy.Minimum
        ):
            new_height = self.heightForWidth(self.width())
            if new_height < 1:
                return
            self.setMaximumHeight(new_height)


class Notification(widgets.Widget):
    """Class representing a single notification."""

    close_clicked = core.Signal()

    def __init__(
        self,
        message: str,
        category: CategoryStr,
        timeout=None,
        autohide: bool = False,
        buttontext: str | None = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        # Store instance variables
        self.message = message
        self.category = category
        self.timeout = timeout
        self.autohide = autohide

        # Set Object name for reference
        self.setObjectName(category)
        self.set_layout("horizontal", margin=0)

        # Create a message area
        message_area = widgets.BoxLayout("horizontal")
        message_area.set_margin(0)

        # Create the layout
        self.message_display = MessageLabel()
        self.message_display.setObjectName("message")
        self.message_display.set_size_policy("minimum", "minimum")
        self.message_display.setWordWrap(True)

        # Create a button that can close notifications
        if not buttontext:
            close_button = widgets.PushButton("\u2715")
        else:
            close_button = widgets.PushButton(buttontext)
            close_button.setStyleSheet("text-decoration: underline;")
        close_button.set_size_policy("fixed", "fixed")
        close_button.setFlat(True)
        close_button.setObjectName("closeButton")
        close_button.clicked.connect(self.close_clicked)

        # Add everything together
        message_area.addWidget(self.message_display)
        # message_area.addStretch(1)
        message_area.addWidget(close_button)
        self.layout().addLayout(message_area)

        # Initialize some variables
        # self.setStyle(category)
        self.setVisible(False)

        # Flag that is set if notification is being removed. This can be used to
        # make sure that even though the notification has not been really removed
        # yet (because it is for example in a fade out animation), it is in the
        # process of being removed
        self.is_being_removed = False
        self.is_fading_in = False
        self.opacity_effect = widgets.GraphicsOpacityEffect(self)

        # Fade in animation
        self.fade_in_anim = core.PropertyAnimation()
        self.fade_in_anim.apply_to(self.opacity_effect, "opacity")
        self.fade_in_anim.set_range(0.0, 1.0)

        # Fade out animation
        self.fade_out_anim = core.PropertyAnimation()
        self.fade_out_anim.apply_to(self.opacity_effect, "opacity")
        self.fade_in_anim.set_range(1.0, 0.0)

    def display(self):
        """Display the notification."""
        self.message_display.setText(self.message)
        self.show()
        self.raise_()

    def close(self):
        """Close the notification."""
        super().close()
        self.deleteLater()

    def fade_in(self, duration: int):
        """Fade in the notification.

        Arguments:
            duration : int
                The desired duration of the animation

        Raises:
            TypeError: duration is not an integer
        """
        if type(duration) != int:
            raise TypeError("duration should be an integer")
        self.setGraphicsEffect(self.opacity_effect)
        self.fade_in_anim.setDuration(duration)
        self.is_fading_in = True
        self.fade_in_anim.finished.connect(self.on_fade_in_finished)
        self.display()
        self.fade_in_anim.start()

    def on_fade_in_finished(self):
        self.is_fading_in = False

    def fade_out(self, finished_callback: Callable, duration: int):
        """Fade out the notification.

        Parameters
        ----------
        finished_callback : callable
            The function to call after the animation has finished (to for instance
            clean up the notification)
        duration : int
            The desired duration of the animation

        Raises
        ------
        TypeError: the wrong datatype is specified for any of the parameters.

        """
        if not callable(finished_callback):
            raise TypeError("finished_callback should be a callable")
        if type(duration) != int:
            raise TypeError("duration should be an integer")

        self.setGraphicsEffect(self.opacity_effect)
        self.fade_out_anim.setDuration(duration)
        self.fade_out_anim.finished.connect(lambda: finished_callback(self))
        self.is_being_removed = True
        self.fade_out_anim.start()

    def paintEvent(self, pe):
        """Redefinition of paintEvent, do not call directly.

        Makes class Notification available in style sheets. Interal Qt function.
        Should not be called directly.
        """
        o = widgets.StyleOption.based_on(self)
        p = gui.Painter(self)
        self.style().drawPrimitive(widgets.Style.PE_Widget, o, p, self)

    @property
    def message(self) -> str:
        """The currently set message to display."""
        return self._message

    @message.setter
    def message(self, value: str):
        """Set the message to display."""
        self._message = value

    @property
    def category(self) -> CategoryStr:
        """The currently set category of this notification."""
        return self._category

    @category.setter
    def category(self, value: CategoryStr):
        """Set the category of this notification.

        Arguments:
            value : {'primary','success','info','warning','danger'}
                The category specification

        Raises:
            ValueError: The category is other than one of the expected values.
        """
        allowed_values = ["primary", "success", "info", "warning", "danger"]
        if value not in allowed_values:
            raise ValueError(
                f"{value!r} is not a valid value. Should be one of {allowed_values}"
            )
        self._category = value

    def enterEvent(self, e):
        """When the notification is set to auto-hide, mouseover closes it."""
        if self.autohide:
            self.close_clicked.emit()


class NotificationArea(widgets.Widget):
    """Notification area to show notifications in.

    Will be projected on top of another QWidget which should be passed as an argument
    to this class.
    """

    def __init__(
        self,
        target_widget: QtWidgets.QWidget,
        use_global_css: bool = False,
        use_queue: bool = True,
        max_messages: int = 2,
    ):
        """Constructor.

        Arguments:
            target_widget : QtWidgets.QWidget
                The widget to project the notifications on
            use_global_css : bool (default: False)
                Flag which indicates whether global style sheets should be used
                (which have been set at app-level). If False, the default style sheets
                stored at DEFAULT_NOTIFICATION_STYLES will be loaded.
            use_queue : bool (default: True)
                Indicates whether a message queue should be implemented. This will only
                show *max_messages* at the same time and will put all other messages in a
                queue. Once a message disappears, the next one in the queue will be shown
                (up to max_messages at the same time)
            max_messages : int (default: 2)
                The number of messages to display at the same time.

        Raises:
            TypeError : target_widget is not an object that inherits QWidget
        """
        if not isinstance(target_widget, QtWidgets.QWidget):
            raise TypeError("target_widget is not a QWidget (or child of it")

        # Pop some variables from kwargs.
        self.use_queue = use_queue
        self.max_messages = max_messages
        super().__init__(parent=target_widget)

        if not use_global_css:
            self.setStyleSheet(DEFAULT_NOTIFICATION_STYLES)

        if self.use_queue:
            self.queue: Queue[Notification] = Queue()

        self.target_widget = target_widget
        self.set_margin(0)

        notification_area_layout = widgets.BoxLayout("vertical")
        self.setLayout(notification_area_layout)

        # Init effects to None
        self.entry_effect: FadeInValue = None
        self.entry_effect_duration = 250
        self.exit_effect: FadeOutValue = None
        self.exit_effect_duration = 500

        # Store original target classes resizeEvent to be called in our own
        # function
        self.target_resize_event = target_widget.resizeEvent
        # Overwrite resizeEvent function of target_widget to capture it ourself
        # (parent's resizeEvent will be called in our function too)
        self.target_widget.resizeEvent = self.resizeEvent  # type: ignore
        self.hide()

    def __delete_notification(self, notification: Notification):
        """Close and destroy the supplied notification."""
        notification.close()
        self.layout().removeWidget(notification)

        self.adjustSize()
        # Hide notification area if it doesn't contain any items
        if self.layout().count() == 0:
            self.hide()

        if self.use_queue:
            try:
                notification = self.queue.get(False)
                self._show_notification(notification)
            except Empty:
                pass

    # Public functions
    def set_entry_effect(self, effect: FadeInValue, duration: int = 250):
        """Set the effect with which the notifications are to appear.

        Arguments:
            effect : {'fade_in', None}
                The effect which should be used (for now only 'fade_in' is available)
                if None is passed for this argument, no effect will be used and the
                notifcations will just appear directly.
            duration : int (default: 250 ms)
                The duration of the effect in milliseconds

        Raises:
            TypeError: the object passed for duration is not an int
            ValueError: duration is less than 0, or effect has an invalid value
        """
        if effect not in ["fade_in", None]:
            raise ValueError("Invalid entry effect")
        if not isinstance(duration, int):
            raise TypeError("Duration should be an int")
        if duration < 0:
            raise ValueError("Duration should be larger than 0")

        self.entry_effect = effect
        self.entry_effect_duration = duration

    def set_exit_effect(self, effect: FadeOutValue, duration: int = 500):
        """Set the effect with which the notifications are to disappear.

        Arguments:
            effect : {'fade_out', None}
                the effect which should be used (for now only 'fade_out' is available)
                if None is passed for this argument, no effect will be used and the
                notifcations will just appear directly.
            duration : int (default: 1000 ms)
                The duration of the effect in milliseconds

        Raises:
            TypeError: the object passed for duration is not an int
            ValueError: duration is less than 0, or effect has an invalid value
        """
        if effect not in ["fade_out", None]:
            raise ValueError("Invalid exit effect")
        if not isinstance(duration, int):
            raise TypeError("Duration should be an int")
        if duration < 0:
            raise ValueError("Duration should be larger than 0")

        self.exit_effect = effect
        self.exit_effect_duration = duration

    @core.Slot(str, str, int, bool)
    @core.Slot(str, str, int, bool, str)
    def display(
        self,
        message: str,
        category: CategoryStr,
        timeout: int = 5000,
        autohide: bool = False,
        buttontext: str | None = None,
    ):
        """Display a notification.

        If a queue is used, then the notification will only be shown directly
        if the number of notifications shown is smaller than max_messages.

        Arguments:
            message : str
                The message to display
            category : {'primary', 'success', 'info', 'warning', 'danger'}
                The type of notification that should be shown. Adheres to bootstrap
                standards which are primary, success, info, warning and danger
            timeout : int, optional
                The duration for which the notification should be shown. If None then
                the notification will be shown indefinitely
            buttontext : str, optional
                The text to display on the closing button. If not provided a cross
                will be shown.

        Raises:
            ValueError: the category is other than one of the expected values.
        """
        notification = Notification(
            message, category, timeout, autohide, buttontext, self
        )
        notification.close_clicked.connect(self.remove)

        # Queue if max amount of notifications is shown
        if self.use_queue and self.layout().count() >= self.max_messages:
            self.queue.put(notification)
        else:
            self._show_notification(notification)

    def _cursor_in_area(self) -> bool:
        geom = self.geometry()
        top_left = self.mapToGlobal(geom.topLeft())
        bottom_right = self.mapToGlobal(geom.bottomRight())
        geom = core.Rect(top_left, bottom_right)
        geom.setTop(geom.top() - CURSOR_MARGIN_TOP)
        geom.setBottom(geom.bottom() + CURSOR_MARGIN_BOTTOM)
        geom.setLeft(geom.left() - CURSOR_MARGIN_LEFT)
        geom.setRight(geom.right() + CURSOR_MARGIN_RIGHT)
        cursor_pos = gui.Cursor.get_position()
        return geom.contains(cursor_pos)

    def _show_notification(self, notification: Notification):
        if self._cursor_in_area():
            core.Timer.singleShot(1000, lambda: self._show_notification(notification))
            return
        if not self.isVisible():
            self.show()
            self.raise_()
        self.layout().addWidget(notification)
        # Check for entry effects
        if self.entry_effect is not None:
            if self.entry_effect == "fade_in":
                notification.fade_in(self.entry_effect_duration)
        else:
            notification.display()

        self.adjustSize()
        if notification.timeout is not None and notification.timeout > 0:
            core.Timer.singleShot(notification.timeout, lambda: self.remove(notification))

    @core.Slot()
    def remove(self, notification: Notification | None = None):
        """Removes a notification.

        Arguments:
            notification : Notification (default: None)
                The notification to remove. This function also serves as a PyQt slot
                for signals emitted from a Notification. In this case, the Notification
                object is retrieved by using self.sender()

        Raises:
            ValueError: notification is not None or a Notification

        """
        # This function also functions as a pyqt slot. In that case, no
        # notification argument is passed, but this is set as self.sender()
        if notification is None:
            notification = self.sender()
        if notification.is_being_removed or notification.is_fading_in:
            return
        notification.is_being_removed = True

        # Check if notification is still present (and has not manually been
        # closed before this function is called by a timeout)
        if notification not in self.layout():
            return

        # Implement animation here
        if self.exit_effect == "fade_out":
            notification.fade_out(self.__delete_notification, self.exit_effect_duration)
        else:
            self.__delete_notification(notification)

    # Internal Qt functions
    def resizeEvent(self, event):
        """Internal QT function (do not call directly)."""
        self.target_resize_event(event)
        newsize = event.size()
        self.setFixedWidth(newsize.width())
        self.adjustSize()

    def paintEvent(self, pe):
        """Redefinition of paintEvent.

        Makes class NotificationArea available in style sheets.
        Internal QT function (do not call directly).
        """
        o = widgets.StyleOption.based_on(self)
        p = gui.Painter(self)
        self.style().drawPrimitive(widgets.Style.PE_Widget, o, p, self)


if __name__ == "__main__":
    app = widgets.app()
    p = widgets.PushButton("test")
    noti = NotificationArea(p)
    p.clicked.connect(lambda: noti.display("test", "danger", timeout=2000))
    p.show()
    app.main_loop()
