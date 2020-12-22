"""A lightweight module handling iconic fonts.

It is designed to provide a simple way for creating QtGui.QIcons from glyphs.

From a user's viewpoint, the main entry point is the ``IconicFont`` class which
contains methods for loading new iconic fonts with their character map and
methods returning instances of ``QIcon``.

"""

# Standard library imports
import hashlib
import json
import pathlib
from typing import Any, Dict, Iterable, List, Optional, Tuple
import warnings

from qtpy import QtCore, QtGui

from prettyqt import constants, core, gui


# Third party imports


# Linux packagers, please set this to True if you want to make qtawesome
# use system fonts
SYSTEM_FONTS = False

# MD5 Hashes for font files bundled with qtawesome:
MD5_HASHES = {
    "fontawesome4.7-webfont.ttf": "b06871f281fee6b241d60582ae9369b9",
    "fontawesome5-regular-webfont.ttf": "6a745dc6a0871f350b0219f5a2678838",
    "fontawesome5-solid-webfont.ttf": "acf50f59802f20d8b45220eaae532a1c",
    "fontawesome5-brands-webfont.ttf": "ed2b8bf117160466ba6220a8f1da54a4",
    "elusiveicons-webfont.ttf": "207966b04c032d5b873fd595a211582e",
    "materialdesignicons-webfont.ttf": "b0fd91bb29dcb296a9a37f8bda0a2d85",
}

_default_options = {
    "color": gui.Color(50, 50, 50),
    "color_disabled": gui.Color(150, 150, 150),
    "opacity": 1.0,
    "scale_factor": 1.0,
}

ZERO_COORD = core.Point(0, 0)


def set_global_defaults(**kwargs):
    """Set global defaults for the options passed to the icon painter."""
    valid_options = [
        "active",
        "selected",
        "disabled",
        "on",
        "off",
        "on_active",
        "on_selected",
        "on_disabled",
        "off_active",
        "off_selected",
        "off_disabled",
        "color",
        "color_on",
        "color_off",
        "color_active",
        "color_selected",
        "color_disabled",
        "color_on_selected",
        "color_on_active",
        "color_on_disabled",
        "color_off_selected",
        "color_off_active",
        "color_off_disabled",
        "animation",
        "offset",
        "scale_factor",
        "rotated",
        "hflip",
        "vflip",
    ]
    for kw in kwargs:
        if kw not in valid_options:
            raise KeyError(f"Invalid option '{kw}'")
        _default_options[kw] = kwargs[kw]


class CharIconPainter:
    """Char icon painter."""

    def paint(self, iconic, painter, rect, mode, state, options: List[Dict[str, Any]]):
        for opt in options:
            self._paint_icon(iconic, painter, rect, mode, state, opt)

    def _paint_icon(self, iconic, painter, rect, mode, state, options: Dict[str, Any]):
        color = options["color"]
        char = options["char"]

        color_options = {
            QtGui.QIcon.On: {
                QtGui.QIcon.Normal: (options["color_on"], options["on"]),
                QtGui.QIcon.Disabled: (
                    options["color_on_disabled"],
                    options["on_disabled"],
                ),
                QtGui.QIcon.Active: (options["color_on_active"], options["on_active"]),
                QtGui.QIcon.Selected: (
                    options["color_on_selected"],
                    options["on_selected"],
                ),
            },
            QtGui.QIcon.Off: {
                QtGui.QIcon.Normal: (options["color_off"], options["off"]),
                QtGui.QIcon.Disabled: (
                    options["color_off_disabled"],
                    options["off_disabled"],
                ),
                QtGui.QIcon.Active: (options["color_off_active"], options["off_active"]),
                QtGui.QIcon.Selected: (
                    options["color_off_selected"],
                    options["off_selected"],
                ),
            },
        }

        color, char = color_options[state][mode]

        painter.save()
        painter.setPen(gui.Color(color))

        # A 16 pixel-high icon yields a font size of 14, which is pixel perfect
        # for font-awesome. 16 * 0.875 = 14
        # The reason why the glyph size is smaller than the icon size is to
        # account for font bearing.

        draw_size = round(0.875 * rect.height() * options["scale_factor"])
        prefix = options["prefix"]

        # Animation setup hook
        animation = options.get("animation")
        if animation is not None:
            animation.setup(self, painter, rect)

        painter.setFont(iconic.font(prefix, draw_size))
        if "offset" in options:
            rect = core.Rect(rect)
            rect.translate(
                round(options["offset"][0] * rect.width()),
                round(options["offset"][1] * rect.height()),
            )

        if "vflip" in options and options["vflip"] is True:
            x_center = rect.width() * 0.5
            y_center = rect.height() * 0.5
            painter.translate(x_center, y_center)
            transfrom = gui.Transform()
            transfrom.scale(1, -1)
            painter.setTransform(transfrom, True)
            painter.translate(-x_center, -y_center)

        if "hflip" in options and options["hflip"] is True:
            x_center = rect.width() * 0.5
            y_center = rect.height() * 0.5
            painter.translate(x_center, y_center)
            transfrom = gui.Transform()
            transfrom.scale(-1, 1)
            painter.setTransform(transfrom, True)
            painter.translate(-x_center, -y_center)

        if "rotated" in options:
            x_center = rect.width() * 0.5
            y_center = rect.height() * 0.5
            painter.translate(x_center, y_center)
            painter.rotate(options["rotated"])
            painter.translate(-x_center, -y_center)

        painter.setOpacity(options.get("opacity", 1.0))

        painter.drawText(rect, int(constants.ALIGN_CENTER), char)
        painter.restore()


