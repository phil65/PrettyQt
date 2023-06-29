from __future__ import annotations

from typing import Any, Literal

from prettyqt import gui
from prettyqt.utils import bidict


CoordinateModeStr = Literal["logical", "object", "stretch_to_device", "object_bounding"]

COORDINATE_MODE: bidict[CoordinateModeStr, gui.QGradient.CoordinateMode] = bidict(
    logical=gui.QGradient.CoordinateMode.LogicalMode,
    object=gui.QGradient.CoordinateMode.ObjectMode,
    stretch_to_device=gui.QGradient.CoordinateMode.StretchToDeviceMode,
    object_bounding=gui.QGradient.CoordinateMode.ObjectBoundingMode,
)

SpreadStr = Literal["pad", "repeat", "reflect"]

SPREAD: bidict[SpreadStr, gui.QGradient.Spread] = bidict(
    pad=gui.QGradient.Spread.PadSpread,
    repeat=gui.QGradient.Spread.RepeatSpread,
    reflect=gui.QGradient.Spread.ReflectSpread,
)

TypeStr = Literal["linear", "radial", "conical", "none"]

TYPE: bidict[TypeStr, gui.QGradient.Type] = bidict(
    linear=gui.QGradient.Type.LinearGradient,
    radial=gui.QGradient.Type.RadialGradient,
    conical=gui.QGradient.Type.ConicalGradient,
    none=gui.QGradient.Type.NoGradient,
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

PRESET: bidict[PresetStr, gui.QGradient.Preset] = bidict(
    warm_flame=gui.QGradient.Preset.WarmFlame,
    night_fade=gui.QGradient.Preset.NightFade,
    spring_warmth=gui.QGradient.Preset.SpringWarmth,
    juicy_peach=gui.QGradient.Preset.JuicyPeach,
    young_passion=gui.QGradient.Preset.YoungPassion,
    lady_lips=gui.QGradient.Preset.LadyLips,
    sunny_morning=gui.QGradient.Preset.SunnyMorning,
    rainy_ashville=gui.QGradient.Preset.RainyAshville,
    frozen_dreams=gui.QGradient.Preset.FrozenDreams,
    winter_neva=gui.QGradient.Preset.WinterNeva,
    dusty_grass=gui.QGradient.Preset.DustyGrass,
    tempting_azure=gui.QGradient.Preset.TemptingAzure,
    heavy_rain=gui.QGradient.Preset.HeavyRain,
    amy_crisp=gui.QGradient.Preset.AmyCrisp,
    mean_fruit=gui.QGradient.Preset.MeanFruit,
    deep_blue=gui.QGradient.Preset.DeepBlue,
    ripe_malinka=gui.QGradient.Preset.RipeMalinka,
    cloudy_knoxville=gui.QGradient.Preset.CloudyKnoxville,
    malibu_beach=gui.QGradient.Preset.MalibuBeach,
    new_life=gui.QGradient.Preset.NewLife,
    true_sunset=gui.QGradient.Preset.TrueSunset,
    morpheus_den=gui.QGradient.Preset.MorpheusDen,
    rare_wind=gui.QGradient.Preset.RareWind,
    near_moon=gui.QGradient.Preset.NearMoon,
    wild_apple=gui.QGradient.Preset.WildApple,
    saint_petersburg=gui.QGradient.Preset.SaintPetersburg,
    plum_plate=gui.QGradient.Preset.PlumPlate,
    everlasting_sky=gui.QGradient.Preset.EverlastingSky,
    happy_fisher=gui.QGradient.Preset.HappyFisher,
    blessing=gui.QGradient.Preset.Blessing,
    sharpeye_eagle=gui.QGradient.Preset.SharpeyeEagle,
    ladoga_bottom=gui.QGradient.Preset.LadogaBottom,
    lemon_gate=gui.QGradient.Preset.LemonGate,
    itmeo_branding=gui.QGradient.Preset.ItmeoBranding,
    zeus_miracle=gui.QGradient.Preset.ZeusMiracle,
    old_hat=gui.QGradient.Preset.OldHat,
    star_wine=gui.QGradient.Preset.StarWine,
    happy_acid=gui.QGradient.Preset.HappyAcid,
    awesome_pine=gui.QGradient.Preset.AwesomePine,
    new_york=gui.QGradient.Preset.NewYork,
    shy_rainbow=gui.QGradient.Preset.ShyRainbow,
    mixed_hopes=gui.QGradient.Preset.MixedHopes,
    fly_high=gui.QGradient.Preset.FlyHigh,
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

    def set_coordinate_mode(self, mode: CoordinateModeStr | gui.QGradient.CoordinateMode):
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

    def set_spread(self, method: SpreadStr | gui.QGradient.Spread):
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


class Gradient(GradientMixin, gui.QGradient):
    pass


if __name__ == "__main__":
    grad = Gradient.for_palette(gui.Palette())
