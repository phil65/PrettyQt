# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "prettyqt",
#   "pyside6",
#   "python-dateutil",
#   "packaging",
# ]
# ///

import inspect
import pathlib
from typing import Any

from PySide6.QtWidgets import QWidget

from prettyqt import custom_widgets, widgets


def create_widget_instance(widget_class: type[QWidget]) -> QWidget | None:
    """Create an instance of the given widget class.

    Args:
        widget_class: The class of the widget to instantiate.

    Returns:
        An instance of the widget if successful, None otherwise.
    """
    try:
        return widget_class()
    except Exception as e:  # noqa: BLE001
        print(f"Failed to create instance of {widget_class.__name__}: {e}")
        return None


def save_widget_screenshot(widget: QWidget, save_path: pathlib.Path) -> None:
    """Save a screenshot of the given widget.

    Args:
        widget: The widget to capture.
        save_path: The directory to save the screenshot in.
    """
    widget.show()
    app.processEvents()
    pixmap = widget.grab()
    filename = f"{type(widget).__name__}.png"
    pixmap.save(str(save_path / filename), "png")


def process_widget(widget_class: type[QWidget], save_path: pathlib.Path) -> None:
    """Process a single widget: create instance, save screenshot, and clean up.

    Args:
        widget_class: The class of the widget to process.
        save_path: The directory to save the screenshot in.
    """
    widget = create_widget_instance(widget_class)
    if widget is None or not isinstance(widget, widgets.WidgetMixin):
        return

    try:
        save_widget_screenshot(widget, save_path)
    except Exception as e:  # noqa: BLE001
        print(f"Error processing {widget_class.__name__}: {e}")
    finally:
        if hasattr(widget, "hide"):
            widget.hide()


def main() -> None:
    """Main function to process all widgets and save screenshots."""
    module_dict: dict[str, Any] = {"custom_widgets": custom_widgets}
    save_path = pathlib.Path().absolute() / "screenshots"
    save_path.mkdir(parents=True, exist_ok=True)

    for module in module_dict.values():
        class_members = inspect.getmembers(module, inspect.isclass)
        for _, widget_class in class_members:
            process_widget(widget_class, save_path)


if __name__ == "__main__":
    app = widgets.app()
    main()
