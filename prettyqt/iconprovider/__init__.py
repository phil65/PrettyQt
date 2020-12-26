"""Core module.

based on qtawesome
"""

import pathlib
from typing import Dict, Optional, Tuple, Union

from qtpy import QtGui

# Third party imports
from prettyqt import gui
from prettyqt.iconprovider.iconic_font import IconicFont, set_global_defaults


class FontAwesome4:
    prefix = "fa"
    font_path = "fontawesome4.7-webfont.ttf"
    charmap_path = "fontawesome4.7-webfont-charmap.json"
    md5 = "b06871f281fee6b241d60582ae9369b9"
    stylename = None


class FontAwesome5:
    prefix = "fa5"
    font_path = "fontawesome5-regular-webfont.ttf"
    charmap_path = "fontawesome5-regular-webfont-charmap.json"
    md5 = "808833867034fb67a4a86dd2155e195d"
    stylename = None


class FontAwesome5Solid:
    prefix = "fa5s"
    font_path = "fontawesome5-solid-webfont.ttf"
    charmap_path = "fontawesome5-solid-webfont-charmap.json"
    md5 = "139654bb0acaba6b00ae30d5faf3d02f"
    stylename = "Solid"


class FontAwesome5Brands:
    prefix = "fa5b"
    font_path = "fontawesome5-brands-webfont.ttf"
    charmap_path = "fontawesome5-brands-webfont-charmap.json"
    md5 = "085b1dd8427dbeff10bd55410915a3f6"
    stylename = None


class ElusiveIcons:
    prefix = "ei"
    font_path = "elusiveicons-webfont.ttf"
    charmap_path = "elusiveicons-webfont-charmap.json"
    md5 = "207966b04c032d5b873fd595a211582e"
    stylename = None


class MaterialDesignIcons:
    prefix = "mdi"
    font_path = "materialdesignicons-webfont.ttf"
    charmap_path = "materialdesignicons-webfont-charmap.json"
    md5 = "b0fd91bb29dcb296a9a37f8bda0a2d85"
    stylename = None


# Constants
FONTS = [
    ("fa", "fontawesome4.7-webfont.ttf", "fontawesome4.7-webfont-charmap.json"),
    (
        "fa5",
        "fontawesome5-regular-webfont.ttf",
        "fontawesome5-regular-webfont-charmap.json",
    ),
    (
        "fa5s",
        "fontawesome5-solid-webfont.ttf",
        "fontawesome5-solid-webfont-charmap.json",
    ),
    (
        "fa5b",
        "fontawesome5-brands-webfont.ttf",
        "fontawesome5-brands-webfont-charmap.json",
    ),
    ("ei", "elusiveicons-webfont.ttf", "elusiveicons-webfont-charmap.json"),
    (
        "mdi",
        "materialdesignicons-webfont.ttf",
        "materialdesignicons-webfont-charmap.json",
    ),
]

_resource: Dict[str, Optional[IconicFont]] = {"iconic": None}


def _instance() -> IconicFont:
    """Return the singleton instance of IconicFont.

    Functions ``icon``, ``load_font``, ``charmap``, ``font`` and
    ``set_defaults`` all rebind to methods of the singleton instance of IconicFont.
    """
    if _resource["iconic"] is None or not _resource["iconic"].has_valid_font_ids():
        iconic = IconicFont(*FONTS)
        _resource["iconic"] = iconic
        return iconic
    return _resource["iconic"]


def reset_cache():
    if _resource["iconic"] is not None:
        _resource["iconic"].icon_cache = {}


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


def for_color(color: Union[str, QtGui.QColor]) -> gui.Icon:
    if isinstance(color, str):
        color = gui.Color.from_text(color)
    if color.isValid():
        bitmap = gui.Pixmap(16, 16)
        bitmap.fill(color)
        return gui.Icon(bitmap)
    else:
        return gui.Icon(_icon("mdi.card-outline"))


def load_font(
    prefix: str,
    ttf_filename: str,
    charmap_filename: str,
    directory: Optional[pathlib.Path] = None,
) -> gui.Font:
    """Load a font file and the associated charmap.

    If ``directory`` is None, the files will be looked for in ``./fonts/``.

    Parameters
    ----------
    prefix: str
        Prefix string to be used when accessing a given font set
    ttf_filename: str
        Ttf font filename
    charmap_filename: str
        Character map filename
    directory: str or None, optional
        Directory for font and charmap files

    Example
    -------
    The spyder ide uses qtawesome and uses a custom font for spyder-specific
    icons::

        qta.load_font('spyder', 'spyder.ttf', 'spyder-charmap.json')

    """
    return _instance().load_font(prefix, ttf_filename, charmap_filename, directory)


def charmap(prefixed_name: str) -> Dict[str, str]:
    """Return the character map used for a given font.

    Returns
    -------
    return_value: dict
        The dictionary mapping the icon names to the corresponding unicode character.

    """
    prefix, name = prefixed_name.split(".")
    return _instance().charmap[prefix][name]


def font(prefix: str, size: int):
    """Return the font corresponding to the specified prefix.

    This can be used to render text using the iconic font directly::

        import qtawesome as qta
        from qtpy import QtWidgets

        label = QtWidgets.QLabel(unichr(0xf19c) + ' ' + 'Label')
        label.setFont(qta.font('fa', 16))

    Parameters
    ----------
    prefix: str
        prefix string of the loaded font
    size: int
        size for the font

    """
    return _instance().font(prefix, size)


def set_defaults(**kwargs):
    """Set default options for icons.

    The valid keyword arguments are:

    'active', 'animation', 'color', 'color_active', 'color_disabled',
    'color_selected', 'disabled', 'offset', 'scale_factor', 'selected'.

    """
    return set_global_defaults(**kwargs)


IconType = Union[QtGui.QIcon, str, pathlib.Path, None]

key_type = Tuple[Optional[str], Optional[str], bool]
icon_cache: Dict[key_type, QtGui.QIcon] = {}


def get_icon(
    icon: IconType, color: Optional[str] = None, as_qicon: bool = False
) -> QtGui.QIcon:
    """Get icon with given color.

    Qtawesome already caches icons, but since we construct our own subclassed icon,
    we cache, too.
    """
    if isinstance(icon, QtGui.QIcon):
        return icon if as_qicon else gui.Icon(icon)
    if isinstance(icon, pathlib.Path):
        icon = str(icon)
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
