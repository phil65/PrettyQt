"""A lightweight module handling iconic fonts.

It is designed to provide a simple way for creating QtGui.QIcons from glyphs.

From a user's viewpoint, the main entry point is the ``IconicFont`` class which
contains methods for loading new iconic fonts with their character map and
methods returning instances of ``QIcon``.

"""

from __future__ import annotations

# Standard library imports
from typing import Any

from prettyqt import constants, gui
from prettyqt.iconprovider import chariconengine
from prettyqt.qt import QtCore, QtGui


_default_options = {
    "color": gui.Color(50, 50, 50),
    "color_disabled": gui.Color(150, 150, 150),
    "opacity": 1.0,
    "scale_factor": 1.0,
}

ICON_KW = [
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

VALID_OPTIONS = [
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

COLOR_OPTIONS = {
    QtGui.QIcon.State.On: {
        QtGui.QIcon.Mode.Normal: ("color_on", "on"),
        QtGui.QIcon.Mode.Disabled: ("color_on_disabled", "on_disabled"),
        QtGui.QIcon.Mode.Active: ("color_on_active", "on_active"),
        QtGui.QIcon.Mode.Selected: ("color_on_selected", "on_selected"),
    },
    QtGui.QIcon.State.Off: {
        QtGui.QIcon.Mode.Normal: ("color_off", "off"),
        QtGui.QIcon.Mode.Disabled: ("color_off_disabled", "off_disabled"),
        QtGui.QIcon.Mode.Active: ("color_off_active", "off_active"),
        QtGui.QIcon.Mode.Selected: ("color_off_selected", "off_selected"),
    },
}


def set_global_defaults(**kwargs):
    """Set global defaults for the options passed to the icon painter."""
    for kw in kwargs:
        if kw not in VALID_OPTIONS:
            raise KeyError(f"Invalid option {kw!r}")
        _default_options[kw] = kwargs[kw]


class FontError(Exception):
    """Exception for font errors."""


class IconicFont:
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
        self.icon_cache = {}
        self.fonts = {font.prefix: font for font in args}

    def paint(
        self,
        painter: gui.Painter,
        rect: QtCore.QRect,
        mode: QtGui.QIcon.Mode,
        state: QtGui.QIcon.State,
        options: list[dict[str, Any]],
    ):
        color_str, char = COLOR_OPTIONS[state][mode]
        for opt in options:
            painter.save()
            color = gui.Color(opt[color_str])
            painter.setPen(color)

            # A 16 pixel-high icon yields a font size of 14, which is pixel perfect
            # for font-awesome. 16 * 0.875 = 14
            # The reason why the glyph size is smaller than the icon size is to
            # account for font bearing.

            draw_size = round(0.875 * rect.height() * opt["scale_factor"])
            # Animation setup hook
            if (animation := opt.get("animation")) is not None:
                animation.setup(painter, rect)
            font = self.fonts[opt["prefix"]].get_font(draw_size)
            painter.setFont(font)
            if "offset" in opt:
                rect.translate(
                    round(opt["offset"][0] * rect.width()),
                    round(opt["offset"][1] * rect.height()),
                )
            x_center = rect.width() * 0.5
            y_center = rect.height() * 0.5
            painter.translate(x_center, y_center)
            transform = gui.Transform()
            if opt.get("vflip") is True:
                transform.scale(1, -1)
            if opt.get("hflip") is True:
                transform.scale(-1, 1)
            if "rotated" in opt:
                transform.rotate(opt["rotated"])
            painter.setTransform(transform, True)
            painter.translate(-x_center, -y_center)
            if (opacity := opt.get("opacity")) is not None:
                painter.setOpacity(opacity)

            painter.drawText(rect, int(constants.ALIGN_CENTER), opt[char])  # type: ignore
            painter.restore()

    def has_valid_font_ids(self) -> bool:
        """Validate instance's font ids are loaded to QFontDatabase.

        It is possible that QFontDatabase was reset or QApplication was recreated
        in both cases it is possible that font is not available.
        """
        # Check stored font ids are still available
        return all(font.is_valid() for font in self.fonts.values())

    def icon(self, *names, **kwargs) -> QtGui.QIcon:
        """Return a QtGui.QIcon object corresponding to the provided icon name."""
        cache_key = f"{names}{kwargs}"
        if cache_key in self.icon_cache:
            return self.icon_cache[cache_key]
        opts = kwargs.pop("options", [{}] * len(names))
        if len(opts) != len(names):
            raise TypeError(f'"options" must be a list of size {len(names)}')
        parsed_options = [self._parse_options(o, kwargs, n) for o, n in zip(opts, names)]
        engine = chariconengine.CharIconEngine(self, parsed_options)
        icon = QtGui.QIcon(engine)
        self.icon_cache[cache_key] = icon
        return icon

    def _parse_options(
        self, specific_options: dict, general_options: dict, name: str
    ) -> dict[str, Any]:
        options = dict(_default_options, **general_options)
        options.update(specific_options)

        # Handle icons for modes (Active, Disabled, Selected, Normal)
        # and states (On, Off)
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
        names = [icon_dict.get(kw, name) for kw in ICON_KW]
        chars = []
        for name in names:
            if "." not in name:
                raise Exception("Invalid icon name")
            prefix, n = name.split(".")
            if prefix not in self.fonts:
                raise Exception(f"Invalid font prefix {prefix!r}")
            if n not in self.fonts[prefix].charmap:
                raise Exception(f"Invalid icon name {n!r} in font {prefix!r}")
            chars.append(self.fonts[prefix].charmap[n])
        options.update(dict(zip(*(ICON_KW, chars))))
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
