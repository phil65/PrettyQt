PrettyQt includes its own layer to both support PySide6 and PyQt6.
The logic for choosing one of these frameworks mirrors the one from [QtPy](https://pypi.org/project/QtPy/), which is the most widely used package for supporting multiple Qt bindings. That should ensure that this framework can be used in conjunction with other packages which build on QtPy.

The logic for choosing one the bindings basically works like this:

1. If one of the two bindings was already imported, use that binding.
2. Check the environment variable QT_API and try to import that binding.
3. If that binding is not installed, try the other one.


PrettyQt only supports the most recent versions (LTS 6.5) of these bindings.
Reason for that is that these are the first versions which are basically on par feature-wise with Qt5. For the future, PrettyQt will at least support Qt Verions back to the last LTS version.

For a long time, PyQt was the only really usable binding. Especially PySide2 was buggy to an extent that it was almost unusable for more complex applications. That changed greatly in recent months up to a point where it is today at least on par with PyQt6.

Starting with 6.5.2, my personal recommendation would be to use PySide6, mainly for excellent support and for pushing features which go beyond just generating a 1:1 binding. (\__feature__ imports, opaque containers, PyPy compatibility, ...)
