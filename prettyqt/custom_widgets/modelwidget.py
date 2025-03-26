"""Widget for displaying and editing Pydantic models."""

from __future__ import annotations

import enum
import logging
import pathlib
import re
import sys
from typing import Any, Literal, TypeVar, get_args, get_origin

import pydantic
from pydantic import BaseModel

from prettyqt import core, custom_widgets, gui, widgets


logger = logging.getLogger(__name__)

# TypeVar for the BaseModel generic type
ModelT = TypeVar("ModelT", bound=BaseModel)


class OptionalFieldWidget(widgets.Widget):
    """Widget for editing an optional field that can be None.

    Consists of a checkbox to enable/disable the field and the actual field editor.
    """

    value_changed = core.Signal()

    def __init__(
        self,
        editor: widgets.Widget,
        parent: widgets.QWidget | None = None,
    ):
        super().__init__(parent)
        self._editor = editor
        self._checkbox = widgets.CheckBox("Enable", checked=True)

        layout = self.set_layout("horizontal", margin=0)
        layout.add(self._checkbox)
        layout.add(self._editor)

        # Connect signals
        self._checkbox.toggled.connect(self._on_checkbox_toggled)
        if hasattr(self._editor, "value_changed"):
            self._editor.value_changed.connect(self.value_changed)

    def _on_checkbox_toggled(self, checked: bool) -> None:
        """Handle checkbox state changes."""
        self._editor.setEnabled(checked)
        self.value_changed.emit()

    def get_value(self) -> Any | None:
        """Return the current value or None if disabled."""
        if not self._checkbox.isChecked():
            return None
        if hasattr(self._editor, "get_value"):
            return self._editor.get_value()
        return None

    def set_value(self, value: Any | None) -> None:
        """Set a new value and update the UI."""
        is_enabled = value is not None
        self._checkbox.setChecked(is_enabled)
        self._editor.setEnabled(is_enabled)

        if is_enabled and hasattr(self._editor, "set_value"):
            self._editor.set_value(value)


class LiteralWidget(widgets.ComboBox):
    """Widget for selecting from a set of literal values."""

    def __init__(
        self,
        values: tuple[Any, ...],
        parent: widgets.QWidget | None = None,
    ):
        super().__init__(parent)
        self._values = values

        # Add items with string representation
        for value in values:
            self.addItem(str(value), value)

    def get_value(self) -> Any:
        """Return the currently selected literal value."""
        return self.currentData()

    def set_value(self, value: Any) -> None:
        """Set the selected value."""
        for i in range(self.count()):
            if self.itemData(i) == value:
                self.setCurrentIndex(i)
                return

        # If not found, select first item as fallback
        if self.count() > 0:
            self.setCurrentIndex(0)


