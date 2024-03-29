from __future__ import annotations

from typing import Literal, Self

from prettyqt import constants
from prettyqt.qt import QtCore
from prettyqt.utils import bidict, get_repr


Loc = QtCore.QLocale
CN = Loc.Country

COUNTRY = bidict(
    any=CN.AnyCountry,
    afghanistan=CN.Afghanistan,
    aland_islands=CN.AlandIslands,
    albania=CN.Albania,
    algeria=CN.Algeria,
    american_samoa=CN.AmericanSamoa,
    andorra=CN.Andorra,
    angola=CN.Angola,
    anguilla=CN.Anguilla,
    antarctica=CN.Antarctica,
    antigua_and_barbuda=CN.AntiguaAndBarbuda,
    argentina=CN.Argentina,
    armenia=CN.Armenia,
    aruba=CN.Aruba,
    ascension_island=CN.AscensionIsland,
    australia=CN.Australia,
    austria=CN.Austria,
    azerbaijan=CN.Azerbaijan,
    bahamas=CN.Bahamas,
    bahrain=CN.Bahrain,
    bangladesh=CN.Bangladesh,
    barbados=CN.Barbados,
    belarus=CN.Belarus,
    belgium=CN.Belgium,
    belize=CN.Belize,
    benin=CN.Benin,
    bermuda=CN.Bermuda,
    bhutan=CN.Bhutan,
    bolivia=CN.Bolivia,
    bonaire=CN.Bonaire,
    bosnia_and_herzegowina=CN.BosniaAndHerzegowina,
    botswana=CN.Botswana,
    bouvet_island=CN.BouvetIsland,
    brazil=CN.Brazil,
    british_indian_ocean_territory=CN.BritishIndianOceanTerritory,
    british_virgin_islands=CN.BritishVirginIslands,
    brunei=CN.Brunei,
    bulgaria=CN.Bulgaria,
    burkina_faso=CN.BurkinaFaso,
    burundi=CN.Burundi,
    cambodia=CN.Cambodia,
    cameroon=CN.Cameroon,
    canada=CN.Canada,
    canary_islands=CN.CanaryIslands,
    cape_verde=CN.CapeVerde,
    cayman_islands=CN.CaymanIslands,
    central_african_republic=CN.CentralAfricanRepublic,
    ceuta_and_melilla=CN.CeutaAndMelilla,
    chad=CN.Chad,
    chile=CN.Chile,
    china=CN.China,
    christmas_island=CN.ChristmasIsland,
    clipperton_island=CN.ClippertonIsland,
    cocos_islands=CN.CocosIslands,
    colombia=CN.Colombia,
    comoros=CN.Comoros,
    congo_brazzaville=CN.CongoBrazzaville,
    congo_kinshasa=CN.CongoKinshasa,
    cook_islands=CN.CookIslands,
    costa_rica=CN.CostaRica,
    croatia=CN.Croatia,
    cuba=CN.Cuba,
    curasao=CN.CuraSao,
    cyprus=CN.Cyprus,
    czech_republic=CN.CzechRepublic,
    denmark=CN.Denmark,
    diego_garcia=CN.DiegoGarcia,
    djibouti=CN.Djibouti,
    dominica=CN.Dominica,
    dominican_republic=CN.DominicanRepublic,
    east_timor=CN.EastTimor,
    ecuador=CN.Ecuador,
    egypt=CN.Egypt,
    el_salvador=CN.ElSalvador,
    equatorial_guinea=CN.EquatorialGuinea,
    eritrea=CN.Eritrea,
    estonia=CN.Estonia,
    ethiopia=CN.Ethiopia,
    european_union=CN.EuropeanUnion,
    europe=CN.Europe,
    falkland_islands=CN.FalklandIslands,
    faroe_islands=CN.FaroeIslands,
    fiji=CN.Fiji,
    finland=CN.Finland,
    france=CN.France,
    french_guiana=CN.FrenchGuiana,
    french_polynesia=CN.FrenchPolynesia,
    french_southern_territories=CN.FrenchSouthernTerritories,
    gabon=CN.Gabon,
    gambia=CN.Gambia,
    georgia=CN.Georgia,
    germany=CN.Germany,
    ghana=CN.Ghana,
    gibraltar=CN.Gibraltar,
    greece=CN.Greece,
    greenland=CN.Greenland,
    grenada=CN.Grenada,
    guadeloupe=CN.Guadeloupe,
    guam=CN.Guam,
    guatemala=CN.Guatemala,
    guernsey=CN.Guernsey,
    guinea=CN.Guinea,
    guineabissau=CN.GuineaBissau,
    guyana=CN.Guyana,
    haiti=CN.Haiti,
    heard_and_mcdonald_islands=CN.HeardAndMcDonaldIslands,
    honduras=CN.Honduras,
    hongkong=CN.HongKong,
    hungary=CN.Hungary,
    iceland=CN.Iceland,
    india=CN.India,
    indonesia=CN.Indonesia,
    iran=CN.Iran,
    iraq=CN.Iraq,
    ireland=CN.Ireland,
    isle_of_man=CN.IsleOfMan,
    israel=CN.Israel,
    italy=CN.Italy,
    ivory_coast=CN.IvoryCoast,
    jamaica=CN.Jamaica,
    japan=CN.Japan,
    jersey=CN.Jersey,
    jordan=CN.Jordan,
    kazakhstan=CN.Kazakhstan,
    kenya=CN.Kenya,
    kiribati=CN.Kiribati,
    kosovo=CN.Kosovo,
    kuwait=CN.Kuwait,
    kyrgyzstan=CN.Kyrgyzstan,
    laos=CN.Laos,
    latin_america=CN.LatinAmerica,
    latvia=CN.Latvia,
    lebanon=CN.Lebanon,
    lesotho=CN.Lesotho,
    liberia=CN.Liberia,
    libya=CN.Libya,
    liechtenstein=CN.Liechtenstein,
    lithuania=CN.Lithuania,
    luxembourg=CN.Luxembourg,
    macau=CN.Macau,
    macedonia=CN.Macedonia,
    madagascar=CN.Madagascar,
    malawi=CN.Malawi,
    malaysia=CN.Malaysia,
    maldives=CN.Maldives,
    mali=CN.Mali,
    malta=CN.Malta,
    marshall_islands=CN.MarshallIslands,
    martinique=CN.Martinique,
    mauritania=CN.Mauritania,
    mauritius=CN.Mauritius,
    mayotte=CN.Mayotte,
    mexico=CN.Mexico,
    micronesia=CN.Micronesia,
    moldova=CN.Moldova,
    monaco=CN.Monaco,
    mongolia=CN.Mongolia,
    montenegro=CN.Montenegro,
    montserrat=CN.Montserrat,
    morocco=CN.Morocco,
    mozambique=CN.Mozambique,
    myanmar=CN.Myanmar,
    namibia=CN.Namibia,
    nauru_country=CN.NauruCountry,
    nepal=CN.Nepal,
    netherlands=CN.Netherlands,
    new_caledonia=CN.NewCaledonia,
    new_zealand=CN.NewZealand,
    nicaragua=CN.Nicaragua,
    niger=CN.Niger,
    nigeria=CN.Nigeria,
    niue=CN.Niue,
    norfolk_island=CN.NorfolkIsland,
    northern_mariana_islands=CN.NorthernMarianaIslands,
    north_korea=CN.NorthKorea,
    norway=CN.Norway,
    oman=CN.Oman,
    outlying_oceania=CN.OutlyingOceania,
    pakistan=CN.Pakistan,
    palau=CN.Palau,
    palestinian_territories=CN.PalestinianTerritories,
    panama=CN.Panama,
    papua_new_guinea=CN.PapuaNewGuinea,
    paraguay=CN.Paraguay,
    peru=CN.Peru,
    philippines=CN.Philippines,
    pitcairn=CN.Pitcairn,
    poland=CN.Poland,
    portugal=CN.Portugal,
    puertorico=CN.PuertoRico,
    qatar=CN.Qatar,
    reunion=CN.Reunion,
    romania=CN.Romania,
    russia=CN.Russia,
    rwanda=CN.Rwanda,
    saint_barthelemy=CN.SaintBarthelemy,
    saint_helena=CN.SaintHelena,
    saint_kitts_and_nevis=CN.SaintKittsAndNevis,
    saint_lucia=CN.SaintLucia,
    saint_martin=CN.SaintMartin,
    saint_pierre_and_miquelon=CN.SaintPierreAndMiquelon,
    saint_vincent_and_the_grenadines=CN.SaintVincentAndTheGrenadines,
    samoa=CN.Samoa,
    san_marino=CN.SanMarino,
    sao_tome_and_principe=CN.SaoTomeAndPrincipe,
    saudi_arabia=CN.SaudiArabia,
    senegal=CN.Senegal,
    serbia=CN.Serbia,
    seychelles=CN.Seychelles,
    sierra_leone=CN.SierraLeone,
    singapore=CN.Singapore,
    sint_maarten=CN.SintMaarten,
    slovakia=CN.Slovakia,
    slovenia=CN.Slovenia,
    solomon_islands=CN.SolomonIslands,
    somalia=CN.Somalia,
    south_africa=CN.SouthAfrica,
    south_georgia_and_south_sandwich_islands=CN.SouthGeorgiaAndTheSouthSandwichIslands,
    south_korea=CN.SouthKorea,
    south_sudan=CN.SouthSudan,
    spain=CN.Spain,
    sri_lanka=CN.SriLanka,
    sudan=CN.Sudan,
    suriname=CN.Suriname,
    svalbard_and_jan_mayen_islands=CN.SvalbardAndJanMayenIslands,
    swaziland=CN.Swaziland,
    sweden=CN.Sweden,
    switzerland=CN.Switzerland,
    syria=CN.Syria,
    taiwan=CN.Taiwan,
    tajikistan=CN.Tajikistan,
    tanzania=CN.Tanzania,
    thailand=CN.Thailand,
    togo=CN.Togo,
    tokelau_country=CN.TokelauCountry,
    tonga=CN.Tonga,
    trinidad_and_tobago=CN.TrinidadAndTobago,
    tristan_da_cunha=CN.TristanDaCunha,
    tunisia=CN.Tunisia,
    turkey=CN.Turkey,
    turkmenistan=CN.Turkmenistan,
    turks_and_caicos_islands=CN.TurksAndCaicosIslands,
    tuvalu_country=CN.TuvaluCountry,
    uganda=CN.Uganda,
    ukraine=CN.Ukraine,
    united_arabemirates=CN.UnitedArabEmirates,
    united_kingdom=CN.UnitedKingdom,
    united_states=CN.UnitedStates,
    united_states_minor_outlying_islands=CN.UnitedStatesMinorOutlyingIslands,
    united_states_virgin_islands=CN.UnitedStatesVirginIslands,
    uruguay=CN.Uruguay,
    uzbekistan=CN.Uzbekistan,
    vanuatu=CN.Vanuatu,
    vatican_city_state=CN.VaticanCityState,
    venezuela=CN.Venezuela,
    vietnam=CN.Vietnam,
    wallis_and_futuna_islands=CN.WallisAndFutunaIslands,
    western_sahara=CN.WesternSahara,
    world=CN.World,
    yemen=CN.Yemen,
    zambia=CN.Zambia,
    zimbabwe=CN.Zimbabwe,
)

