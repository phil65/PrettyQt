from __future__ import annotations

from typing import Any, Literal

from prettyqt import gui
from prettyqt.qt import QtGui
from prettyqt.utils import bidict


CoordinateModeStr = Literal["logical", "object", "stretch_to_device", "object_bounding"]

COORDINATE_MODE: bidict[CoordinateModeStr, QtGui.QGradient.CoordinateMode] = bidict(
    logical=QtGui.QGradient.CoordinateMode.LogicalMode,
    object=QtGui.QGradient.CoordinateMode.ObjectMode,
    stretch_to_device=QtGui.QGradient.CoordinateMode.StretchToDeviceMode,
    object_bounding=QtGui.QGradient.CoordinateMode.ObjectBoundingMode,
)

SpreadStr = Literal["pad", "repeat", "reflect"]

SPREAD: bidict[SpreadStr, QtGui.QGradient.Spread] = bidict(
    pad=QtGui.QGradient.Spread.PadSpread,
    repeat=QtGui.QGradient.Spread.RepeatSpread,
    reflect=QtGui.QGradient.Spread.ReflectSpread,
)

TypeStr = Literal["linear", "radial", "conical", "none"]

TYPE: bidict[TypeStr, QtGui.QGradient.Type] = bidict(
    linear=QtGui.QGradient.Type.LinearGradient,
    radial=QtGui.QGradient.Type.RadialGradient,
    conical=QtGui.QGradient.Type.ConicalGradient,
    none=QtGui.QGradient.Type.NoGradient,
)

PresetStr = Literal[
    "warm_flame",
    "night_fade",
    "spring_warmth",
    "juicy_peach",
    "young_passion",
    "lady_lips",
    "sunny_morning",
    "rainy_ashville",
    "frozen_dreams",
    "winter_neva",
    "dusty_grass",
    "tempting_azure",
    "heavy_rain",
    "amy_crisp",
    "mean_fruit",
    "deep_blue",
    "ripe_malinka",
    "cloudy_knoxville",
    "malibu_beach",
    "new_life",
    "true_sunset",
    "morpheus_den",
    "rare_wind",
    "near_moon",
    "wild_apple",
    "saint_petersburg",
    "plum_plate",
    "everlasting_sky",
    "happy_fisher",
    "blessing",
    "sharpeye_eagle",
    "ladoga_bottom",
    "lemon_gate",
    "itmeo_branding",
    "zeus_miracle",
    "old_hat",
    "star_wine",
    "happy_acid",
    "awesome_pine",
    "new_york",
    "shy_rainbow",
    "mixed_hopes",
    "fly_high",
]

