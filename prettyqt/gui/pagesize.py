from typing import Literal

from qtpy import QtGui

from prettyqt.utils import bidict


PAGE_SIZE_ID = bidict(
    a0=QtGui.QPageSize.A0,
    a1=QtGui.QPageSize.A1,
    a2=QtGui.QPageSize.A2,
    a3=QtGui.QPageSize.A3,
    a4=QtGui.QPageSize.A4,
    a5=QtGui.QPageSize.A5,
    a6=QtGui.QPageSize.A6,
    a7=QtGui.QPageSize.A7,
    a8=QtGui.QPageSize.A8,
    a9=QtGui.QPageSize.A9,
    b0=QtGui.QPageSize.B0,
    b1=QtGui.QPageSize.B1,
    b2=QtGui.QPageSize.B2,
    b3=QtGui.QPageSize.B3,
    b4=QtGui.QPageSize.B4,
    b5=QtGui.QPageSize.B5,
    b6=QtGui.QPageSize.B6,
    b7=QtGui.QPageSize.B7,
    b8=QtGui.QPageSize.B8,
    b9=QtGui.QPageSize.B9,
    b10=QtGui.QPageSize.B10,
    c5e=QtGui.QPageSize.C5E,
    comm_10e=QtGui.QPageSize.Comm10E,
    dle=QtGui.QPageSize.DLE,
    executive=QtGui.QPageSize.Executive,
    folio=QtGui.QPageSize.Folio,
    ledger=QtGui.QPageSize.Ledger,
    legal=QtGui.QPageSize.Legal,
    letter=QtGui.QPageSize.Letter,
    tabloid=QtGui.QPageSize.Tabloid,
    custom=QtGui.QPageSize.Custom,
    a10=QtGui.QPageSize.A10,
    a3_extra=QtGui.QPageSize.A3Extra,
    a4_extra=QtGui.QPageSize.A4Extra,
    a4_plus=QtGui.QPageSize.A4Plus,
    a4_small=QtGui.QPageSize.A4Small,
    a5_extra=QtGui.QPageSize.A5Extra,
    b5_extra=QtGui.QPageSize.B5Extra,
    jis_b0=QtGui.QPageSize.JisB0,
    jis_b1=QtGui.QPageSize.JisB1,
    jis_b2=QtGui.QPageSize.JisB2,
    jis_b3=QtGui.QPageSize.JisB3,
    jis_b4=QtGui.QPageSize.JisB4,
    jis_b5=QtGui.QPageSize.JisB5,
    jis_b6=QtGui.QPageSize.JisB6,
    jis_b7=QtGui.QPageSize.JisB7,
    jis_b8=QtGui.QPageSize.JisB8,
    jis_b9=QtGui.QPageSize.JisB9,
    jis_b10=QtGui.QPageSize.JisB10,
    # c5e=QtGui.QPageSize.AnsiA, Letter
    # c5e=QtGui.QPageSize.AnsiB, Ledger
    ansi_c=QtGui.QPageSize.AnsiC,
    ansi_d=QtGui.QPageSize.AnsiD,
    ansi_e=QtGui.QPageSize.AnsiE,
    legal_extra=QtGui.QPageSize.LegalExtra,
    letter_extra=QtGui.QPageSize.LetterExtra,
    letter_plus=QtGui.QPageSize.LetterPlus,
    letter_small=QtGui.QPageSize.LetterSmall,
    tabloid_extra=QtGui.QPageSize.TabloidExtra,
    arch_a=QtGui.QPageSize.ArchA,
    arch_b=QtGui.QPageSize.ArchB,
    arch_c=QtGui.QPageSize.ArchC,
    arch_d=QtGui.QPageSize.ArchD,
    arch_e=QtGui.QPageSize.ArchE,
    imperial_7x9=QtGui.QPageSize.Imperial7x9,
    imperial_8x10=QtGui.QPageSize.Imperial8x10,
    imperial_9x11=QtGui.QPageSize.Imperial9x11,
    imperial_9x12=QtGui.QPageSize.Imperial9x12,
    imperial_10x11=QtGui.QPageSize.Imperial10x11,
    imperial_10x13=QtGui.QPageSize.Imperial10x13,
    imperial_10x14=QtGui.QPageSize.Imperial10x14,
    imperial_12x11=QtGui.QPageSize.Imperial12x11,
    imperial_15x11=QtGui.QPageSize.Imperial15x11,
    executive_standard=QtGui.QPageSize.ExecutiveStandard,
    note=QtGui.QPageSize.Note,
    quarto=QtGui.QPageSize.Quarto,
    statement=QtGui.QPageSize.Statement,
    super_a=QtGui.QPageSize.SuperA,
    super_b=QtGui.QPageSize.SuperB,
    postcard=QtGui.QPageSize.Postcard,
    double_postcard=QtGui.QPageSize.DoublePostcard,
    prc_16_k=QtGui.QPageSize.Prc16K,
    prc_32_k=QtGui.QPageSize.Prc32K,
    prc_32_k_big=QtGui.QPageSize.Prc32KBig,
    fan_fold_us=QtGui.QPageSize.FanFoldUS,
    fan_fold_german=QtGui.QPageSize.FanFoldGerman,
    fan_fold_german_legal=QtGui.QPageSize.FanFoldGermanLegal,
    envelope_b4=QtGui.QPageSize.EnvelopeB4,
    envelope_b5=QtGui.QPageSize.EnvelopeB5,
    envelope_b6=QtGui.QPageSize.EnvelopeB6,
    envelope_c0=QtGui.QPageSize.EnvelopeC0,
    envelope_c1=QtGui.QPageSize.EnvelopeC1,
    envelope_c2=QtGui.QPageSize.EnvelopeC2,
    envelope_c3=QtGui.QPageSize.EnvelopeC3,
    envelope_c4=QtGui.QPageSize.EnvelopeC4,
    # envelope_c5=QtGui.QPageSize.EnvelopeC5, c5e
    envelope_c6=QtGui.QPageSize.EnvelopeC6,
    envelope_c65=QtGui.QPageSize.EnvelopeC65,
    envelope_c7=QtGui.QPageSize.EnvelopeC7,
    # envelope_dl=QtGui.QPageSize.EnvelopeDL, dle
    envelope_9=QtGui.QPageSize.Envelope9,
    # envelope_10=QtGui.QPageSize.Envelope10, comm10e
    envelope_11=QtGui.QPageSize.Envelope11,
    envelope_12=QtGui.QPageSize.Envelope12,
    envelope_14=QtGui.QPageSize.Envelope14,
    envelope_monarch=QtGui.QPageSize.EnvelopeMonarch,
    envelope_personal=QtGui.QPageSize.EnvelopePersonal,
    envelope_chou_3=QtGui.QPageSize.EnvelopeChou3,
    envelope_chou_4=QtGui.QPageSize.EnvelopeChou4,
    envelope_invite=QtGui.QPageSize.EnvelopeInvite,
    envelope_italian=QtGui.QPageSize.EnvelopeItalian,
    envelope_kaku_2=QtGui.QPageSize.EnvelopeKaku2,
    envelope_kaku_3=QtGui.QPageSize.EnvelopeKaku3,
    envelope_prc_1=QtGui.QPageSize.EnvelopePrc1,
    envelope_prc_2=QtGui.QPageSize.EnvelopePrc2,
    envelope_prc_3=QtGui.QPageSize.EnvelopePrc3,
    envelope_prc_4=QtGui.QPageSize.EnvelopePrc4,
    envelope_prc_5=QtGui.QPageSize.EnvelopePrc5,
    envelope_prc_6=QtGui.QPageSize.EnvelopePrc6,
    envelope_prc_7=QtGui.QPageSize.EnvelopePrc7,
    envelope_prc_8=QtGui.QPageSize.EnvelopePrc8,
    envelope_prc_9=QtGui.QPageSize.EnvelopePrc9,
    envelope_prc_10=QtGui.QPageSize.EnvelopePrc10,
    envelope_you_4=QtGui.QPageSize.EnvelopeYou4,
    # last_page_size=QtGui.QPageSize.LastPageSize, envelope_you_4
)

