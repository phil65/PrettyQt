# AGENTS.md

## Overview

PrettyQt is a "pythonic" layer over the whole Qt 6 API, running on either PyQt6 or
PySide6. Each Qt class gets a subclass (Q-prefix dropped) that keeps the original Qt API
and adds snake_case helpers, string-instead-of-enum setters/getters, `__dunder__` methods
and extra kwargs. On top of that it ships its own widgets, item models, proxy models,
delegates, validators and tooling. Not copier-managed; everything here is hand-maintained.

## Architecture

- `prettyqt/qt/` — binding shim (QtPy-style). `prettyqt/qt/__init__.py` picks the binding:
  an already-imported binding wins, then `QT_API` (`pyqt6` default, or `pyside6`), then the
  other one. Each `prettyqt/qt/Qt<Module>/__init__.py` does `from PyQt6.Qt<Module> import *`
  or the PySide6 equivalent and papers over binding differences. All other code imports Qt
  only via `prettyqt.qt` (never `PyQt6` / `PySide6` directly).
- One package per Qt module, lowercase without `Qt` prefix: `core`, `gui`, `widgets`,
  `network`, `charts`, `multimedia`, `quick`, `qml`, `pdf`, `webenginewidgets`, ...
  (`QtHelp` → `qthelp`). Each `__init__.py` star-imports the raw Qt module (so
  `widgets.QWidget` still exists), then imports the wrappers in **dependency order**
  (base classes/mixins first), sets `QT_MODULE = Qt<Module>` and lists `__all__`.
  Packages with `QT_MODULE` are "Qt-based"; the rest are add-ons.
- One wrapper class per file, file name = lowercased class name
  (`prettyqt/widgets/checkbox.py` → `widgets.CheckBox`). Pattern:
  `class CheckBox(widgets.AbstractButtonMixin, widgets.QCheckBox)`. Abstract/base Qt
  classes get a `FooMixin` plus a concrete `Foo(FooMixin, QFoo)` so subclasses can reuse the
  mixin (`WidgetMixin`, `ObjectMixin`, `AbstractItemModelMixin`, ...). Files often end with
  an `if __name__ == "__main__":` demo.
- Core mechanics live in `prettyqt/core/object.py` (`ObjectMixin`): kwargs in the
  constructor are camel-cased and string values mapped to enums via `_get_map()`, which every
  mixin extends via `super()._get_map() | {...}`.
- Enum ↔ string mapping: `prettyqt/constants/__init__.py` (re-exports `Qt.*` enums plus
  `bidict`s like `CHECK_STATE` with matching `...Str` `Literal` types). Module-specific
  bidicts sit next to the class. `prettyqt.utils.bidict.get_enum_value()` accepts str or enum;
  invalid values raise `prettyqt.utils.InvalidParamError`.
- Layering: `core` must not import `gui`, `gui` must not import `widgets`, etc. (mirrors Qt).
  `prettyqt/widgets/__init__.py` imports `validators`, `itemdelegates` and `custom_widgets`
  at the end (registration side effects).
- Add-on packages: `custom_widgets/` (80+ own widgets, `editors/`, `layouts/`,
  `itemviews/`, `regexeditor/`, ...), `itemmodels/` (tree/table models for python objects,
  dataclasses, json, fsspec, ...; `proxies/` holds proxy models), `itemdelegates/`,
  `validators/`, `eventfilters/`, `animations/`, `iconprovider/` (qtawesome-style font icons,
  fonts in `iconprovider/fonts/`), `syntaxhighlighters/`, `debugging/`, `ipython/`, `custom_network/`,
  `utils/` (helpers, `datatypes.py` type conversions, `classhelpers.py`, `proxifier.py`).
- `prettyqt/__init__.py`: `import_all()` imports every subpackage in `__all__`, logging
  (not raising) when a binding lacks a module.
