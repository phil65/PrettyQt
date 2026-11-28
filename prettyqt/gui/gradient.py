from typing import TYPE_CHECKING, Any, Literal

from prettyqt import gui
from prettyqt.utils import bidict, colors


if TYPE_CHECKING:
    from prettyqt.utils import datatypes


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
    "strong_bliss",
    "fresh_milk",
    "snow_again",
    "february_ink",
    "kind_steel",
    "soft_grass",
    "grown_early",
    "sharp_blues",
    "shady_water",
    "dirty_beauty",
    "great_whale",
    "teen_notebook",
    "polite_rumors",
    "sweet_period",
    "wide_matrix",
    "soft_cherish",
    "red_salvation",
    "burning_spring",
    "night_party",
    "sky_glider",
    "heaven_peach",
    "purple_division",
    "aqua_splash",
    "spiky_naga",
    "love_kiss",
    "clean_mirror",
    "premium_dark",
    "cold_evening",
    "cochiti_lake",
    "summer_games",
    "passionate_bed",
    "mountain_rock",
    "desert_hump",
    "jungle_day",
    "phoenix_start",
    "october_silence",
    "faraway_river",
    "alchemist_lab",
    "over_sun",
    "premium_white",
    "mars_party",
    "eternal_constance",
    "japan_blush",
    "smiling_rain",
    "cloudy_apple",
    "big_mango",
    "healthy_water",
    "amour_amour",
    "risky_concrete",
    "strong_stick",
    "vicious_stance",
    "palo_alto",
    "happy_memories",
    "midnight_bloom",
    "crystalline",
    "party_bliss",
    "confident_cloud",
    "le_cocktail",
    "river_city",
    "frozen_berry",
    "child_care",
    "flying_lemon",
    "new_retrowave",
    "hidden_jaguar",
    "above_the_sky",
    "nega",
    "dense_water",
    "seashore",
    "marble_wall",
    "cheerful_caramel",
    "night_sky",
    "magic_lake",
    "young_grass",
    "colorful_peach",
    "gentle_care",
    "plum_bath",
    "happy_unicorn",
    "african_field",
    "solid_stone",
    "orange_juice",
    "glass_water",
    "north_miracle",
    "fruit_blend",
    "millennium_pine",
    "high_flight",
    "mole_hall",
    "space_shift",
    "forest_inei",
    "royal_garden",
    "rich_metal",
    "juicy_cake",
    "smart_indigo",
    "sand_strike",
    "norse_beauty",
    "aqua_guidance",
    "sun_veggie",
    "sea_lord",
    "black_sea",
    "grass_shampoo",
    "landing_aircraft",
    "witch_dance",
    "sleepless_night",
    "angel_care",
    "crystal_river",
    "soft_lipstick",
    "salt_mountain",
    "perfect_white",
    "fresh_oasis",
    "strict_november",
    "morning_salad",
    "deep_relief",
    "sea_strike",
    "night_call",
    "supreme_sky",
    "light_blue",
    "mind_crawl",
    "lily_meadow",
    "sugar_lollipop",
    "sweet_dessert",
    "magic_ray",
    "teen_party",
    "frozen_heat",
    "gagarin_view",
    "fabled_sunset",
    "perfect_blue",
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
    strong_bliss=gui.QGradient.Preset.StrongBliss,
    fresh_milk=gui.QGradient.Preset.FreshMilk,
    snow_again=gui.QGradient.Preset.SnowAgain,
    february_ink=gui.QGradient.Preset.FebruaryInk,
    kind_steel=gui.QGradient.Preset.KindSteel,
    soft_grass=gui.QGradient.Preset.SoftGrass,
    grown_early=gui.QGradient.Preset.GrownEarly,
    sharp_blues=gui.QGradient.Preset.SharpBlues,
    shady_water=gui.QGradient.Preset.ShadyWater,
    dirty_beauty=gui.QGradient.Preset.DirtyBeauty,
    great_whale=gui.QGradient.Preset.GreatWhale,
    teen_notebook=gui.QGradient.Preset.TeenNotebook,
    polite_rumors=gui.QGradient.Preset.PoliteRumors,
    sweet_period=gui.QGradient.Preset.SweetPeriod,
    wide_matrix=gui.QGradient.Preset.WideMatrix,
    soft_cherish=gui.QGradient.Preset.SoftCherish,
    red_salvation=gui.QGradient.Preset.RedSalvation,
    burning_spring=gui.QGradient.Preset.BurningSpring,
    night_party=gui.QGradient.Preset.NightParty,
    sky_glider=gui.QGradient.Preset.SkyGlider,
    heaven_peach=gui.QGradient.Preset.HeavenPeach,
    purple_division=gui.QGradient.Preset.PurpleDivision,
    aqua_splash=gui.QGradient.Preset.AquaSplash,
    spiky_naga=gui.QGradient.Preset.SpikyNaga,
    love_kiss=gui.QGradient.Preset.LoveKiss,
    clean_mirror=gui.QGradient.Preset.CleanMirror,
    premium_dark=gui.QGradient.Preset.PremiumDark,
    cold_evening=gui.QGradient.Preset.ColdEvening,
    cochiti_lake=gui.QGradient.Preset.CochitiLake,
    summer_games=gui.QGradient.Preset.SummerGames,
    passionate_bed=gui.QGradient.Preset.PassionateBed,
    mountain_rock=gui.QGradient.Preset.MountainRock,
    desert_hump=gui.QGradient.Preset.DesertHump,
    jungle_day=gui.QGradient.Preset.JungleDay,
    phoenix_start=gui.QGradient.Preset.PhoenixStart,
    october_silence=gui.QGradient.Preset.OctoberSilence,
    faraway_river=gui.QGradient.Preset.FarawayRiver,
    alchemist_lab=gui.QGradient.Preset.AlchemistLab,
    over_sun=gui.QGradient.Preset.OverSun,
    premium_white=gui.QGradient.Preset.PremiumWhite,
    mars_party=gui.QGradient.Preset.MarsParty,
    eternal_constance=gui.QGradient.Preset.EternalConstance,
    japan_blush=gui.QGradient.Preset.JapanBlush,
    smiling_rain=gui.QGradient.Preset.SmilingRain,
    cloudy_apple=gui.QGradient.Preset.CloudyApple,
    big_mango=gui.QGradient.Preset.BigMango,
    healthy_water=gui.QGradient.Preset.HealthyWater,
    amour_amour=gui.QGradient.Preset.AmourAmour,
    risky_concrete=gui.QGradient.Preset.RiskyConcrete,
    strong_stick=gui.QGradient.Preset.StrongStick,
    vicious_stance=gui.QGradient.Preset.ViciousStance,
    palo_alto=gui.QGradient.Preset.PaloAlto,
    happy_memories=gui.QGradient.Preset.HappyMemories,
    midnight_bloom=gui.QGradient.Preset.MidnightBloom,
    crystalline=gui.QGradient.Preset.Crystalline,
    party_bliss=gui.QGradient.Preset.PartyBliss,
    confident_cloud=gui.QGradient.Preset.ConfidentCloud,
    le_cocktail=gui.QGradient.Preset.LeCocktail,
    river_city=gui.QGradient.Preset.RiverCity,
    frozen_berry=gui.QGradient.Preset.FrozenBerry,
    child_care=gui.QGradient.Preset.ChildCare,
    flying_lemon=gui.QGradient.Preset.FlyingLemon,
    new_retrowave=gui.QGradient.Preset.NewRetrowave,
    hidden_jaguar=gui.QGradient.Preset.HiddenJaguar,
    above_the_sky=gui.QGradient.Preset.AboveTheSky,
    nega=gui.QGradient.Preset.Nega,
    dense_water=gui.QGradient.Preset.DenseWater,
    seashore=gui.QGradient.Preset.Seashore,
    marble_wall=gui.QGradient.Preset.MarbleWall,
    cheerful_caramel=gui.QGradient.Preset.CheerfulCaramel,
    night_sky=gui.QGradient.Preset.NightSky,
    magic_lake=gui.QGradient.Preset.MagicLake,
    young_grass=gui.QGradient.Preset.YoungGrass,
    colorful_peach=gui.QGradient.Preset.ColorfulPeach,
    gentle_care=gui.QGradient.Preset.GentleCare,
    plum_bath=gui.QGradient.Preset.PlumBath,
    happy_unicorn=gui.QGradient.Preset.HappyUnicorn,
    african_field=gui.QGradient.Preset.AfricanField,
    solid_stone=gui.QGradient.Preset.SolidStone,
    orange_juice=gui.QGradient.Preset.OrangeJuice,
    glass_water=gui.QGradient.Preset.GlassWater,
    north_miracle=gui.QGradient.Preset.NorthMiracle,
    fruit_blend=gui.QGradient.Preset.FruitBlend,
    millennium_pine=gui.QGradient.Preset.MillenniumPine,
    high_flight=gui.QGradient.Preset.HighFlight,
    mole_hall=gui.QGradient.Preset.MoleHall,
    space_shift=gui.QGradient.Preset.SpaceShift,
    forest_inei=gui.QGradient.Preset.ForestInei,
    royal_garden=gui.QGradient.Preset.RoyalGarden,
    rich_metal=gui.QGradient.Preset.RichMetal,
    juicy_cake=gui.QGradient.Preset.JuicyCake,
    smart_indigo=gui.QGradient.Preset.SmartIndigo,
    sand_strike=gui.QGradient.Preset.SandStrike,
    norse_beauty=gui.QGradient.Preset.NorseBeauty,
    aqua_guidance=gui.QGradient.Preset.AquaGuidance,
    sun_veggie=gui.QGradient.Preset.SunVeggie,
    sea_lord=gui.QGradient.Preset.SeaLord,
    black_sea=gui.QGradient.Preset.BlackSea,
    grass_shampoo=gui.QGradient.Preset.GrassShampoo,
    landing_aircraft=gui.QGradient.Preset.LandingAircraft,
    witch_dance=gui.QGradient.Preset.WitchDance,
    sleepless_night=gui.QGradient.Preset.SleeplessNight,
    angel_care=gui.QGradient.Preset.AngelCare,
    crystal_river=gui.QGradient.Preset.CrystalRiver,
    soft_lipstick=gui.QGradient.Preset.SoftLipstick,
    salt_mountain=gui.QGradient.Preset.SaltMountain,
    perfect_white=gui.QGradient.Preset.PerfectWhite,
    fresh_oasis=gui.QGradient.Preset.FreshOasis,
    strict_november=gui.QGradient.Preset.StrictNovember,
    morning_salad=gui.QGradient.Preset.MorningSalad,
    deep_relief=gui.QGradient.Preset.DeepRelief,
    sea_strike=gui.QGradient.Preset.SeaStrike,
    night_call=gui.QGradient.Preset.NightCall,
    supreme_sky=gui.QGradient.Preset.SupremeSky,
    light_blue=gui.QGradient.Preset.LightBlue,
    mind_crawl=gui.QGradient.Preset.MindCrawl,
    lily_meadow=gui.QGradient.Preset.LilyMeadow,
    sugar_lollipop=gui.QGradient.Preset.SugarLollipop,
    sweet_dessert=gui.QGradient.Preset.SweetDessert,
    magic_ray=gui.QGradient.Preset.MagicRay,
    teen_party=gui.QGradient.Preset.TeenParty,
    frozen_heat=gui.QGradient.Preset.FrozenHeat,
    gagarin_view=gui.QGradient.Preset.GagarinView,
    fabled_sunset=gui.QGradient.Preset.FabledSunset,
    perfect_blue=gui.QGradient.Preset.PerfectBlue,
)


if TYPE_CHECKING:
    from prettyqt.qt import QtGui

    _GradientBase = QtGui.QGradient
else:
    _GradientBase = object


class GradientMixin(_GradientBase):
    def __setitem__(self, key: float, value: datatypes.ColorType):
        self.set_color_at(key, value)

    def serialize(self) -> dict[str, Any]:
        return dict(
            coordinate_mode=self.get_coordinate_mode(),
            spread=self.get_spread(),
            stops=self.get_stops(),
        )

    def set_color_at(self, key: float, color: datatypes.ColorType):
        super().setColorAt(key, colors.get_color(color))

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
        for pos, color in self.stops():
            if factor > 0:
                self.setColorAt(pos, color.lighter(factor))
            else:
                self.setColorAt(pos, color.darker(-factor))


class Gradient(GradientMixin, gui.QGradient):
    """Used in combination with QBrush to specify gradient fills."""


if __name__ == "__main__":
    grad = Gradient.for_palette(gui.Palette())
