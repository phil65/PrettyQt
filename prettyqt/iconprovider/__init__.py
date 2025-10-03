from __future__ import annotations

from dataclasses import dataclass
import json
import os

from typing import Literal, overload, TYPE_CHECKING

# Third party imports
from prettyqt import gui, paths
from prettyqt.iconprovider.iconic_font import FontError, IconicFont, set_global_defaults
from prettyqt.qt import QtGui

if TYPE_CHECKING:
    import pathlib
    from prettyqt.utils import datatypes


key_type = tuple[str | None, str | None, bool]
icon_cache: dict[key_type, QtGui.QIcon] = {}
# Linux packagers, please set this to True if you want to make qtawesome
# use system fonts
SYSTEM_FONTS = False
PREFIXES = ("mdi.", "mdi6.", "fa5.", "fa5s.", "ei.", "ph.")


def hook(obj: dict) -> dict:
    result = {}
    for key, val in obj.items():
        try:
            result[key] = chr(int(val, 16))
        except ValueError as e:
            msg = f"Failed to load character {key}:{val}"
            raise FontError(msg) from e
    return result


@dataclass
class IconFont:
    """Class describing an Icon font."""

    prefix: str
    font_path: str
    charmap_path: str
    md5: str
    stylename: str | None = None
    path: pathlib.Path = paths.ICON_FONT_PATH

    def __post_init__(self):
        hash_val = None if SYSTEM_FONTS else self.md5
        id_ = gui.FontDatabase.add_font(self.path / self.font_path, ttf_hash=hash_val)
        loaded_font_families = gui.FontDatabase.applicationFontFamilies(id_)
        self.font_id = id_
        self.font_name = loaded_font_families[0]
        with (self.path / self.charmap_path).open("r") as codes:
            self.charmap = json.load(codes, object_hook=hook)

    def __dir__(self):
        icons = [i.replace("-", "_") for i in self.charmap]
        return list(super().__dir__()) + icons

    def __getattr__(self, name: str):
        return f"{self.prefix}.{name.replace('_', '-')}"

    def is_valid(self) -> bool:
        return len(gui.FontDatabase.applicationFontFamilies(self.font_id)) > 0

    def get_font(self, size: float) -> gui.Font:
        font = gui.Font(self.font_name)
        font.setPixelSize(round(size))
        if self.stylename:  # solid style
            font.setStyleName(self.stylename)
        return font


_resource: dict[str, IconicFont | None] = {"iconic": None}


def _instance() -> IconicFont:
    """Return the singleton instance of IconicFont.

    Functions ``icon``, ``load_font``, ``charmap``, ``font`` and
    ``set_defaults`` all rebind to methods of the singleton instance of IconicFont.
    """
    if _resource["iconic"] is not None and _resource["iconic"].has_valid_font_ids():
        return _resource["iconic"]
    font_awesome_5 = IconFont(
        prefix="fa5",
        font_path="fontawesome5-regular-webfont.ttf",
        charmap_path="fontawesome5-regular-webfont-charmap.json",
        md5="dc47e4089f5bcb25f241bdeb2de0fb58",
    )

    font_awesome_5_solid = IconFont(
        prefix="fa5s",
        font_path="fontawesome5-solid-webfont.ttf",
        charmap_path="fontawesome5-solid-webfont-charmap.json",
        md5="5de19800fc9ae73438c2e5c61d041b48",
        stylename="Solid",
    )

    font_awesome_5_brands = IconFont(
        prefix="fa5b",
        font_path="fontawesome5-brands-webfont.ttf",
        charmap_path="fontawesome5-brands-webfont-charmap.json",
        md5="513aa607d398efaccc559916c3431403",
    )

    elusive_icons = IconFont(
        prefix="ei",
        font_path="elusiveicons-webfont.ttf",
        charmap_path="elusiveicons-webfont-charmap.json",
        md5="207966b04c032d5b873fd595a211582e",
    )

    material_design_5_icons = IconFont(
        prefix="mdi",
        font_path="materialdesignicons5-webfont.ttf",
        charmap_path="materialdesignicons5-webfont-charmap.json",
        md5="b7d40e7ef80c1d4af6d94902af66e524",
    )

    material_design_6_icons = IconFont(
        prefix="mdi6",
        font_path="materialdesignicons6-webfont.ttf",
        charmap_path="materialdesignicons6-webfont-charmap.json",
        md5="9a2f455e7cbce011368aee95d292613b",
    )

    phosphor_icons = IconFont(
        prefix="ph",
        font_path="phosphor.ttf",
        charmap_path="phosphor-charmap.json",
        md5="5b8dc57388b2d86243566b996cc3a789",
    )

    remix_icons = IconFont(
        prefix="ri",
        font_path="remixicon.ttf",
        charmap_path="remixicon-charmap.json",
        md5="888e61f04316f10bddfff7bee10c6dd0",
    )

    codicon_icons = IconFont(
        prefix="msc",
        font_path="codicon.ttf",
        charmap_path="codicon-charmap.json",
        md5="d8565ee605ac4d2fa71fe018863337ca",
    )
    iconic = IconicFont(
        font_awesome_5,
        font_awesome_5_brands,
        font_awesome_5_solid,
        elusive_icons,
        material_design_5_icons,
        material_design_6_icons,
        phosphor_icons,
        remix_icons,
        codicon_icons,
    )
    _resource["iconic"] = iconic
    return iconic


def reset_cache():
    if _resource["iconic"] is not None:
        _resource["iconic"].icon_cache.clear()