LN = Loc.Language

LANGUAGE = bidict(
    any_language=LN.AnyLanguage,
    c=LN.C,
    abkhazian=LN.Abkhazian,
    afar=LN.Afar,
    afrikaans=LN.Afrikaans,
    aghem=LN.Aghem,
    akan=LN.Akan,
    akkadian=LN.Akkadian,
    akoose=LN.Akoose,
    albanian=LN.Albanian,
    american_sign_language=LN.AmericanSignLanguage,
    amharic=LN.Amharic,
    ancient_egyptian=LN.AncientEgyptian,
    ancient_greek=LN.AncientGreek,
    arabic=LN.Arabic,
    aragonese=LN.Aragonese,
    aramaic=LN.Aramaic,
    armenian=LN.Armenian,
    assamese=LN.Assamese,
    asturian=LN.Asturian,
    asu=LN.Asu,
    atsam=LN.Atsam,
    avaric=LN.Avaric,
    avestan=LN.Avestan,
    aymara=LN.Aymara,
    azerbaijani=LN.Azerbaijani,
    bafia=LN.Bafia,
    balinese=LN.Balinese,
    bambara=LN.Bambara,
    bamun=LN.Bamun,
    basaa=LN.Basaa,
    bashkir=LN.Bashkir,
    basque=LN.Basque,
    bataktoba=LN.BatakToba,
    belarusian=LN.Belarusian,
    bemba=LN.Bemba,
    bena=LN.Bena,
    bengali=LN.Bengali,
    bhojpuri=LN.Bhojpuri,
    bislama=LN.Bislama,
    blin=LN.Blin,
    bodo=LN.Bodo,
    bosnian=LN.Bosnian,
    breton=LN.Breton,
    buginese=LN.Buginese,
    bulgarian=LN.Bulgarian,
    burmese=LN.Burmese,
    cantonese=LN.Cantonese,
    catalan=LN.Catalan,
    cebuano=LN.Cebuano,
    central_kurdish=LN.CentralKurdish,
    central_morocco_tamazight=LN.CentralMoroccoTamazight,
    chakma=LN.Chakma,
    chamorro=LN.Chamorro,
    chechen=LN.Chechen,
    cherokee=LN.Cherokee,
    chickasaw=LN.Chickasaw,
    chiga=LN.Chiga,
    chinese=LN.Chinese,
    church=LN.Church,
    chuvash=LN.Chuvash,
    colognian=LN.Colognian,
    coptic=LN.Coptic,
    cornish=LN.Cornish,
    corsican=LN.Corsican,
    cree=LN.Cree,
    croatian=LN.Croatian,
    czech=LN.Czech,
    danish=LN.Danish,
    divehi=LN.Divehi,
    dogri=LN.Dogri,
    duala=LN.Duala,
    dutch=LN.Dutch,
    dzongkha=LN.Dzongkha,
    embu=LN.Embu,
    english=LN.English,
    erzya=LN.Erzya,
    esperanto=LN.Esperanto,
    estonian=LN.Estonian,
    ewe=LN.Ewe,
    ewondo=LN.Ewondo,
    faroese=LN.Faroese,
    fijian=LN.Fijian,
    filipino=LN.Filipino,
    finnish=LN.Finnish,
    french=LN.French,
    friulian=LN.Friulian,
    fulah=LN.Fulah,
    ga=LN.Ga,
    gaelic=LN.Gaelic,
    galician=LN.Galician,
    ganda=LN.Ganda,
    geez=LN.Geez,
    georgian=LN.Georgian,
    german=LN.German,
    gothic=LN.Gothic,
    greek=LN.Greek,
    greenlandic=LN.Greenlandic,
    guarani=LN.Guarani,
    gujarati=LN.Gujarati,
    gusii=LN.Gusii,
    haitian=LN.Haitian,
    hausa=LN.Hausa,
    hawaiian=LN.Hawaiian,
    hebrew=LN.Hebrew,
    herero=LN.Herero,
    hindi=LN.Hindi,
    hirimotu=LN.HiriMotu,
    hungarian=LN.Hungarian,
    icelandic=LN.Icelandic,
    ido=LN.Ido,
    igbo=LN.Igbo,
    inari_sami=LN.InariSami,
    indonesian=LN.Indonesian,
    ingush=LN.Ingush,
    interlingua=LN.Interlingua,
    interlingue=LN.Interlingue,
    inuktitut=LN.Inuktitut,
    inupiak=LN.Inupiak,
    irish=LN.Irish,
    italian=LN.Italian,
    japanese=LN.Japanese,
    javanese=LN.Javanese,
    jju=LN.Jju,
    jola_fonyi=LN.JolaFonyi,
    kabuverdianu=LN.Kabuverdianu,
    kabyle=LN.Kabyle,
    kako=LN.Kako,
    kalenjin=LN.Kalenjin,
    kamba=LN.Kamba,
    kannada=LN.Kannada,
    kanuri=LN.Kanuri,
    kashmiri=LN.Kashmiri,
    kazakh=LN.Kazakh,
    kenyang=LN.Kenyang,
    khmer=LN.Khmer,
    kiche=LN.Kiche,
    kikuyu=LN.Kikuyu,
    kinyarwanda=LN.Kinyarwanda,
    kirghiz=LN.Kirghiz,
    komi=LN.Komi,
    kongo=LN.Kongo,
    konkani=LN.Konkani,
    korean=LN.Korean,
    koro=LN.Koro,
    koyraboro_senni=LN.KoyraboroSenni,
    koyra_chiini=LN.KoyraChiini,
    kpelle=LN.Kpelle,
    kurdish=LN.Kurdish,
    kwanyama=LN.Kwanyama,
    kwasio=LN.Kwasio,
    lakota=LN.Lakota,
    langi=LN.Langi,
    lao=LN.Lao,
    latin=LN.Latin,
    latvian=LN.Latvian,
    lezghian=LN.Lezghian,
    limburgish=LN.Limburgish,
    lingala=LN.Lingala,
    literary_chinese=LN.LiteraryChinese,
    lithuanian=LN.Lithuanian,
    lojban=LN.Lojban,
    lower_sorbian=LN.LowerSorbian,
    low_german=LN.LowGerman,
    luba_katanga=LN.LubaKatanga,
    lule_sami=LN.LuleSami,
    luo=LN.Luo,
    luxembourgish=LN.Luxembourgish,
    luyia=LN.Luyia,
    macedonian=LN.Macedonian,
    machame=LN.Machame,
    maithili=LN.Maithili,
    makhuwa_meetto=LN.MakhuwaMeetto,
    makonde=LN.Makonde,
    malagasy=LN.Malagasy,
    malay=LN.Malay,
    malayalam=LN.Malayalam,
    maltese=LN.Maltese,
    mandingo=LN.Mandingo,
    manipuri=LN.Manipuri,
    manx=LN.Manx,
    maori=LN.Maori,
    mapuche=LN.Mapuche,
    marathi=LN.Marathi,
    marshallese=LN.Marshallese,
    masai=LN.Masai,
    mazanderani=LN.Mazanderani,
    mende=LN.Mende,
    meru=LN.Meru,
    meta=LN.Meta,
    mohawk=LN.Mohawk,
    mongolian=LN.Mongolian,
    morisyen=LN.Morisyen,
    mundang=LN.Mundang,
    muscogee=LN.Muscogee,
    nama=LN.Nama,
    nauru_language=LN.NauruLanguage,
    navaho=LN.Navaho,
    ndonga=LN.Ndonga,
    nepali=LN.Nepali,
    newari=LN.Newari,
    ngiemboon=LN.Ngiemboon,
    ngomba=LN.Ngomba,
    nko=LN.Nko,
    northern_luri=LN.NorthernLuri,
    northern_sami=LN.NorthernSami,
    northern_sotho=LN.NorthernSotho,
    north_ndebele=LN.NorthNdebele,
    norwegian_bokmal=LN.NorwegianBokmal,
    norwegian_nynorsk=LN.NorwegianNynorsk,
    nuer=LN.Nuer,
    nyanja=LN.Nyanja,
    nyankole=LN.Nyankole,
    occitan=LN.Occitan,
    ojibwa=LN.Ojibwa,
    old_irish=LN.OldIrish,
    old_norse=LN.OldNorse,
    old_persian=LN.OldPersian,
    oriya=LN.Oriya,
    oromo=LN.Oromo,
    osage=LN.Osage,
    ossetic=LN.Ossetic,
    pahlavi=LN.Pahlavi,
    palauan=LN.Palauan,
    pali=LN.Pali,
    papiamento=LN.Papiamento,
    pashto=LN.Pashto,
    persian=LN.Persian,
    phoenician=LN.Phoenician,
    polish=LN.Polish,
    portuguese=LN.Portuguese,
    prussian=LN.Prussian,
    punjabi=LN.Punjabi,
    quechua=LN.Quechua,
    romanian=LN.Romanian,
    romansh=LN.Romansh,
    rombo=LN.Rombo,
    rundi=LN.Rundi,
    russian=LN.Russian,
    rwa=LN.Rwa,
    saho=LN.Saho,
    sakha=LN.Sakha,
    samburu=LN.Samburu,
    samoan=LN.Samoan,
    sango=LN.Sango,
    sangu=LN.Sangu,
    sanskrit=LN.Sanskrit,
    santali=LN.Santali,
    sardinian=LN.Sardinian,
    saurashtra=LN.Saurashtra,
    sena=LN.Sena,
    serbian=LN.Serbian,
    shambala=LN.Shambala,
    shona=LN.Shona,
    sichuanyi=LN.SichuanYi,
    sicilian=LN.Sicilian,
    sidamo=LN.Sidamo,
    silesian=LN.Silesian,
    sindhi=LN.Sindhi,
    sinhala=LN.Sinhala,
    skoltsami=LN.SkoltSami,
    slovak=LN.Slovak,
    slovenian=LN.Slovenian,
    soga=LN.Soga,
    somali=LN.Somali,
    southern_kurdish=LN.SouthernKurdish,
    southern_sami=LN.SouthernSami,
    southern_sotho=LN.SouthernSotho,
    south_ndebele=LN.SouthNdebele,
    spanish=LN.Spanish,
    standard_moroccan_tamazight=LN.StandardMoroccanTamazight,
    sundanese=LN.Sundanese,
    swahili=LN.Swahili,
    swati=LN.Swati,
    swedish=LN.Swedish,
    swiss_german=LN.SwissGerman,
    syriac=LN.Syriac,
    tachelhit=LN.Tachelhit,
    tahitian=LN.Tahitian,
    taidam=LN.TaiDam,
    taita=LN.Taita,
    tajik=LN.Tajik,
    tamil=LN.Tamil,
    taroko=LN.Taroko,
    tasawaq=LN.Tasawaq,
    tatar=LN.Tatar,
    telugu=LN.Telugu,
    teso=LN.Teso,
    thai=LN.Thai,
    tibetan=LN.Tibetan,
    tigre=LN.Tigre,
    tigrinya=LN.Tigrinya,
    tokelau_language=LN.TokelauLanguage,
    tokpisin=LN.TokPisin,
    tongan=LN.Tongan,
    tsonga=LN.Tsonga,
    tswana=LN.Tswana,
    turkish=LN.Turkish,
    turkmen=LN.Turkmen,
    tuvalu_language=LN.TuvaluLanguage,
    tyap=LN.Tyap,
    ugaritic=LN.Ugaritic,
    uighur=LN.Uighur,
    ukrainian=LN.Ukrainian,
    upper_sorbian=LN.UpperSorbian,
    urdu=LN.Urdu,
    uzbek=LN.Uzbek,
    vai=LN.Vai,
    venda=LN.Venda,
    vietnamese=LN.Vietnamese,
    volapuk=LN.Volapuk,
    vunjo=LN.Vunjo,
    walamo=LN.Walamo,
    walloon=LN.Walloon,
    walser=LN.Walser,
    warlpiri=LN.Warlpiri,
    welsh=LN.Welsh,
    western_balochi=LN.WesternBalochi,
    western_frisian=LN.WesternFrisian,
    wolof=LN.Wolof,
    xhosa=LN.Xhosa,
    yangben=LN.Yangben,
    yiddish=LN.Yiddish,
    yoruba=LN.Yoruba,
    zarma=LN.Zarma,
    zhuang=LN.Zhuang,
    zulu=LN.Zulu,
)