class ModelWidget[ModelT](widgets.Widget):
    """Widget that displays and edits Pydantic model attributes.

    Takes either a BaseModel class or instance and generates appropriate
    widgets for each field based on its type.

    Parameters:
        model: A Pydantic BaseModel class or instance
        parent: Parent widget
        show_confirm_button: Whether to show a confirm button

    Signals:
        model_changed: Emitted when any field value changes
        confirm_clicked: Emitted when the confirm button is clicked
    """

    model_changed = core.Signal(object)
    confirm_clicked = core.Signal()

    def __init__(
        self,
        model: type[ModelT] | ModelT,
        parent: widgets.QWidget | None = None,
        show_confirm_button: bool = False,
    ):
        super().__init__(parent)
        self._model_class: type[ModelT] = (
            model if isinstance(model, type) else type(model)
        )
        self._current_model = None if isinstance(model, type) else model
        self._editors: dict[str, widgets.QWidget] = {}
        self._field_info: dict[str, pydantic.fields.FieldInfo] = {}

        # Initialize UI
        self._init_ui(show_confirm_button)

        # Populate form with fields
        self._create_form_fields()

        # Set initial values
        if self._current_model:
            self._update_editors_from_model()

    def _init_ui(self, show_confirm_button: bool) -> None:
        """Initialize the widget's UI components."""
        main_layout = self.set_layout("vertical")

        # Form layout for fields
        self._form_layout = widgets.FormLayout()
        main_layout.addLayout(self._form_layout)

        # Optional confirm button
        if show_confirm_button:
            button_layout = widgets.HBoxLayout()
            button_layout.addStretch()
            self._confirm_button = widgets.PushButton(
                "Confirm", clicked=self.confirm_clicked.emit
            )
            button_layout.addWidget(self._confirm_button)
            main_layout.addLayout(button_layout)

    def _create_form_fields(self) -> None:
        """Create form fields based on model schema."""
        model_fields = self._model_class.model_fields  # pyright: ignore

        for field_name, field_info in model_fields.items():
            # Skip private fields (starting with underscore)
            if field_name.startswith("_"):
                continue

            # Store field info for later use
            self._field_info[field_name] = field_info

            # Create editor widget
            editor = self._get_editor_for_field(field_name, field_info)
            if editor is None:
                logger.warning("No editor found for field %s", field_name)
                continue

            # Setup change signal
            if hasattr(editor, "value_changed"):
                editor.value_changed.connect(
                    lambda *args, name=field_name: self._on_field_changed(name)
                )

            # Add label and editor to form
            label = widgets.Label(field_name.replace("_", " ").title())

            # Set tooltip if description is available
            if description := getattr(field_info, "description", None):
                label.setToolTip(description)
                editor.setToolTip(description)

            self._form_layout.addRow(label, editor)
            self._editors[field_name] = editor

    def _get_editor_for_field(
        self, field_name: str, field_info: pydantic.fields.FieldInfo
    ) -> widgets.Widget | None:
        """Return an appropriate editor widget for the given field type."""
        # Check for optional types (Union with None)
        annotation = field_info.annotation
        is_optional = False

        # Strip Optional/Union with None
        origin = get_origin(annotation)
        if origin is not None and origin is type(None).__or__:  # Handle | None
            annotation_args = get_args(annotation)
            annotation = annotation_args[0]  # Get the non-None type
            is_optional = True

        # Check for Literal
        if get_origin(annotation) is Literal:
            literal_values = get_args(annotation)
            editor = LiteralWidget(literal_values)
            # Wrap in OptionalFieldWidget if it's optional
            if is_optional:
                return OptionalFieldWidget(editor)  # type: ignore
            return editor  # type: ignore

        # Get default value to determine type
        if self._current_model:
            val = getattr(self._current_model, field_name)
        else:
            val = field_info.default

            # Handle default_factory if needed
            if (
                val is pydantic.fields.PydanticUndefined
                and hasattr(field_info, "default_factory")
                and field_info.default_factory is not None
            ):
                val = field_info.default_factory()  # type: ignore

        # For annotations or other cases where default might not be available
        if val is pydantic.fields.PydanticUndefined:
            # Get from type annotation
            field_type = annotation
            if field_type is bool:
                editor = widgets.CheckBox()
            elif field_type is int:
                editor = widgets.SpinBox()
            elif field_type is float:
                editor = widgets.DoubleSpinBox()
            elif field_type is str:
                editor = widgets.LineEdit()
                editor.setFrame(False)
            elif field_type is pathlib.Path:
                editor = custom_widgets.FileChooserButton()
            elif isinstance(field_type, type) and issubclass(field_type, BaseModel):
                # Nested model support
                editor = ModelWidget(field_type)  # type: ignore
            else:
                # Add more type checks as needed
                editor = None

            if editor is not None:
                self._apply_constraints(editor, field_info)
                # Wrap in OptionalFieldWidget if it's optional
                if is_optional:
                    return OptionalFieldWidget(editor)  # type: ignore
                return editor  # type: ignore

        # Get editor based on value type
        editor = self._create_editor_for_value(val)

        # Apply constraints if available
        if editor is not None:
            self._apply_constraints(editor, field_info)
            # Wrap in OptionalFieldWidget if it's optional
            if is_optional:
                return OptionalFieldWidget(editor)  # type: ignore

        return editor  # type: ignore

    def _create_editor_for_value(self, val: Any) -> widgets.QWidget | None:  # noqa: PLR0911
        """Create an editor widget based on the value type."""
        match val:
            case bool():
                return widgets.CheckBox()
            case enum.Flag():
                widget = custom_widgets.EnumFlagWidget()
                widget._set_enum_class(type(val))
                return widget
            case enum.Enum():
                widget = custom_widgets.EnumComboBox()
                widget._set_enum_class(type(val))
                return widget
            case int():
                return widgets.SpinBox()
            case float():
                return widgets.DoubleSpinBox()
            case (int(), *_):
                return custom_widgets.ListInput(typ=int)
            case (float(), *_):
                return custom_widgets.ListInput(typ=float)
            case (str(), *_):
                return custom_widgets.StringListEdit()
            case pathlib.Path():
                return custom_widgets.FileChooserButton()
            case str():
                widget = widgets.LineEdit()
                widget.setFrame(False)
                return widget
            case core.QRegularExpression() | re.Pattern():
                return custom_widgets.RegexInput(show_error=False)
            case core.QTime():
                return widgets.TimeEdit()
            case core.QDate():
                return widgets.DateEdit()
            case core.QDateTime():
                return widgets.DateTimeEdit()
            case core.QPoint():
                return custom_widgets.PointEdit()
            case core.QSize():
                return custom_widgets.SizeEdit()
            case core.QRect():
                return custom_widgets.RectEdit()
            case gui.QKeySequence():
                return widgets.KeySequenceEdit()
            case gui.QRegion():
                return custom_widgets.RegionEdit()
            case gui.QFont():
                return widgets.FontComboBox()
            case gui.QColor():
                return custom_widgets.ColorComboBox()
            case gui.QBrush():
                return custom_widgets.BrushEdit()
            case widgets.QSizePolicy():
                return custom_widgets.SizePolicyEdit()
            case core.QUrl():
                return custom_widgets.UrlLineEdit()
            case gui.QPalette():
                return custom_widgets.PaletteEdit()
            case gui.QCursor():
                return custom_widgets.CursorEdit()
            case gui.QIcon():
                return custom_widgets.IconEdit()
            case core.QLocale():
                return custom_widgets.LocaleEdit()
            case slice():
                return custom_widgets.SliceEdit()
            case range():
                return custom_widgets.RangeEdit()
            case BaseModel():
                # Handle nested Pydantic model
                return ModelWidget(val)
            case _:
                logger.warning(f"No matching editor for type {type(val)}")  # noqa: G004
                return None

    def _apply_constraints(
        self, editor: widgets.QWidget, field_info: pydantic.fields.FieldInfo
    ) -> None:
        """Apply field constraints to editor widget if applicable."""
        # Handle minimum/maximum constraints for numeric fields
        if isinstance(editor, widgets.SpinBox | widgets.DoubleSpinBox):
            if hasattr(field_info, "ge") and field_info.ge is not None:  # pyright: ignore
                editor.set_minimum(field_info.ge)  # pyright: ignore
            elif hasattr(field_info, "gt") and field_info.gt is not None:  # pyright: ignore
                editor.set_minimum(
                    field_info.gt  # pyright: ignore
                    + (1 if isinstance(editor, widgets.SpinBox) else 0.000001)
                )

            if hasattr(field_info, "le") and field_info.le is not None:  # pyright: ignore
                editor.set_maximum(field_info.le)  # pyright: ignore
            elif hasattr(field_info, "lt") and field_info.lt is not None:  # pyright: ignore
                editor.set_maximum(
                    field_info.lt  # pyright: ignore
                    - (1 if isinstance(editor, widgets.SpinBox) else 0.000001)
                )

        # Handle string patterns for line edits
        if (
            isinstance(editor, widgets.LineEdit)
            and hasattr(field_info, "pattern")
            and field_info.pattern  # pyright: ignore
        ):
            editor.set_regex_validator(field_info.pattern)  # pyright: ignore

    def _update_editors_from_model(self) -> None:
        """Update editors with values from the current model."""
        if not self._current_model:
            return

        for field_name, editor in self._editors.items():
            if hasattr(self._current_model, field_name):
                value = getattr(self._current_model, field_name)
                if hasattr(editor, "set_value"):
                    editor.set_value(value)  # pyright: ignore

    def _on_field_changed(self, field_name: str) -> None:
        """Handle changes in field values."""
        if field_name not in self._editors:
            return

        try:
            # Create a new model with updated values
            model_data = self._get_model_data()
            new_model = self._model_class(**model_data)

            # Update current model and emit change signal
            self._current_model = new_model
            self.model_changed.emit(new_model)
        except Exception:
            logger.exception("Error updating model")

    def _get_model_data(self) -> dict[str, Any]:
        """Get a dictionary of field values from editors."""
        data = {}
        for field_name, editor in self._editors.items():
            if hasattr(editor, "get_value"):
                data[field_name] = editor.get_value()  # pyright: ignore
        return data

    def get_model(self) -> ModelT:
        """Get the current model with values from the form."""
        if self._current_model is None:
            model_data = self._get_model_data()
            self._current_model = self._model_class(**model_data)
        return self._current_model

    def set_model(self, model: ModelT) -> None:
        """Set a new model and update the form."""
        if not isinstance(model, self._model_class):
            typ = type(model).__name__
            msg = f"Expected model of type {self._model_class.__name__}, got {typ}"
            raise TypeError(msg)

        self._current_model = model
        self._update_editors_from_model()


if __name__ == "__main__":
    from enum import Enum

    app = widgets.app()

    class Color(str, Enum):
        RED = "red"
        GREEN = "green"
        BLUE = "blue"

    class Address(BaseModel):
        street: str
        city: str
        zip_code: str

    class Person(BaseModel):
        name: str
        age: int
        is_active: bool = True
        favorite_color: Color = Color.BLUE
        email: str | None = None
        address: Address | None = None
        status: Literal["new", "active", "inactive"] = "new"

    # Create initial model
    address = Address(street="123 Main St", city="New York", zip_code="10001")
    person = Person(name="John Doe", age=30, address=address)

    # Create and show widget
    widget = ModelWidget(person, show_confirm_button=True)
    widget.model_changed.connect(lambda model: print(f"Model updated: {model}"))
    widget.confirm_clicked.connect(lambda: print(f"Final model: {widget.get_model()}"))
    widget.show()

    sys.exit(app.exec())
