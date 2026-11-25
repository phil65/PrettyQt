"""Tests for PydanticForm / PydanticDialog."""

from __future__ import annotations

import enum
import pathlib
from typing import Annotated, Literal

import pytest


pydantic = pytest.importorskip("pydantic")

from prettyqt import custom_widgets, widgets  # noqa: E402
from prettyqt.custom_widgets import pydanticform as pf  # noqa: E402


class Color(enum.Enum):
    RED = "red"
    GREEN = "green"


class Inner(pydantic.BaseModel):
    x: int = 1
    label: str = "inner"


class Params(pydantic.BaseModel):
    name: str = pydantic.Field("abc", title="Name", description="The name")
    count: Annotated[int, pydantic.Field(ge=0, le=10)] = 3
    exclusive: int = pydantic.Field(5, gt=0, lt=100)
    factor: float = pydantic.Field(0.5, gt=0, lt=1, json_schema_extra={"step": 0.1})
    flag: bool = True
    how: Literal["left", "right"] = "left"
    color: Color = Color.RED
    colors: list[Color] = pydantic.Field(default_factory=list)
    columns: list[str] = pydantic.Field(default_factory=list)
    path: pathlib.Path | None = None
    limit: int | None = None
    inner: Inner = Inner()
    opt_inner: Inner | None = None
    notes: str = pydantic.Field("", json_schema_extra={"multiline": True})
    extra: dict[str, int] = pydantic.Field(default_factory=dict)


@pytest.fixture
def form(qtbot):
    widget = pf.PydanticForm(Params, debounce_ms=0)
    qtbot.addWidget(widget)
    return widget


def test_lazy_export():
    assert custom_widgets.PydanticForm is pf.PydanticForm
    assert custom_widgets.PydanticDialog is pf.PydanticDialog


def test_editor_types(form):
    expected = {
        "name": widgets.LineEdit,
        "count": widgets.SpinBox,
        "factor": widgets.DoubleSpinBox,
        "flag": widgets.CheckBox,
        "how": pf.ChoiceEditor,
        "color": pf.ChoiceEditor,
        "colors": pf.MultiChoiceEditor,
        "columns": pf.StringListEditor,
        "path": pf.OptionalEditor,
        "limit": pf.OptionalEditor,
        "inner": pf.ModelEditor,
        "opt_inner": pf.ModelEditor,
        "notes": widgets.PlainTextEdit,
        "extra": pf.JsonEditor,
    }
    for name, cls in expected.items():
        assert isinstance(form.get_editor(name), cls), name
    assert isinstance(form.get_editor("path").editor, custom_widgets.FileChooserButton)
    assert form.get_editor("name").toolTip() == "The name"


def test_defaults_roundtrip(form):
    assert form.get_value() == Params()
    assert form.is_valid()
    assert form.get_errors() == {}


def test_constraints(form):
    count = form.get_editor("count")
    assert (count.minimum(), count.maximum()) == (0, 10)
    exclusive = form.get_editor("exclusive")
    assert (exclusive.minimum(), exclusive.maximum()) == (1, 99)
    factor = form.get_editor("factor")
    assert factor.minimum() > 0
    assert factor.maximum() < 1
    assert factor.singleStep() == pytest.approx(0.1)


def test_set_value(form):
    value = Params(
        name="xyz",
        count=7,
        how="right",
        color=Color.GREEN,
        colors=[Color.GREEN],
        columns=["a", "b"],
        path=pathlib.Path("data.csv"),
        limit=4,
        inner=Inner(x=9, label="i"),
        opt_inner=Inner(x=2),
        notes="line1\nline2",
        extra={"a": 1},
    )
    form.set_value(value)
    assert form.get_value() == value
    form.set_value(Params())
    assert form.get_value() == Params()


def test_value_changed_emits_validated_model(qtbot, form):
    with qtbot.waitSignal(form.value_changed) as blocker:
        form.get_editor("name").set_value("new")
    assert isinstance(blocker.args[0], Params)
    assert blocker.args[0].name == "new"


def test_debounce(qtbot):
    form = pf.PydanticForm(Params, debounce_ms=50)
    qtbot.addWidget(form)
    received = []
    form.value_changed.connect(received.append)
    for i in range(5):
        form.get_editor("count").set_value(i)
    assert received == []
    qtbot.waitUntil(lambda: len(received) == 1)
    qtbot.wait(100)
    assert len(received) == 1
    assert received[0].count == 4  # noqa: PLR2004


def test_optional_editor(form):
    limit = form.get_editor("limit")
    assert not limit.checkbox.isChecked()
    assert not limit.editor.isEnabled()
    limit.set_value(5)
    assert limit.checkbox.isChecked()
    assert form.get_value().limit == 5  # noqa: PLR2004
    limit.checkbox.setChecked(False)
    assert form.get_value().limit is None


def test_list_editors(form):
    form.get_editor("columns").editor.set_text(" a, b ,,c")
    form.get_editor("colors").set_value([Color.RED, Color.GREEN])
    value = form.get_value()
    assert value.columns == ["a", "b", "c"]
    assert value.colors == [Color.RED, Color.GREEN]


def test_optional_nested_model(form):
    editor = form.get_editor("opt_inner")
    assert editor.isCheckable()
    assert form.get_value().opt_inner is None
    editor.setChecked(True)
    editor.form.get_editor("x").set_value(4)
    assert form.get_value().opt_inner == Inner(x=4)