def _icon(*names, **kwargs) -> QtGui.QIcon:
    """Return a QIcon object corresponding to the provided icon name(s).

    This function is the main interface of qtawesome.

    It can be used to create a QIcon instance from a single glyph
    or from a list of glyphs that are displayed on the top of each other.
    Such icon stacks are generally used to combine multiple glyphs to make
    more complex icons.

    Glyph names are specified by strings, of the form ``prefix.name``.
    The ``prefix`` corresponds to the font to be used and ``name`` is the
    name of the icon.

     - The prefix corresponding to Font-Awesome 4.x is 'fa'
     - The prefix corresponding to Font-Awesome 5.x (regular) is 'fa5'
     - The prefix corresponding to Font-Awesome 5.x (solid) is 'fa5s'
     - The prefix corresponding to Font-Awesome 5.x (brands) is 'fa5b'
     - The prefix corresponding to Elusive-Icons is 'ei'
     - The prefix corresponding to Material-Design-Icons is 'mdi'

    When requesting a single glyph, options (such as color or positional offsets)
    can be passed as keyword arguments::

        import qtawesome as qta

        music_icon = qta.icon(
            'fa5s.music',
            color='blue',
            color_active='orange')

    When requesting multiple glyphs, the `options` keyword argument contains
    the list of option dictionaries to be used for each glyph::

        camera_ban = qta.icon('fa5s.camera', 'fa5s.ban', options=[{
                'scale_factor': 0.5,
                'active': 'fa5s.balance-scale'
            }, {
                'color': 'red',
                'opacity': 0.7
            }])

    Qt's ``QIcon`` object has four modes

        - ``Normal``: The user is not interacting with the icon, but the
          functionality represented by the icon is available.
        - ``Disabled``: The functionality corresponding to the icon is not
          available.
        - ``Active``: The functionality corresponding to the icon is available.
          The user is interacting with the icon, for example, moving the mouse
          over it or clicking it.
        - ``Selected``: The item represented by the icon is selected.

    The glyph for the Normal mode is the one specified with the main positional
    argument.

     - ``color``: icon color in the ``Normal`` mode.

    The following four options will apply to the icon regardless of the mode.

     - ``offset``: tuple (x, y) corresponding to the horizontal and vertical
       offsets for the glyph, specified as a proportion of the icon size.
     - ``animation``: animation object for the icon.
     - ``scale_factor``: multiplicative scale factor to be used for the glyph.

    The following options apply to the different modes of the icon

     - ``active``: name of the glyph to be used when the icon is ``Active``.
     - ``color_active``: the corresponding icon color.

     - ``disabled``: name of the glyph to be used when the icon is ``Disabled``.
     - ``color_disabled``: the corresponding icon color.

     - ``selected``: name of the glyph to be used when the icon is ``Selected``.
     - ``color_selected``: the corresponding icon color.

    Default values for these options can be specified via the function
    ``set_defaults``. If unspecified, the default defaults are::

        {
            'opacity': 1.0,
            'scale_factor': 1.0
            'color': QColor(50, 50, 50),
            'color_disabled': QColor(150, 150, 150),
        }

    If no default value is provided for ``active``, ``disabled`` or ``selected``
    the glyph specified for the ``Normal`` mode will be used.

    """
    return _instance().icon(*names, **kwargs)


def for_color(color: str | QtGui.QColor | QtGui.QBrush) -> gui.Icon:
    match color:
        case str():
            color = gui.Color(color)
        case gui.QBrush():
            color = color.color()
        case gui.QColor():
            pass
        case _:
            raise TypeError(color)
    if color.isValid():
        bitmap = gui.Pixmap(16, 16)
        bitmap.fill(color)
        return gui.Icon(bitmap)
    return gui.Icon(_icon("mdi.card-outline"))


def set_defaults(**kwargs):
    """Set default options for icons.

    The valid keyword arguments are:

    'active', 'animation', 'color', 'color_active', 'color_disabled',
    'color_selected', 'disabled', 'offset', 'scale_factor', 'selected'.

    """
    return set_global_defaults(**kwargs)


@overload
def get_icon(
    icon: datatypes.IconType, color: str | None = None, as_qicon: Literal[False] = False
) -> gui.Icon: ...


@overload
def get_icon(
    icon: datatypes.IconType, color: str | None = None, as_qicon: Literal[True] = True
) -> QtGui.QIcon: ...


def get_icon(
    icon: datatypes.IconType, color: str | None = None, as_qicon: bool = False
) -> QtGui.QIcon:
    """Get icon with given color.

    Qtawesome already caches icons, but since we construct our own subclassed icon,
    we cache, too.
    """
    if isinstance(icon, QtGui.QIcon):
        return icon if as_qicon else gui.Icon(icon)
    if isinstance(icon, os.PathLike):
        icon = os.fspath(icon)
    if (icon, color, as_qicon) in icon_cache:
        return icon_cache[(icon, color, as_qicon)]
    if isinstance(icon, str) and icon.startswith(PREFIXES):
        new = _icon(icon, color=color) if color is not None else _icon(icon)
    else:
        new = QtGui.QIcon(icon)  # type: ignore
    icon = new if as_qicon else gui.Icon(new)
    icon_cache[(icon, color, as_qicon)] = icon
    return icon


if __name__ == "__main__":
    from prettyqt import custom_widgets, widgets

    app = widgets.app()
    icon = _icon("mdi.folder", vflip=True)
    # state = icon.__getstate__()
    # icon_2 = gui.Icon()
    # icon_2.__setstate__(state)
    widget = custom_widgets.IconWidget()
    widget.set_icon(icon)
    widget.set_icon_size(100)
    widget.show()
    app.exec()
