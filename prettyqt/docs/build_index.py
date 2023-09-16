import mknodes
from prettyqt import core, gui, itemmodels, widgets
from prettyqt.utils import classhelpers


DESCRIPTION = """
PrettyQt basically is a wrapper for the whole Qt API (either on top of PySide6 or
PyQt6 bindings).
Perhaps it can be seen as a small Python equivalent of the KDE framework.

Main objective is to make Qt feel "pythonic". Qt is originally a C++ Framework,
and using it can be quite cumbersome for Python developers. (very restrictive when it
comes to types, very OOP-centric, lot of enum use, snakeCase naming etc.)

PrettyQt aims to improve this by:

* adding more powerful methods to the classes, which accept more types and have more options (in form of keyword arguments)
* doing [type conversions](types.md) for method parameters to lessen the strictness for types.
* raising Exceptions or returning `None` instead of returning `*1` or invalid objects.
* all enum getters/setters also work with strings. Everything typed with Literals for an excellent IDE experience. (Example: )
* adding a lot of `__dunder__` methods to the classes to make them behave like good python citizens.
"""


def build_index(page):
    Proxies = classhelpers.get_subclasses(core.AbstractProxyModelMixin)
    Delegates = classhelpers.get_subclasses(widgets.StyledItemDelegate)
    TreeModels = classhelpers.get_subclasses(itemmodels.TreeModel)
    TableModels = classhelpers.get_subclasses(core.AbstractTableModelMixin)
    all_models = list(TableModels) + list(TreeModels)
    table_tabs = {
        "30+ Item Models": mknodes.MkClassTable(klasses=all_models),
        "25+ Proxy Models": mknodes.MkClassTable(klasses=list(Proxies)),
        "20+ Validators": mknodes.MkClassTable(klasses=gui.Validator.__subclasses__()),
        "10+ Item Delegates": mknodes.MkClassTable(klasses=list(Delegates)),
    }

    shields = mknodes.MkShields(
        shields=["version", "status", "codecov"],
        user="phil65",
        project="prettyqt",
    )
    page += "# PrettyQt: Pythonic layer on top of PyQt6 / PySide6"
    page += shields
    page += mknodes.MkTabbed(tabs=table_tabs, header="Features")
    page += DESCRIPTION
    page += "[Read more](general.md) about the general API design."
    page += mknodes.MkInstallGuide(distribution="prettyqt", header="Where to get it")


if __name__ == "__main__":
    page = mknodes.MkPage()
    build_index(page)
    print(page)