class FontError(Exception):
    """Exception for font errors."""


class CharIconEngine(gui.IconEngine):
    """Specialization of QtGui.QIconEngine used to draw font-based icons."""

    def __init__(self, iconic: QtCore.QObject, painter, options):
        super().__init__()
        self.iconic = iconic
        self.painter = painter
        self.options = options

    def paint(self, painter: QtGui.QPainter, rect: QtCore.QRect, mode, state):
        self.painter.paint(self.iconic, painter, rect, mode, state, self.options)

    def pixmap(self, size, mode, state) -> QtGui.QPixmap:
        pm = QtGui.QPixmap(size)
        pm.fill(QtCore.Qt.transparent)
        self.paint(gui.Painter(pm), core.Rect(ZERO_COORD, size), mode, state)
        return pm


class IconicFont(core.Object):
    """Main class for managing iconic fonts."""

    def __init__(self, *args):
        """Initialize IconicFont.

        Parameters
        ----------
        ``*args``: tuples
            Each positional argument is a tuple of 3 or 4 values:
            - The prefix string to be used when accessing a given font set,
            - The ttf font filename,
            - The json charmap filename,
            - Optionally, the directory containing these files. When not
              provided, the files will be looked for in ``./fonts/``.
        """
        super().__init__()
        self.painter = CharIconPainter()
        self.painters: Dict[str, CharIconPainter] = {}
        self.fontname = {}
        self.fontids = {}
        self.charmap = {}
        self.icon_cache = {}
        for fargs in args:
            self.load_font(*fargs)

    def load_font(
        self,
        prefix: str,
        ttf_filename: str,
        charmap_filename: str,
        directory: Optional[pathlib.Path] = None,
    ):
        """Load a font file and the associated charmap.

        If ``directory`` is None, the files will be looked for in ``./fonts/``.

        Parameters
        ----------
        prefix: str
            Prefix string to be used when accessing a given font set
        ttf_filename: str
            Ttf font filename
        charmap_filename: str
            Charmap filename
        directory: str or None, optional
            Directory for font and charmap files
        """
        if directory is None:
            directory = pathlib.Path(__file__).parent / "fonts"

        # Load font
        if gui.app() is None:
            return
        id_ = gui.FontDatabase.add_font(directory / ttf_filename)
        loaded_font_families = gui.FontDatabase.applicationFontFamilies(id_)

        if not loaded_font_families:
            raise FontError(
                f"Font at '{directory / ttf_filename}' appears to be empty. "
                "If you are on Windows 10, please read "
                "https://support.microsoft.com/"
                "en-us/kb/3053676 "
                "to know how to prevent Windows from blocking "
                "the fonts that come with QtAwesome."
            )
        self.fontids[prefix] = id_
        self.fontname[prefix] = loaded_font_families[0]

        def hook(obj: dict) -> dict:
            result = {}
            for key in obj:
                try:
                    result[key] = chr(int(obj[key], 16))
                except ValueError:
                    if int(obj[key], 16) > 0xFFFF:
                        # ignoring unsupported code in Python 2.7 32bit Windows
                        # ValueError: chr() arg not in range(0x10000)
                        pass
                    else:
                        raise FontError("Failed to load character " f"{key}:{obj[key]}")
            return result

        with (directory / charmap_filename).open("r") as codes:
            self.charmap[prefix] = json.load(codes, object_hook=hook)

        # Verify that vendorized fonts are not corrupt
        if SYSTEM_FONTS:
            return
        ttf_hash = MD5_HASHES.get(ttf_filename, None)
        if ttf_hash is None:
            return
        hasher = hashlib.md5()
        content = (directory / ttf_filename).read_bytes()
        hasher.update(content)
        ttf_calculated_hash_code = hasher.hexdigest()
        if ttf_calculated_hash_code != ttf_hash:
            raise FontError(f"Font is corrupt at: '{directory / ttf_filename}'")

    def icon(self, *names, **kwargs) -> QtGui.QIcon:
        """Return a QtGui.QIcon object corresponding to the provided icon name."""
        cache_key = f"{names}{kwargs}"
        if cache_key in self.icon_cache:
            return self.icon_cache[cache_key]
        options_list = kwargs.pop("options", [{}] * len(names))
        if len(options_list) != len(names):
            raise Exception(f'"options" must be a list of size {len(names)}')
        if gui.app() is None:
            warnings.warn("You need to have a running QGuiApplication.")
            return QtGui.QIcon()
        parsed_options = [
            self._parse_options(opt, kwargs, name)
            for opt, name in zip(options_list, names)
        ]
        icon = self._icon_by_painter(self.painter, parsed_options)
        self.icon_cache[cache_key] = icon
        return icon

    def _parse_options(
        self, specific_options: dict, general_options: dict, name: str
    ) -> Dict[str, Any]:
        options = dict(_default_options, **general_options)
        options.update(specific_options)

        # Handle icons for modes (Active, Disabled, Selected, Normal)
        # and states (On, Off)
        icon_kw = [
            "char",
            "on",
            "off",
            "active",
            "selected",
            "disabled",
            "on_active",
            "on_selected",
            "on_disabled",
            "off_active",
            "off_selected",
            "off_disabled",
        ]
        char = options.get("char", name)
        on = options.get("on", char)
        off = options.get("off", char)
        active = options.get("active", on)
        selected = options.get("selected", active)
        disabled = options.get("disabled", char)
        on_active = options.get("on_active", active)
        on_selected = options.get("on_selected", selected)
        on_disabled = options.get("on_disabled", disabled)
        off_active = options.get("off_active", active)
        off_selected = options.get("off_selected", selected)
        off_disabled = options.get("off_disabled", disabled)

        icon_dict = {
            "char": char,
            "on": on,
            "off": off,
            "active": active,
            "selected": selected,
            "disabled": disabled,
            "on_active": on_active,
            "on_selected": on_selected,
            "on_disabled": on_disabled,
            "off_active": off_active,
            "off_selected": off_selected,
            "off_disabled": off_disabled,
        }
        names = [icon_dict.get(kw, name) for kw in icon_kw]
        prefix, chars = self._get_prefix_chars(names)
        options.update(dict(zip(*(icon_kw, chars))))
        options.update({"prefix": prefix})

        # Handle colors for modes (Active, Disabled, Selected, Normal)
        # and states (On, Off)
        color = options.get("color")
        options.setdefault("color_on", color)
        options.setdefault("color_active", options["color_on"])
        options.setdefault("color_selected", options["color_active"])
        options.setdefault("color_on_active", options["color_active"])
        options.setdefault("color_on_selected", options["color_selected"])
        options.setdefault("color_on_disabled", options["color_disabled"])
        options.setdefault("color_off", color)
        options.setdefault("color_off_active", options["color_active"])
        options.setdefault("color_off_selected", options["color_selected"])
        options.setdefault("color_off_disabled", options["color_disabled"])

        return options

    def _get_prefix_chars(self, names: Iterable[str]) -> Tuple[str, List[str]]:
        chars = []
        for name in names:
            if "." not in name:
                raise Exception("Invalid icon name")
            prefix, n = name.split(".")
            if prefix not in self.charmap:
                raise Exception(f'Invalid font prefix "{prefix}"')
            if n not in self.charmap[prefix]:
                raise Exception(f'Invalid icon name "{n}" in font "{prefix}"')
            chars.append(self.charmap[prefix][n])
        return prefix, chars

    def font(self, prefix: str, size: float) -> gui.Font:
        """Return a gui.Font corresponding to the given prefix and size."""
        font = gui.Font(self.fontname[prefix])
        font.setPixelSize(round(size))
        if prefix[-1] == "s":  # solid style
            font.setStyleName("Solid")
        return font

    def set_custom_icon(self, name: str, painter: CharIconPainter):
        """Associate a user-provided CharIconPainter to an icon name.

        The custom icon can later be addressed by calling
        icon('custom.NAME') where NAME is the provided name for that icon.

        Parameters
        ----------
        name: str
            name of the custom icon
        painter: CharIconPainter
            The icon painter, implementing
            ``paint(self, iconic, painter, rect, mode, state, options)``
        """
        self.painters[name] = painter

    def _custom_icon(self, name: str, **kwargs) -> QtGui.QIcon:
        """Return the custom icon corresponding to the given name."""
        if name not in self.painters:
            return QtGui.QIcon()
        return self._icon_by_painter(
            self.painters[name], dict(_default_options, **kwargs)
        )

    def _icon_by_painter(self, painter: CharIconPainter, options) -> QtGui.QIcon:
        """Return the icon corresponding to the given painter."""
        engine = CharIconEngine(self, painter, options)
        return QtGui.QIcon(engine)