- `prettyqtmarkdown/` + `prettyqt/docs/` (entry point: `prettyqt/docs/gen_pages.py`): mknodes-based docs
  generation (needs the `docs` group / `mknodes`, not a runtime dependency).

## Where to look

| Task | Location |
| --- | --- |
| Wrap a new Qt class | new file in `prettyqt/<module>/`, import it in that package's `__init__.py` after its bases, add to `__all__` |
| Add a custom widget | `prettyqt/custom_widgets/<name>.py` (or a subpackage), export in `prettyqt/custom_widgets/__init__.py` |
| Add an item model / proxy | `prettyqt/itemmodels/`, `prettyqt/itemmodels/proxies/` |
| Binding differences, import fallbacks | `prettyqt/qt/Qt<Module>/__init__.py` |
| Enum ↔ string maps | `prettyqt/constants/__init__.py`, or the class's module |
| Argument type conversion | `prettyqt/utils/datatypes.py` |
| Docs site structure | `prettyqt/docs/gen_pages.py`, `prettyqt/docs/build_root.py`, `prettyqt/docs/build_index.py`, `prettyqt/docs/SUMMARY.md` |
| Hand-written guide pages | `prettyqt/docs/api_guidelines/`, `prettyqt/docs/features/` |
| PyInstaller hook | `prettyqt/__pyinstaller/` |
| Tests | `tests/test_<module>.py` (one file per package), fixtures in `tests/conftest.py` |

## Commands

```bash
uv sync --extra pyside6 --extra addons     # or --extra pyqt6; extras swap the binding
QT_QPA_PLATFORM=offscreen uv run pytest   # headless; CI uses xvfb instead
uv run pytest --doctest-modules           # CI's PySide6 run
QT_API=pyside6 uv run pytest              # force a binding when both are installed
uv run ruff check . && uv run ruff format --check .
uv run mypy prettyqt/                     # duty lint_check; not enforced in CI
uv run mkdocs-mknodes build               # docs (slow: generates a page per class)
uv build
```

`duties.py` wraps these (`duty test`, `duty lint`, `duty lint_check`, `duty version`).
CI: `.github/workflows/build.yml` runs pytest under PyQt6 and PySide6 on
Linux/macOS/Windows plus the docs build; the `deploy` job (tags `v*` only) publishes to
PyPI and gh-pages.

## Conventions

- Python >= 3.12, `from __future__ import annotations`, ruff (line length 90, preview
  format). Typing uses `Literal` string aliases (`...Str`) for enum-accepting APIs.
- Naming: setters `set_foo()`, getters `get_foo()` (to avoid clashing with Qt's `foo()`),
  string values for enums. Never break the inherited Qt signature; only add.
- Keep wrappers thin and binding-agnostic; anything binding-specific goes in `prettyqt/qt/`
  or behind `prettyqt.qt.API` / `PYSIDE6` / `PYQT6` checks.
- Tests are flat functions using pytest-qt's `qtbot` / `qapp` (app class is
  `widgets.Application`, see `tests/conftest.py`). Modules missing from a binding are skipped
  with `pytest.importorskip`.

## Pitfalls

- Downstream projects depend on `prettyqt[pyside6]`: be conservative with public API changes.
- Binding gaps: `scintilla` (QScintilla) is PyQt6-only; `scxml` is PySide6-only;
  `designer` exports different plugin classes per binding; PyQt6's QtPdf ships in the separate `PyQt6-Pdf` wheel.
- Many add-on modules import optional libs (`pydantic`, `attrs`, `git`, `pandas`,
  `IPython`/`qtconsole`, `fsspec`, `PIL`, `mknodes`) lazily or only when that module is
  imported; they are not runtime dependencies. Eager imports must be declared in
  `[project] dependencies`.
- Import order in package `__init__.py` files matters (bases before subclasses).
- Tests need a display: set `QT_QPA_PLATFORM=offscreen` (or run under xvfb).
- `prettyqt/qt/` and `docs/` are excluded from ruff.