FormatTypeStr = Literal["long", "short", "narrow"]

FORMAT_TYPE: bidict[FormatTypeStr, QtCore.QLocale.FormatType] = bidict(
    long=QtCore.QLocale.FormatType.LongFormat,
    short=QtCore.QLocale.FormatType.ShortFormat,
    narrow=QtCore.QLocale.FormatType.NarrowFormat,
)

MeasurementSystemStr = Literal["metric", "imperial_us", "imperial_uk"]

MEASUREMENT_SYSTEM: bidict[MeasurementSystemStr, QtCore.QLocale.MeasurementSystem] = (
    bidict(
        metric=QtCore.QLocale.MeasurementSystem.MetricSystem,
        imperial_us=QtCore.QLocale.MeasurementSystem.ImperialUSSystem,
        imperial_uk=QtCore.QLocale.MeasurementSystem.ImperialUKSystem,
    )
)

DataSizeFormatStr = Literal["iec", "traditional", "si"]

DATA_SIZE_FORMAT: bidict[DataSizeFormatStr, QtCore.QLocale.DataSizeIecFormat] = bidict(
    iec=QtCore.QLocale.DataSizeFormat.DataSizeIecFormat,
    traditional=QtCore.QLocale.DataSizeFormat.DataSizeTraditionalFormat,
    si=QtCore.QLocale.DataSizeFormat.DataSizeSIFormat,
)

