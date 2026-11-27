"""Headless Qt UI inspection, screenshot capture, and layout diagnostics.

Provides lightweight utilities and a `UIInspector` helper for driving any Qt /
PrettyQt widget offscreen, waiting for async state to settle, capturing PNG
screenshots, dumping indented widget trees, and detecting common layout issues
(clipped labels, cramped buttons, zero-size widgets, and out-of-bounds children).
"""

from dataclasses import asdict, dataclass
import json
import math
import os
import pathlib
import re
import time
from typing import TYPE_CHECKING, Any

from prettyqt.qt import QtCore, QtGui, QtWidgets


if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Mapping


CLIP_TOLERANCE_PX = 4
BOUNDS_TOLERANCE_PX = 2
LABEL_PREVIEW_LEN = 48
BUTTON_PREVIEW_LEN = 40

_DEFAULT_ZERO_SIZE_CLASSES = frozenset({"TrackingSpacer", "HeaderView", "QHeaderView"})
_DEFAULT_ZERO_SIZE_NAMES = frozenset({"qt_scrollarea_viewport"})
_RICH_TEXT_RE = re.compile(r"<[/!]?[A-Za-z][A-Za-z0-9]*(?:[\s/>]|$)")


@dataclass(frozen=True, slots=True)
class CaptureInfo:
    """Metadata for a captured widget screenshot."""

    scenario: str
    target: str
    path: str
    width: int
    height: int


@dataclass(frozen=True, slots=True)
class LayoutWarning:
    """A layout diagnostic emitted while inspecting a widget tree."""

    widget: str
    kind: str
    detail: str


