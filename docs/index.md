---
hide:
  - navigation
---
# prettyqt: Pythonic layer on top of PyQt6 / PySide6
[![PyPI Latest Release](https://img.shields.io/pypi/v/prettyqt.svg)](https://pypi.org/project/prettyqt/)
[![Package Status](https://img.shields.io/pypi/status/prettyqt.svg)](https://pypi.org/project/prettyqt/)
[![CodeCov](https://codecov.io/gh/phil65/PrettyQt/branch/master/graph/badge.svg)](https://codecov.io/gh/phil65/PrettyQt)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyUp](https://pyup.io/repos/github/phil65/PrettyQt/shield.svg)](https://pyup.io/repos/github/phil65/PrettyQt/)

## What is it?

**PrettyQt** is a Python package that provides a pythonic layer on top of the GUI frameworks PyQt6 / PySide6.

## Main Features
  - Subclasses for a large part of the Qt classes, enriched with helper and __dunder__ methods to give a feel of a native GUI library.
  - more than 80 pre-defined widgets and layouts for common use cases
  - more than 30 ItemModels for different data types
  - more than 25 general-purpose [proxy models](proxies.md)
  - 10 ItemDelegates for different purposes
  - 20 different [validators](validators.md)
  - much, much more.

PrettyQt basically is a wrapper for the whole Qt API (either on top of PySide6 or PyQt6).
Perhaps it can be seen as a small Python equivalent of the KDE framework.

The library contains a tree of mixins, with one mixin for each Qt class.
These mixins also inherit from each other and are applied to the Qt classes.
That way each class gets all helper methods from all sub-mixins.

Example: The class "TreeView" inherits from original Qt Class "QTreeView" and gets helper methods
from "TreeViewMxin", "AbstractItemViewMixin", "AbstractScrollAreaMixin",
"FrameMixin", "WidgetMixin" and "ObjectMixin".

To illustrate this, we will use some of our included models:

```py
    from prettyqt import custom_models, widgets

    app = widgets.app()
    widget = widgets.TreeView()
    model = custom_models.SubClassTreeModel(core.AbstractItemModelMixin)
    widget.set_model(model)
    widget.show()
```

<figure markdown>
  ![Image title](images/abstractitemmodelmixin_subclasses.png)
  <figcaption>AbstractitemModelMixin subclasses</figcaption>
</figure>

You can see a comparison here between Our mixin tree and the original Qt Tree.
As you can notice, every Qt class with Subclasses has a corresponding Mixin.

To show what this leads to, we will look at another example:

```py
    from prettyqt import custom_models, widgets

    app = widgets.app()
    widget = widgets.TreeView()
    model = custom_models.ParentClassTreeModel(widgets.TreeWidget)
    widget.set_model(model)
    widget.show()
```

<figure markdown>
  ![Image title](images/treewidget_parentclasses.png)
  <figcaption>TreeWidget parent classes</figcaption>
</figure>

when passing `show_mro=True` to ParentclassTreeModel, we can also take a loot at the method resolution order:

<figure markdown>
  ![Image title](images/treewidget_mro.png)
  <figcaption>TreeWidget MRO</figcaption>
</figure>

Main objective is to make Qt feel "pythonic". Qt is originally a C++ Framework,
and using it can be quite cumbersome for Python developers. (very restrictive when it comes to types,
very OOP-centric, lot of enum use, snakeCase naming etc.) PrettyQt aims to improve this by:

- adding more powerful methods to the classes, which accept more types and have more options (in form of keyword arguments)
- doing conversions for method parameters to lessen the strictness for types. (Example: points, sizes and rectangles can also be passed to Qt methods as tuples.)
- raising Exceptions or returning None instead of returning -1 or invalid objects.
- all enum getters/setters also work with strings. Everything typed with Literals for an excellent IDE experience. (Example: )
- adding a lot of __dunder__ methods to the classes to make them behave like good python citizens.


The minimum supported python version is 3.10. Since large parts of the library are dealing with type conversions, the match-case statement is essential, therefore makin it impossible to use older Python versions.
The minimum supported Qt version is 6.5, since it is the first Qt Version which is up-to-par featurewise with Qt5.

The aim is to support the last two released Python versions as well as keeping support for the last Qt LTS release.

Apart from the 3D related modules (Qt3D, QtDataVizualization), QtXml and QtSql,
almost every class from Qt is covered.

## Covered Qt modules

| Qt Module           | PrettyQt module            |
|---------------------|----------------------------|
| QtBluetooth         | prettyqt.bluetooth         |
| QtCharts            | prettyqt.charts            |
| QtCore              | prettyqt.core              |
| QtDesigner          | prettyqt.designer          |
| QtGui               | prettyqt.gui               |
| QtLocation          | prettyqt.location          |
| QtMultimedia        | prettyqt.multimedia        |
| QtMultimediaWidgets | prettyqt.multimediawidgets |
| QtNetwork           | prettyqt.network           |
| QtOpenGLWidgets     | prettyqt.openglwidgets     |
| QtPdf               | prettyqt.pdf               |
| QtPdfWidgets        | prettyqt.pdfwidgets        |
| QtPositioning       | prettyqt.positioning       |
| QtPrintSupport      | prettyqt.printsupport      |
| QtQml               | prettyqt.qml               |
| QtHelp              | prettyqt.qthelp            |
| QtQuick             | prettyqt.quick             |
| QtQuickWidgets      | prettyqt.quickwidgets      |
| QScintilla          | prettyqt.scintilla         |
| QtScXml             | prettyqt.scxml             |
| QtSpatialAudio      | prettyqt.spatialaudio      |
| QtStateMachine      | prettyqt.statemachine      |
| QtSvg               | prettyqt.svg               |
| QtSvgWidgets        | prettyqt.svgwidgets        |
| QtTest              | prettyqt.test              |
| QtTextToSpeech      | prettyqt.texttospeech      |
| QtWebChannel        | prettyqt.webchannel        |
| QtWebEngineCore     | prettyqt.webenginecore     |
| QtWebEngineWidgets  | prettyqt.webenginewidgets  |
| QtWidgets           | prettyqt.widgets           |


All subclassed Qt classes in mentioned modules are called exactly like the
Qt-Counterpart, except that the leading Q is missing.

### Examples:

- QtWidgets.QWidget -> widgets.Widget
- QtCore.QObject -> core.Object

Apart from the mentioned mixin tree and the corresponding classes, this library also
contains a lot of custom widgets, delegates, eventfilters, validators,
syntaxhighlighters, layouts, models, proxy models and much more.

Converting to PrettyQt should be very straightforward since the original behaviour of the
Qt classes didnt change for the largest parts and all methods from base Qt modules
are still available. (There might be a few constructors with slightly different behaviour though.)

Interested? Take a look at the documentation! (even though it totally sucks in its current state.)

## Where to get it
The source code is currently hosted on GitHub at:
https://github.com/phil65/PrettyQt

The latest released version are available at the [Python
package index](https://pypi.org/project/prettyqt).

```sh
# or PyPI
pip install prettyqt
```

## Required dependencies
- [bidict](https://pypi.org/project/bidict)
- [pygments](https://pypi.org/project/pygments)
- [qstylizer](https://pypi.org/project/qstylizer)
- [typing_extensions](https://pypi.org/project/typing_extensions)

# And one of...
- [pyside6](https://pypi.org/project/pyside6)
- [pyqt6](https://pypi.org/project/pyqt6)

Note: Only Qt 6.5+ is supported.

## Optional dependencies
- [orjson](https://pypi.org/project/orjson)
- [numpy](https://pypi.org/project/numpy)
- [ipython](https://pypi.org/project/ipython)
- [qtconsole](https://pypi.org/project/qtconsole)
- [pillow](https://pypi.org/project/pillow)
- [fsspec](https://pypi.org/project/fsspec)
- [docutils](https://pypi.org/project/docutils)


## Installation from sources

This project uses poetry for dependency management and packaging. Install this first.
In the `prettyqt` directory (same one where you found this file after
cloning the git repo), execute:

```sh
poetry install
```

## License
[MIT](LICENSE)

## Documentation
The official documentation is hosted on Github Pages: https://phil65.github.io/PrettyQt/

## Contributing to prettyqt [![Open Source Helpers](https://www.codetriage.com/phil65/prettyqt/badges/users.svg)](https://www.codetriage.com/phil65/prettyqt)

All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.

Or maybe through using PrettyQt you have an idea of your own or are looking for something in the documentation and thinking ‘this can be improved’...you can do something about it!
