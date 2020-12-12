# prettyqt: Pythonic layer on top of PyQt5 / PySide2
[![PyPI Latest Release](https://img.shields.io/pypi/v/prettyqt.svg)](https://pypi.org/project/prettyqt/)
[![Package Status](https://img.shields.io/pypi/status/prettyqt.svg)](https://pypi.org/project/prettyqt/)
[![License](https://img.shields.io/pypi/l/prettyqt.svg)](https://github.com/prettyqt-dev/prettyqt/blob/master/LICENSE)
[![Travis Build Status](https://travis-ci.org/prettyqt-dev/prettyqt.svg?branch=master)](https://travis-ci.org/prettyqt-dev/prettyqt)
[![CodeCov](https://codecov.io/gh/phil65/PrettyQt/branch/master/graph/badge.svg)](https://codecov.io/gh/phil65/PrettyQt)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyUp](https://pyup.io/repos/github/phil65/PrettyQt/shield.svg)](https://pyup.io/repos/github/phil65/PrettyQt/)

## What is it?

**PrettyQt** is a Python package that provides a pythonic layer on top of the GUI frameworks PyQt5 / PySide2.

## Main Features
Here are just a few of the things that PrettyQt does well:

  - Large parts of the Qt API are available in a **PEP-8**-compliant way.
  - Several predefined widgets, validators, models, syntax highlighters are included.
  - A regex module based on QRegularExpression with the same API as Pythons core re module.


   [widgets]: https://phil65.github.io/PrettyQt/widgets.html
   [validators]: https://phil65.github.io/PrettyQt/validators.html
   [syntaxhighlighters]: https://phil65.github.io/PrettyQt/syntaxhighlighters.html
   [models]: https://phil65.github.io/PrettyQt/models.html


## Where to get it
The source code is currently hosted on GitHub at:
https://github.com/phil65/PrettyQt

The latest released version are available at the [Python
package index](https://pypi.org/project/prettyqt).

```sh
# or PyPI
pip install prettyqt
```

## Dependencies
- [qtpy](https://pypi.org/project/prettyqt)
- [qtawesome](https://pypi.org/project/qtawesome)
- [bidict](https://pypi.org/project/bidict)
- [orjson](https://pypi.org/project/orjson)
- [regex](https://pypi.org/project/regex)
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
