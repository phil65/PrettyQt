from __future__ import annotations

from typing import Any, Literal

from prettyqt import gui
from prettyqt.qt import QtGui
from prettyqt.utils import InvalidParamError, bidict, prettyprinter


COORDINATE_MODE = bidict(
    logical=QtGui.QGradient.LogicalMode,
    object=QtGui.QGradient.ObjectMode,
    stretch_to_device=QtGui.QGradient.StretchToDeviceMode,
    object_bounding=QtGui.QGradient.ObjectBoundingMode,
)

CoordinateModeStr = Literal["logical", "object", "stretch_to_device", "object_bounding"]

SPREAD = bidict(
    pad=QtGui.QGradient.PadSpread,
    repeat=QtGui.QGradient.RepeatSpread,
    reflect=QtGui.QGradient.ReflectSpread,
)

SpreadStr = Literal["pad", "repeat", "reflect"]

TYPE = bidict(
    linear=QtGui.QGradient.LinearGradient,
    radial=QtGui.QGradient.RadialGradient,
    conical=QtGui.QGradient.ConicalGradient,
    none=QtGui.QGradient.NoGradient,
)

TypeStr = Literal["linear", "radial", "conical", "none"]


PRESET = bidict(
    warm_flame=QtGui.QGradient.WarmFlame,
    night_fade=QtGui.QGradient.NightFade,
    spring_warmth=QtGui.QGradient.SpringWarmth,
    juicy_peach=QtGui.QGradient.JuicyPeach,
    young_passion=QtGui.QGradient.YoungPassion,
    lady_lips=QtGui.QGradient.LadyLips,
    sunny_morning=QtGui.QGradient.SunnyMorning,
    rainy_ashville=QtGui.QGradient.RainyAshville,
    frozen_dreams=QtGui.QGradient.FrozenDreams,
    winter_neva=QtGui.QGradient.WinterNeva,
    dusty_grass=QtGui.QGradient.DustyGrass,
    tempting_azure=QtGui.QGradient.TemptingAzure,
    heavy_rain=QtGui.QGradient.HeavyRain,
    amy_crisp=QtGui.QGradient.AmyCrisp,
    mean_fruit=QtGui.QGradient.MeanFruit,
    deep_blue=QtGui.QGradient.DeepBlue,
    ripe_malinka=QtGui.QGradient.RipeMalinka,
    cloudy_knoxville=QtGui.QGradient.CloudyKnoxville,
    malibu_beach=QtGui.QGradient.MalibuBeach,
    new_life=QtGui.QGradient.NewLife,
    true_sunset=QtGui.QGradient.TrueSunset,
    morpheus_den=QtGui.QGradient.MorpheusDen,
    rare_wind=QtGui.QGradient.RareWind,
    near_moon=QtGui.QGradient.NearMoon,
    wild_apple=QtGui.QGradient.WildApple,
    saint_petersburg=QtGui.QGradient.SaintPetersburg,
    plum_plate=QtGui.QGradient.PlumPlate,
    everlasting_sky=QtGui.QGradient.EverlastingSky,
    happy_fisher=QtGui.QGradient.HappyFisher,
    blessing=QtGui.QGradient.Blessing,
    sharpeye_eagle=QtGui.QGradient.SharpeyeEagle,
    ladoga_bottom=QtGui.QGradient.LadogaBottom,
    lemon_gate=QtGui.QGradient.LemonGate,
    itmeo_branding=QtGui.QGradient.ItmeoBranding,
    zeus_miracle=QtGui.QGradient.ZeusMiracle,
    old_hat=QtGui.QGradient.OldHat,
    star_wine=QtGui.QGradient.StarWine,
    happy_acid=QtGui.QGradient.HappyAcid,
    awesome_pine=QtGui.QGradient.AwesomePine,
    new_york=QtGui.QGradient.NewYork,
    shy_rainbow=QtGui.QGradient.ShyRainbow,
    mixed_hopes=QtGui.QGradient.MixedHopes,
    fly_high=QtGui.QGradient.FlyHigh,
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