PRESET: bidict[PresetStr, QtGui.QGradient.Preset] = bidict(
    warm_flame=QtGui.QGradient.Preset.WarmFlame,
    night_fade=QtGui.QGradient.Preset.NightFade,
    spring_warmth=QtGui.QGradient.Preset.SpringWarmth,
    juicy_peach=QtGui.QGradient.Preset.JuicyPeach,
    young_passion=QtGui.QGradient.Preset.YoungPassion,
    lady_lips=QtGui.QGradient.Preset.LadyLips,
    sunny_morning=QtGui.QGradient.Preset.SunnyMorning,
    rainy_ashville=QtGui.QGradient.Preset.RainyAshville,
    frozen_dreams=QtGui.QGradient.Preset.FrozenDreams,
    winter_neva=QtGui.QGradient.Preset.WinterNeva,
    dusty_grass=QtGui.QGradient.Preset.DustyGrass,
    tempting_azure=QtGui.QGradient.Preset.TemptingAzure,
    heavy_rain=QtGui.QGradient.Preset.HeavyRain,
    amy_crisp=QtGui.QGradient.Preset.AmyCrisp,
    mean_fruit=QtGui.QGradient.Preset.MeanFruit,
    deep_blue=QtGui.QGradient.Preset.DeepBlue,
    ripe_malinka=QtGui.QGradient.Preset.RipeMalinka,
    cloudy_knoxville=QtGui.QGradient.Preset.CloudyKnoxville,
    malibu_beach=QtGui.QGradient.Preset.MalibuBeach,
    new_life=QtGui.QGradient.Preset.NewLife,
    true_sunset=QtGui.QGradient.Preset.TrueSunset,
    morpheus_den=QtGui.QGradient.Preset.MorpheusDen,
    rare_wind=QtGui.QGradient.Preset.RareWind,
    near_moon=QtGui.QGradient.Preset.NearMoon,
    wild_apple=QtGui.QGradient.Preset.WildApple,
    saint_petersburg=QtGui.QGradient.Preset.SaintPetersburg,
    plum_plate=QtGui.QGradient.Preset.PlumPlate,
    everlasting_sky=QtGui.QGradient.Preset.EverlastingSky,
    happy_fisher=QtGui.QGradient.Preset.HappyFisher,
    blessing=QtGui.QGradient.Preset.Blessing,
    sharpeye_eagle=QtGui.QGradient.Preset.SharpeyeEagle,
    ladoga_bottom=QtGui.QGradient.Preset.LadogaBottom,
    lemon_gate=QtGui.QGradient.Preset.LemonGate,
    itmeo_branding=QtGui.QGradient.Preset.ItmeoBranding,
    zeus_miracle=QtGui.QGradient.Preset.ZeusMiracle,
    old_hat=QtGui.QGradient.Preset.OldHat,
    star_wine=QtGui.QGradient.Preset.StarWine,
    happy_acid=QtGui.QGradient.Preset.HappyAcid,
    awesome_pine=QtGui.QGradient.Preset.AwesomePine,
    new_york=QtGui.QGradient.Preset.NewYork,
    shy_rainbow=QtGui.QGradient.Preset.ShyRainbow,
    mixed_hopes=QtGui.QGradient.Preset.MixedHopes,
    fly_high=QtGui.QGradient.Preset.FlyHigh,
    # ...
)


class GradientMixin:
    def __setitem__(self, key: float, value):
        self.setColorAt(key, value)

    def serialize(self) -> dict[str, Any]:
        return dict(
            coordinate_mode=self.get_coordinate_mode(),
            spread=self.get_spread(),
            stops=self.get_stops(),
        )

    def set_coordinate_mode(
        self, mode: CoordinateModeStr | QtGui.QGradient.CoordinateMode
    ):
        """Set the coordinate mode.

        Args:
            mode: coordinate mode
        """
        self.setCoordinateMode(COORDINATE_MODE.get_enum_value(mode))

    def get_coordinate_mode(self) -> CoordinateModeStr:
        """Return current coordinate mode.

        Returns:
            coordinate mode
        """
        return COORDINATE_MODE.inverse[self.coordinateMode()]

    def set_spread(self, method: SpreadStr | QtGui.QGradient.Spread):
        """Set the spread method.

        Args:
            method: spread method
        """
        self.setSpread(SPREAD.get_enum_value(method))

    def get_spread(self) -> SpreadStr:
        """Return current spread method.

        Returns:
            spread method
        """
        return SPREAD.inverse[self.spread()]

    def get_type(self) -> TypeStr:
        """Return current gradient type.

        Returns:
            gradient type
        """
        return TYPE.inverse[self.type()]

    def get_stops(self) -> list[tuple[float, gui.Color]]:
        return [(i, gui.Color(j)) for (i, j) in self.stops()]

    @classmethod
    def for_palette(cls, palette: gui.Palette, group: gui.palette.GroupStr = "active"):
        gradient = cls()
        for i, role_name in enumerate(gui.palette.ROLE):
            color = palette.get_color(role_name, group)
            gradient.setColorAt(i / len(gui.palette.ROLE), color)
        return gradient

    def change_brightness(self, factor: float):
        # still need to streamline changing brightness across the framework...
        # color.lighter returns a lighter color when arg is > 100 (same for darker)
        factor = int(factor * 100)
        for pos, color in grad.stops():
            if factor > 0:
                self.setColorAt(pos, color.lighter(factor))
            else:
                self.setColorAt(pos, color.darker(-factor))


class Gradient(GradientMixin, QtGui.QGradient):
    pass


if __name__ == "__main__":
    grad = Gradient.for_palette(gui.Palette())