NumberOptionStr = Literal[
    "default",
    "omit_group_separator",
    "reject_group_separator",
    "omit_leading_zero_in_exponent",
    "reject_leading_zero_in_exponent",
    "include_trailing_zeroes_after_dot",
    "reject_trailing_zeroes_after_dot",
]

NO = QtCore.QLocale.NumberOption
NUMBER_OPTION: bidict[NumberOptionStr, NO] = bidict(
    default=NO.DefaultNumberOptions,
    omit_group_separator=NO.OmitGroupSeparator,
    reject_group_separator=NO.RejectGroupSeparator,
    omit_leading_zero_in_exponent=NO.OmitLeadingZeroInExponent,
    reject_leading_zero_in_exponent=NO.RejectLeadingZeroInExponent,
    include_trailing_zeroes_after_dot=NO.IncludeTrailingZeroesAfterDot,
    reject_trailing_zeroes_after_dot=NO.RejectTrailingZeroesAfterDot,
)

OFFSET = ord("🇦") - ord("A")


class Locale(QtCore.QLocale):
    """Converts between numbers and their string representations in various languages."""

    def __repr__(self):
        return get_repr(self, self.bcp47Name())

    def __reduce__(self):
        return type(self), (self.bcp47Name(),)

    def get_flag_unicode(self):
        name = self.name().split("_")[1]
        name = [c for c in name.lower() if c.isalnum()]
        return "".join([chr(ord(c.upper()) + OFFSET) for c in name])

    @classmethod
    def get_system_locale(cls) -> Self:
        return cls(cls.system())

    @classmethod
    def get_c_locale(cls) -> Self:
        return cls(cls.c())

    @classmethod
    def get_system_language(cls) -> str:
        return cls.get_system_locale().uiLanguages()[0]

    def get_country(self):
        return COUNTRY.inverse[self.country()]

    def get_measurement_system(self) -> MeasurementSystemStr:
        return MEASUREMENT_SYSTEM.inverse[self.measurementSystem()]

    def get_formatted_data_size(
        self, size: int, precision: int = 2, fmt: DataSizeFormatStr = "iec"
    ) -> str:
        if size < 0:
            return ""
        return self.formattedDataSize(size, precision, DATA_SIZE_FORMAT[fmt])

    def get_first_day_of_week(self) -> constants.DayOfWeekStr:
        return constants.DAY_OF_WEEK.inverse[self.firstDayOfWeek()]

    def get_text_direction(self) -> constants.LayoutDirectionStr:
        return constants.LAYOUT_DIRECTION.inverse[self.textDirection()]

    def get_weekdays(self) -> list[constants.DayOfWeekStr]:
        return [constants.DAY_OF_WEEK.inverse[i] for i in self.weekdays()]

    def get_day_name(self, day: int, format_type: FormatTypeStr = "long") -> str:
        return self.dayName(day, FORMAT_TYPE[format_type])

    def get_month_name(self, month: int, format_type: FormatTypeStr = "long") -> str:
        return self.monthName(month, FORMAT_TYPE[format_type])

    def get_standalone_day_name(
        self, day: int, format_type: FormatTypeStr = "long"
    ) -> str:
        return self.standaloneDayName(day, FORMAT_TYPE[format_type])

    def get_time_format(self, format_type: FormatTypeStr = "long") -> str:
        return self.timeFormat(FORMAT_TYPE[format_type])

    def get_date_format(self, format_type: FormatTypeStr = "long") -> str:
        return self.dateFormat(FORMAT_TYPE[format_type])

    def get_datetime_format(self, format_type: FormatTypeStr = "long") -> str:
        return self.dateTimeFormat(FORMAT_TYPE[format_type])

    def to_datetime(
        self, text: str, format_type: FormatTypeStr | str = "long"
    ) -> QtCore.QDateTime:
        if format_type in {"long", "short", "narrow"}:
            format_type = FORMAT_TYPE[format_type]
        return self.toDateTime(text, format_type)

    def to_date(
        self, text: str, format_type: FormatTypeStr | str = "long"
    ) -> QtCore.QDate:
        if format_type in {"long", "short", "narrow"}:
            format_type = FORMAT_TYPE[format_type]
        return self.toDate(text, format_type)

    def to_time(
        self, text: str, format_type: FormatTypeStr | str = "long"
    ) -> QtCore.QTime:
        if format_type in {"long", "short", "narrow"}:
            format_type = FORMAT_TYPE[format_type]
        return self.to_time(text, format_type)

    def get_standalone_month_name(
        self, month: int, format_type: FormatTypeStr = "long"
    ) -> str:
        return self.standaloneMonthName(month, FORMAT_TYPE[format_type])

    def quote_string(self, string: str, alternate_style: bool = False) -> str:
        flag = (
            self.QuotationStyle.AlternateQuotation
            if alternate_style
            else self.QuotationStyle.StandardQuotation
        )
        return self.quoteString(string, flag)

    @classmethod
    def get_all_locales(cls) -> list[Self]:
        return [
            cls(i)
            for i in cls.matchingLocales(
                cls.Language.AnyLanguage, cls.Script.AnyScript, cls.Country.AnyCountry
            )
        ]


if __name__ == "__main__":
    from prettyqt import gui, widgets

    app = widgets.app()
    locale = Locale.get_all_locales()[100].get_flag_unicode()
    p = gui.Pixmap.create_char(locale, 64)
    w = widgets.Label()
    w.set_pixmap(p)
    w.show()
    app.exec()