class Validated(pydantic.BaseModel):
    text: str = pydantic.Field("ok", min_length=2)
    inner: Inner = Inner()
    low: int = 0
    high: int = 1

    @pydantic.field_validator("text")
    @classmethod
    def no_spaces(cls, v: str) -> str:
        if " " in v:
            msg = "no spaces allowed"
            raise ValueError(msg)
        return v

    @pydantic.model_validator(mode="after")
    def check_order(self):
        if self.low > self.high:
            msg = "low must not exceed high"
            raise ValueError(msg)
        return self


def test_inline_errors(qtbot):
    form = pf.PydanticForm(Validated, debounce_ms=0)
    qtbot.addWidget(form)
    form.show()
    errors = []
    form.errors_changed.connect(errors.append)
    form.get_editor("text").set_value("a b")
    assert "text" in form.get_errors()
    assert "no spaces allowed" in form.get_errors()["text"]
    assert form._error_labels["text"].isVisible()
    assert form.get_value() is None
    form.get_editor("text").set_value("ab")
    assert form.get_errors() == {}
    assert not form._error_labels["text"].isVisible()
    assert errors[-1] == {}
    # model-level error goes to the form-level label
    form.get_editor("low").set_value(5)
    assert pf.ROOT_KEY in form.get_errors()
    assert form._root_error.isVisible()
    assert "low must not exceed high" in form._root_error.text()


def test_nested_errors(qtbot):
    class Strict(pydantic.BaseModel):
        name: str = pydantic.Field("ok", pattern=r"^\w+$")

    class Outer(pydantic.BaseModel):
        strict: Strict = Strict()

    form = pf.PydanticForm(Outer, debounce_ms=0)
    qtbot.addWidget(form)
    form.show()
    sub = form.get_editor("strict").form
    sub.get_editor("name").set_value("not ok!")
    assert "strict.name" in form.get_errors()
    assert sub.get_errors().keys() == {"name"}
    assert sub._error_labels["name"].isVisible()


def test_hints(qtbot):
    def column_factory(name, info, hints):
        combo = pf.ChoiceEditor([(c, c) for c in ["a", "b", "c"]])
        combo.setObjectName("column_chooser")
        return combo

    class Hinted(pydantic.BaseModel):
        column: str = pydantic.Field("b", json_schema_extra={"widget": "column"})
        missing: str = pydantic.Field("x", json_schema_extra={"widget": "unknown"})
        how: str = pydantic.Field(
            "l", json_schema_extra={"mapping": {"l": "Left", "r": "Right"}}
        )
        unit: float = pydantic.Field(
            1.0, json_schema_extra={"suffix": " mm", "decimals": 2}
        )
        text: str = pydantic.Field("", json_schema_extra={"placeholder": "Type..."})
        secret: str = pydantic.Field("kept", json_schema_extra={"hidden": True})
        fixed: int = pydantic.Field(1, json_schema_extra={"readonly": True})
        folder: str = pydantic.Field("", json_schema_extra={"widget": "line_edit"})
        lines: list[str] = pydantic.Field([], json_schema_extra={"multiline": True})

    form = pf.PydanticForm(
        Hinted, debounce_ms=0, widget_factories={"column": column_factory}
    )
    qtbot.addWidget(form)
    assert form.get_editor("column").objectName() == "column"
    assert form.get_editor("column").get_value() == "b"
    assert isinstance(form.get_editor("missing"), widgets.LineEdit)
    how = form.get_editor("how")
    assert [how.itemText(i) for i in range(how.count())] == ["Left", "Right"]
    how.setCurrentIndex(1)
    assert form.get_value().how == "r"
    unit = form.get_editor("unit")
    assert unit.suffix() == " mm"
    assert unit.decimals() == 2  # noqa: PLR2004
    assert form.get_editor("text").placeholderText() == "Type..."
    with pytest.raises(KeyError):
        form.get_editor("secret")
    assert form.get_value().secret == "kept"
    form.set_value(Hinted(secret="other"))
    assert form.get_value().secret == "other"
    assert not form.get_editor("fixed").isEnabled()
    lines = form.get_editor("lines")
    lines.set_value(["a", "b"])
    assert lines.editor.text() == "a\nb"
    assert form.get_value().lines == ["a", "b"]


def test_required_fields(qtbot):
    class Required(pydantic.BaseModel):
        name: str
        size: int = pydantic.Field(ge=1)
        mode: Literal["a", "b"]

    form = pf.PydanticForm(Required, debounce_ms=0)
    qtbot.addWidget(form)
    assert form.get_value() == Required(name="", size=1, mode="a")


def test_instance_constructor(qtbot):
    form = pf.PydanticForm(Params(name="given", limit=2))
    qtbot.addWidget(form)
    assert form.get_model() is Params
    assert form.get_value() == Params(name="given", limit=2)


def test_dialog(qtbot):
    dialog = pf.PydanticDialog(Validated, title="Edit")
    qtbot.addWidget(dialog)
    assert dialog.windowTitle() == "Edit"
    ok = dialog.button_box["ok"]
    assert ok.isEnabled()
    dialog.form.get_editor("text").set_value("a b")
    assert not ok.isEnabled()
    dialog.accept()
    assert not dialog.is_accepted()
    dialog.form.get_editor("text").set_value("fine")
    assert ok.isEnabled()
    dialog.accept()
    assert dialog.is_accepted()
    assert dialog.get_value() == Validated(text="fine")
