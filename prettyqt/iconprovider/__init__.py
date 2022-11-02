"""Core module.

based on qtawesome
"""
from __future__ import annotations

import json
import os
import pathlib
from typing import Optional

from prettyqt.qt import QtGui

# Third party imports
from prettyqt import gui, paths
from prettyqt.iconprovider.iconic_font import FontError, IconicFont, set_global_defaults
from prettyqt.utils import types


key_type = tuple[Optional[str], Optional[str], bool]
icon_cache: dict[key_type, QtGui.QIcon] = {}
# Linux packagers, please set this to True if you want to make qtawesome
# use system fonts
SYSTEM_FONTS = False


def hook(obj: dict) -> dict:
    result = {}
    for key in obj:
        try:
            result[key] = chr(int(obj[key], 16))
        except ValueError:
            raise FontError(f"Failed to load character {key}:{obj[key]}")
    return result


class IconFont:
    path: pathlib.Path = paths.ICON_FONT_PATH
    prefix: str
    font_path: str
    charmap_path: str
    md5: str
    stylename: str | None = None

    def __init__(self):
        hash_val = None if SYSTEM_FONTS else self.md5
        id_ = gui.FontDatabase.add_font(self.path / self.font_path, ttf_hash=hash_val)
        loaded_font_families = gui.FontDatabase.applicationFontFamilies(id_)
        self.font_id = id_
        self.font_name = loaded_font_families[0]
        with (self.path / self.charmap_path).open("r") as codes:
            self.charmap = json.load(codes, object_hook=hook)

    def __dir__(self):
        icons = [i.replace("-", "_") for i in self.charmap.keys()]
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


class FontAwesome5(IconFont):
    prefix = "fa5"
    font_path = "fontawesome5-regular-webfont.ttf"
    charmap_path = "fontawesome5-regular-webfont-charmap.json"
    md5 = "808833867034fb67a4a86dd2155e195d"


class FontAwesome5Solid(IconFont):
    prefix = "fa5s"
    font_path = "fontawesome5-solid-webfont.ttf"
    charmap_path = "fontawesome5-solid-webfont-charmap.json"
    md5 = "139654bb0acaba6b00ae30d5faf3d02f"
    stylename = "Solid"


class FontAwesome5Brands(IconFont):
    prefix = "fa5b"
    font_path = "fontawesome5-brands-webfont.ttf"
    charmap_path = "fontawesome5-brands-webfont-charmap.json"
    md5 = "085b1dd8427dbeff10bd55410915a3f6"


class ElusiveIcons(IconFont):
    prefix = "ei"
    font_path = "elusiveicons-webfont.ttf"
    charmap_path = "elusiveicons-webfont-charmap.json"
    md5 = "207966b04c032d5b873fd595a211582e"


class MaterialDesign5Icons(IconFont):
    prefix = "mdi"
    font_path = "materialdesignicons5-webfont.ttf"
    charmap_path = "materialdesignicons5-webfont-charmap.json"
    md5 = "b7d40e7ef80c1d4af6d94902af66e524"


class MaterialDesign6Icons(IconFont):
    prefix = "mdi6"
    font_path = "materialdesignicons6-webfont.ttf"
    charmap_path = "materialdesignicons6-webfont-charmap.json"
    md5 = "9a2f455e7cbce011368aee95d292613b"


class PhosphorIcons(IconFont):
    prefix = "ph"
    font_path = "phosphor.ttf"
    charmap_path = "phosphor-charmap.json"
    md5 = "5b8dc57388b2d86243566b996cc3a789"


class RemixIcons(IconFont):
    prefix = "ri"
    font_path = "remixicon.ttf"
    charmap_path = "remixicon-charmap.json"
    md5 = "888e61f04316f10bddfff7bee10c6dd0"


class CodiconIcons(IconFont):
    prefix = "msc"
    font_path = "codicon.ttf"
    charmap_path = "codicon-charmap.json"
    md5 = "ca2f9e22cee3a59156b3eded74d87784"


_resource: dict[str, IconicFont | None] = {"iconic": None}


def _instance() -> IconicFont:
    """Return the singleton instance of IconicFont.

    Functions ``icon``, ``load_font``, ``charmap``, ``font`` and
    ``set_defaults`` all rebind to methods of the singleton instance of IconicFont.
    """
    if _resource["iconic"] is None or not _resource["iconic"].has_valid_font_ids():
        iconic = IconicFont(
            FontAwesome5(),
            FontAwesome5Brands(),
            FontAwesome5Solid(),
            ElusiveIcons(),
            MaterialDesign5Icons(),
            MaterialDesign6Icons(),
            PhosphorIcons(),
            RemixIcons(),
            CodiconIcons(),
        )
        _resource["iconic"] = iconic
        return iconic
    return _resource["iconic"]


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


def for_color(color: str | QtGui.QColor) -> gui.Icon:
    if isinstance(color, str):
        color = gui.Color.from_text(color)
    if color.isValid():
        bitmap = gui.Pixmap(16, 16)
        bitmap.fill(color)
        return gui.Icon(bitmap)
    else:
        return gui.Icon(_icon("mdi.card-outline"))


def set_defaults(**kwargs):
    """Set default options for icons.

    The valid keyword arguments are:

    'active', 'animation', 'color', 'color_active', 'color_disabled',
    'color_selected', 'disabled', 'offset', 'scale_factor', 'selected'.

    """
    return set_global_defaults(**kwargs)


def get_icon(
    icon: types.IconType, color: str | None = None, as_qicon: bool = False
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
    if isinstance(icon, str) and icon.startswith("mdi."):
        if color is not None:
            new = _icon(icon, color=color)
        else:
            new = _icon(icon)
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
    app.main_loop()
