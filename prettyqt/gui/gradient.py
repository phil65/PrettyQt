from __future__ import annotations

from typing import Any, Literal

from prettyqt import gui
from prettyqt.qt import QtGui
from prettyqt.utils import InvalidParamError, bidict, prettyprinter


COORDINATE_MODE = bidict(
    logical=QtGui.QGradient.CoordinateMode.LogicalMode,
    object=QtGui.QGradient.CoordinateMode.ObjectMode,
    stretch_to_device=QtGui.QGradient.CoordinateMode.StretchToDeviceMode,
    object_bounding=QtGui.QGradient.CoordinateMode.ObjectBoundingMode,
)

CoordinateModeStr = Literal["logical", "object", "stretch_to_device", "object_bounding"]

SPREAD = bidict(
    pad=QtGui.QGradient.Spread.PadSpread,
    repeat=QtGui.QGradient.Spread.RepeatSpread,
    reflect=QtGui.QGradient.Spread.ReflectSpread,
)

SpreadStr = Literal["pad", "repeat", "reflect"]

TYPE = bidict(
    linear=QtGui.QGradient.Type.LinearGradient,
    radial=QtGui.QGradient.Type.RadialGradient,
    conical=QtGui.QGradient.Type.ConicalGradient,
    none=QtGui.QGradient.Type.NoGradient,
)

TypeStr = Literal["linear", "radial", "conical", "none"]


PRESET = bidict(
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


class Gradient(prettyprinter.PrettyPrinter, QtGui.QGradient):
    def __setitem__(self, key: float, value):
        self.setColorAt(key, value)

    def serialize_fields(self):
        return dict(
            coordinate_mode=self.get_coordinate_mode(),
            spread=self.get_spread(),
            stops=self.get_stops(),
        )

    def serialize(self) -> dict[str, Any]:
        return self.serialize_fields()

    def set_coordinate_mode(self, mode: CoordinateModeStr):
        """Set the coordinate mode.

        Args:
            mode: coordinate mode

        Raises:
            InvalidParamError: mode does not exist
        """
        if mode not in COORDINATE_MODE:
            raise InvalidParamError(mode, COORDINATE_MODE)
        self.setCoordinateMode(COORDINATE_MODE[mode])

    def get_coordinate_mode(self) -> CoordinateModeStr:
        """Return current coordinate mode.

        Returns:
            coordinate mode
        """
        return COORDINATE_MODE.inverse[self.coordinateMode()]

    def set_spread(self, method: SpreadStr):
        """Set the spread method.

        Args:
            method: spread method

        Raises:
            InvalidParamError: method does not exist
        """
        if method not in SPREAD:
            raise InvalidParamError(method, SPREAD)
        self.setSpread(SPREAD[method])

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


if __name__ == "__main__":
    grad = Gradient()
    grad.setStops([(0.0, gui.Color("red")), (1.0, gui.Color("green"))])
    print(grad.get_stops())
    print(repr(grad))