SIZE_MATCH_POLICY = bidict(
    fuzzy=QtGui.QPageSize.FuzzyMatch,
    fuzzy_orientation=QtGui.QPageSize.FuzzyOrientationMatch,
    exact=QtGui.QPageSize.ExactMatch,
)

UNITS = bidict(
    millimeter=QtGui.QPageSize.Millimeter,
    point=QtGui.QPageSize.Point,
    inch=QtGui.QPageSize.Inch,
    pica=QtGui.QPageSize.Pica,
    didot=QtGui.QPageSize.Didot,
    cicero=QtGui.QPageSize.Cicero,
)

UnitStr = Literal["millimeter", "point", "inch", "pica", "didot", "cicero"]


class PageSize(QtGui.QPageSize):
    def __repr__(self):
        return f"{self.__class__.__name__}({self.get_id()!r})"

    def __reduce__(self):
        return self.__class__, (self.id(),)

    def get_definition_units(self) -> UnitStr:
        """Get the definition unit.

        Returns:
            unit
        """
        units = self.definitionUnits()
        if units == -1:
            raise ValueError("Invalid page size")
        return UNITS.inverse[units]

    def get_id(self) -> str:
        """Get the standard page size id.

        Returns:
            page size id
        """
        return PAGE_SIZE_ID.inverse[self.id()]


if __name__ == "__main__":
    size = PageSize()
    print(repr(size))
