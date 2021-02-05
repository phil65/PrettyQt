from __future__ import annotations

from prettyqt import gui
from prettyqt.utils import types


WINDOW_ICON_COLOR = "darkcyan"


def set_window_icon_color(color: str):
    global WINDOW_ICON_COLOR
    WINDOW_ICON_COLOR = color


def get_color(color: types.ColorType) -> gui.Color:
    """Get gui.Color instance for given parameter.

    named colors are 'aliceblue', 'antiquewhite', 'aqua', 'aquamarine',
    'azure', 'beige', 'bisque', 'black', 'blanchedalmond', 'blue', 'blueviolet',
    'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral',
    'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan',
    'darkgoldenrod', 'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki',
    'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred',
    'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey',
    'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey',
    'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro',
    'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow', 'grey',
    'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender',
    'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral',
    'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightgrey',
    'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray',
    'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen',
    'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid',
    'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen',
    'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose',
    'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orange',
    'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise',
    'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum',
    'powderblue', 'purple', 'red', 'rosybrown', 'royalblue', 'saddlebrown',
    'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue',
    'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue',
    'tan', 'teal', 'thistle', 'tomato', 'transparent', 'turquoise', 'violet',
    'wheat', 'white', 'whitesmoke', 'yellow', 'yellowgreen'

    Args:
        color (ColorType): color to create gui.Icon from

    Returns:
        gui.Color: color instance
    """
    if isinstance(color, (tuple, list)):
        return gui.Color(*color)
    return gui.Color(color)


def interpolate_text_colors(
    bg: types.ColorType, fg: types.ColorType, n_colors: int
) -> list[gui.Color]:
    bg = get_color(bg)
    fg = get_color(fg)
    pal = []
    M = 35
    HUE_BASE = 90 if bg.hue() == -1 else bg.hue()
    for i in range(n_colors):
        h = HUE_BASE + (360.0 / n_colors * i) % 360
        s = 240.0
        v = max(bg.value(), fg.value()) * 0.85
        if (bg.hue() - M < h < bg.hue() + M) or (fg.hue() - M < h < fg.hue() + M):
            h = ((bg.hue() + fg.hue()) / (i + 1)) % 360
            s = ((bg.saturation() + fg.saturation() + 2 * i) / 2) % 256
            v = ((bg.value() + fg.value() + 2 * i) / 2) % 256
        pal.append(gui.Color.from_hsv(h, s, v))
    return pal