def ensure_offscreen() -> None:
    """Configure Qt to use the offscreen platform plugin if unset."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


def pump(
    app: QtCore.QCoreApplication | None = None,
    ms: int = 40,
) -> None:
    """Process Qt events for `ms` milliseconds so layouts and timers settle."""
    qapp = app if app is not None else QtCore.QCoreApplication.instance()
    if qapp is None:
        return
    flags = QtCore.QEventLoop.ProcessEventsFlag.AllEvents
    deadline = time.monotonic() + ms / 1000.0
    while time.monotonic() < deadline:
        qapp.processEvents(flags, 10)
        time.sleep(0.005)
    qapp.processEvents(flags)


def wait_until(
    predicate: Callable[[], object],
    *,
    timeout_ms: int = 5000,
    interval_ms: int = 10,
    app: QtCore.QCoreApplication | None = None,
) -> bool:
    """Process Qt events until `predicate()` returns truthy or `timeout_ms` elapses."""
    qapp = app if app is not None else QtCore.QCoreApplication.instance()
    flags = QtCore.QEventLoop.ProcessEventsFlag.AllEvents
    deadline = time.monotonic() + timeout_ms / 1000.0
    step_s = max(interval_ms, 1) / 1000.0
    while True:
        if qapp is not None:
            qapp.processEvents(flags, interval_ms)
        if predicate():
            return True
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return False
        time.sleep(min(step_s, remaining))


def find_widget(
    root: QtWidgets.QWidget,
    selector: str,
) -> QtWidgets.QWidget | None:
    """Resolve a widget selector within `root`.

    Resolves `"window"` / `"root"` (or `root.objectName()`) to `root`,
    then checks `QDockWidget` children by `objectName`, and finally falls
    back to `root.findChild(QWidget, selector)`.
    """
    if selector in ("window", "root") or (selector and selector == root.objectName()):
        return root
    for dock in root.findChildren(QtWidgets.QDockWidget):
        if dock.objectName() == selector:
            return dock
    return root.findChild(QtWidgets.QWidget, selector)


def capture(
    widget: QtWidgets.QWidget,
    path: str | os.PathLike[str],
    *,
    scenario: str = "",
    target: str = "",
) -> CaptureInfo:
    """Grab a screenshot of `widget` and save it to `path`."""
    out_path = pathlib.Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pixmap = widget.grab()
    pixmap.save(str(out_path))
    return CaptureInfo(
        scenario=scenario,
        target=target,
        path=str(out_path),
        width=pixmap.width(),
        height=pixmap.height(),
    )


def default_ignore_zero_size(widget: QtWidgets.QWidget) -> bool:
    """Return True for internal Qt widgets that legitimately have zero size."""
    if (
        type(widget).__name__ in _DEFAULT_ZERO_SIZE_CLASSES
        or widget.objectName() in _DEFAULT_ZERO_SIZE_NAMES
    ):
        return True
    return isinstance(widget, QtWidgets.QMenuBar) and not widget.actions()


def _label_for(widget: QtWidgets.QWidget) -> str:
    name = widget.objectName()
    cls = type(widget).__name__
    return f"{cls}#{name}" if name else cls


def _might_be_rich_text(text: str) -> bool:
    fn = getattr(QtGui.Qt, "mightBeRichText", None)
    if callable(fn):
        return bool(fn(text))
    return bool(_RICH_TEXT_RE.search(text))


def _label_text_metrics(widget: QtWidgets.QLabel) -> tuple[str, int]:
    """Return `(plain_text, required_width_px)` for a `QLabel`."""
    raw = widget.text()
    if not raw:
        return "", 0
    fmt = widget.textFormat()
    is_markdown = fmt == QtCore.Qt.TextFormat.MarkdownText
    is_rich = fmt == QtCore.Qt.TextFormat.RichText or (
        fmt == QtCore.Qt.TextFormat.AutoText and _might_be_rich_text(raw)
    )
    if is_rich or is_markdown:
        doc = QtGui.QTextDocument()
        doc.setDefaultFont(widget.font())
        doc.setDocumentMargin(0)
        if is_markdown:
            doc.setMarkdown(raw)
        else:
            doc.setHtml(raw)
        return doc.toPlainText(), math.ceil(doc.idealWidth())
    fm = widget.fontMetrics()
    lines = raw.splitlines() or [raw]
    needed = max(fm.horizontalAdvance(line) for line in lines)
    return raw, needed


def _is_scroll_viewport(widget: QtWidgets.QWidget) -> bool:
    if widget.objectName() == "qt_scrollarea_viewport":
        return True
    grandparent = widget.parentWidget()
    return (
        isinstance(grandparent, QtWidgets.QAbstractScrollArea)
        and grandparent.viewport() is widget
    )


def _is_offscreen_dock(widget: QtWidgets.QWidget) -> bool:
    """Detect inactive tabified `QDockWidget`s parked offscreen by Qt."""
    if not isinstance(widget, QtWidgets.QDockWidget) or widget.isFloating():
        return False
    geo = widget.geometry()
    return geo.right() < 0 or geo.bottom() < 0


def _check_out_of_bounds(
    widget: QtWidgets.QWidget,
    root: QtWidgets.QWidget,
) -> LayoutWarning | None:
    if widget is root or (
        widget.isWindow() and widget.windowType() != QtCore.Qt.WindowType.SubWindow
    ):
        return None
    parent = widget.parentWidget()
    if (
        parent is None
        or parent.width() <= 0
        or parent.height() <= 0
        or _is_scroll_viewport(parent)
        or _is_offscreen_dock(widget)
    ):
        return None
    geo = widget.geometry()
    if geo.width() <= 0 or geo.height() <= 0:
        return None
    pw, ph = parent.width(), parent.height()
    if (
        geo.x() < -BOUNDS_TOLERANCE_PX
        or geo.y() < -BOUNDS_TOLERANCE_PX
        or geo.x() + geo.width() > pw + BOUNDS_TOLERANCE_PX
        or geo.y() + geo.height() > ph + BOUNDS_TOLERANCE_PX
    ):
        return LayoutWarning(
            _label_for(widget),
            "out-of-bounds",
            (
                f"geometry [{geo.x()},{geo.y()} {geo.width()}x{geo.height()}] "
                f"exceeds parent {_label_for(parent)} ({pw}x{ph})"
            ),
        )
    return None


def inspect_tree(
    root: QtWidgets.QWidget,
    *,
    max_depth: int = 8,
    ignore_zero_size: Callable[[QtWidgets.QWidget], bool] | None = None,
) -> tuple[list[str], list[LayoutWarning]]:
    """Return an indented widget tree and layout diagnostics for `root`.

    Checks for:
    - `clipped-label`: visible non-wrapping `QLabel` whose rendered text exceeds width
    - `cramped-button`: visible `QAbstractButton` narrower than its `sizeHint()`
    - `zero-size`: visible widget with 0 width or height
    - `out-of-bounds`: visible child / `SubWindow` extending outside its parent's rect
    """
    ignore_zero = (
        ignore_zero_size if ignore_zero_size is not None else default_ignore_zero_size
    )
    lines: list[str] = []
    warnings: list[LayoutWarning] = []

    def visit(widget: QtWidgets.QWidget, depth: int) -> None:
        if depth > max_depth or not widget.isVisible():
            return
        if widget is not root and _is_offscreen_dock(widget):
            return
        geo = widget.geometry()
        label = _label_for(widget)
        extra = ""
        if isinstance(widget, QtWidgets.QLabel):
            plain, needed = _label_text_metrics(widget)
            preview = plain.replace("\n", " ")[:LABEL_PREVIEW_LEN]
            if preview:
                extra = f' text="{preview}"'
            if (
                plain
                and not widget.wordWrap()
                and widget.width() > 0
                and needed > widget.width() + CLIP_TOLERANCE_PX
            ):
                warnings.append(
                    LayoutWarning(
                        label,
                        "clipped-label",
                        f'"{preview}" needs {needed}px, has {widget.width()}px',
                    )
                )
        elif isinstance(widget, QtWidgets.QAbstractButton):
            preview = widget.text().replace("&", "")[:BUTTON_PREVIEW_LEN]
            if preview:
                extra = f' text="{preview}"'
                needed = widget.sizeHint().width()
                if 0 < widget.width() < needed - CLIP_TOLERANCE_PX:
                    warnings.append(
                        LayoutWarning(
                            label,
                            "cramped-button",
                            f'"{preview}" sizeHint={needed}px, width={widget.width()}px',
                        )
                    )
        elif isinstance(widget, QtWidgets.QDockWidget):
            extra = f' title="{widget.windowTitle()}"'

        if (widget.width() == 0 or widget.height() == 0) and not ignore_zero(widget):
            warnings.append(
                LayoutWarning(
                    label,
                    "zero-size",
                    f"visible widget has geometry {geo.width()}x{geo.height()}",
                )
            )

        if (oob := _check_out_of_bounds(widget, root)) is not None:
            warnings.append(oob)

        indent = "  " * depth
        lines.append(
            f"{indent}{label} [{geo.x()},{geo.y()} {geo.width()}x{geo.height()}]{extra}"
        )
        for child in widget.children():
            if isinstance(child, QtWidgets.QWidget):
                visit(child, depth + 1)

    visit(root, 0)
    return lines, warnings


class UIInspector:
    """High-level inspection and screenshot helper bound to a root widget."""

    def __init__(
        self,
        root: QtWidgets.QWidget,
        out_dir: str | os.PathLike[str] | None = None,
        *,
        app: QtCore.QCoreApplication | None = None,
        ignore_zero_size: Callable[[QtWidgets.QWidget], bool] | None = None,
    ) -> None:
        self.root = root
        self.out_dir = pathlib.Path(out_dir) if out_dir is not None else None
        self._app = app
        self.ignore_zero_size = ignore_zero_size
        self.captures: list[CaptureInfo] = []
        self.collected_warnings: list[LayoutWarning] = []

    @property
    def app(self) -> QtCore.QCoreApplication | None:
        return self._app if self._app is not None else QtCore.QCoreApplication.instance()

    def pump(self, ms: int = 40) -> None:
        """Process Qt events for `ms` milliseconds."""
        pump(self.app, ms=ms)

    def wait_until(
        self,
        predicate: Callable[[], object],
        *,
        timeout_ms: int = 5000,
        interval_ms: int = 10,
    ) -> bool:
        """Process Qt events until `predicate()` returns truthy or times out."""
        return wait_until(
            predicate,
            timeout_ms=timeout_ms,
            interval_ms=interval_ms,
            app=self.app,
        )

    def resize(self, width: int, height: int, *, settle_ms: int = 40) -> None:
        """Resize the root widget and let layouts settle."""
        self.root.resize(width, height)
        if settle_ms > 0:
            self.pump(settle_ms)

    def find(self, selector: str) -> QtWidgets.QWidget | None:
        """Resolve a widget selector within `self.root`."""
        return find_widget(self.root, selector)

    def capture(
        self,
        path: str | os.PathLike[str] | None = None,
        *,
        target: str = "window",
        scenario: str = "",
        widget: QtWidgets.QWidget | None = None,
    ) -> CaptureInfo:
        """Capture `target` (or explicit `widget`) to `path` (or inside `out_dir`)."""
        resolved = widget if widget is not None else self.find(target)
        if resolved is None:
            raise LookupError(
                f"Target widget {target!r} not found under {type(self.root).__name__}"
            )
        if path is None:
            if self.out_dir is None:
                raise ValueError(
                    "Either `path` or `UIInspector(..., out_dir=...)` must be provided"
                )
            stem = f"{scenario}_{target}" if scenario else target
            out_path = self.out_dir / f"{stem}.png"
        else:
            out_path = pathlib.Path(path)
            if not out_path.is_absolute() and self.out_dir is not None:
                out_path = self.out_dir / out_path
        info = capture(resolved, out_path, scenario=scenario, target=target)
        self.captures.append(info)
        return info

    def capture_targets(
        self,
        targets: Iterable[str],
        *,
        scenario: str = "",
        out_dir: str | os.PathLike[str] | None = None,
        strict: bool = False,
    ) -> list[CaptureInfo]:
        """Capture multiple named targets, returning their `CaptureInfo` records."""
        base = pathlib.Path(out_dir) if out_dir is not None else self.out_dir
        if base is None:
            raise ValueError(
                "Either `out_dir` or `UIInspector(..., out_dir=...)` must be provided"
            )
        unique_targets = list(dict.fromkeys(targets))
        single = len(unique_targets) == 1
        results: list[CaptureInfo] = []
        for target in unique_targets:
            widget = self.find(target)
            if widget is None:
                if strict:
                    raise LookupError(
                        f"Target widget {target!r} not found under "
                        f"{type(self.root).__name__}"
                    )
                continue
            if scenario:
                fname = f"{scenario}.png" if single else f"{scenario}_{target}.png"
            else:
                fname = f"{target}.png"
            info = capture(widget, base / fname, scenario=scenario, target=target)
            self.captures.append(info)
            results.append(info)
        return results

    def tree(
        self,
        *,
        target: str | None = None,
        max_depth: int = 8,
    ) -> tuple[list[str], list[LayoutWarning]]:
        """Inspect the widget tree of `root` (or `target`)."""
        widget = self.root if target is None else self.find(target)
        if widget is None:
            raise LookupError(
                f"Target widget {target!r} not found under {type(self.root).__name__}"
            )
        return inspect_tree(
            widget,
            max_depth=max_depth,
            ignore_zero_size=self.ignore_zero_size,
        )

    def warnings(
        self,
        *,
        target: str | None = None,
        max_depth: int = 8,
        record: bool = False,
    ) -> list[LayoutWarning]:
        """Return layout warnings for `root` (or `target`)."""
        _, warns = self.tree(target=target, max_depth=max_depth)
        if record:
            self.collected_warnings.extend(warns)
        return warns

    def write_manifest(
        self,
        path: str | os.PathLike[str] | None = None,
        *,
        extra: Mapping[str, Any] | None = None,
        warnings: Iterable[LayoutWarning] | None = None,
    ) -> pathlib.Path:
        """Write a JSON manifest of captures and layout warnings."""
        if path is None:
            if self.out_dir is None:
                raise ValueError(
                    "Either `path` or `UIInspector(..., out_dir=...)` must be provided"
                )
            out_path = self.out_dir / "manifest.json"
        else:
            out_path = pathlib.Path(path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        warn_list = (
            list(warnings) if warnings is not None else list(self.collected_warnings)
        )
        payload: dict[str, Any] = {
            "size": f"{self.root.width()}x{self.root.height()}",
            "captures": [asdict(c) for c in self.captures],
            "warnings": [asdict(w) for w in warn_list],
        }
        if extra:
            payload.update(extra)
        out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return out_path
