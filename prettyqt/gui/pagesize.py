from __future__ import annotations

from typing import Literal

from prettyqt import qt
from prettyqt.qt import QtGui
from prettyqt.utils import bidict


PAGE_SIZE_ID = bidict(
    a0=QtGui.QPageSize.PageSizeId.A0,
    a1=QtGui.QPageSize.PageSizeId.A1,
    a2=QtGui.QPageSize.PageSizeId.A2,
    a3=QtGui.QPageSize.PageSizeId.A3,
    a4=QtGui.QPageSize.PageSizeId.A4,
    a5=QtGui.QPageSize.PageSizeId.A5,
    a6=QtGui.QPageSize.PageSizeId.A6,
    a7=QtGui.QPageSize.PageSizeId.A7,
    a8=QtGui.QPageSize.PageSizeId.A8,
    a9=QtGui.QPageSize.PageSizeId.A9,
    b0=QtGui.QPageSize.PageSizeId.B0,
    b1=QtGui.QPageSize.PageSizeId.B1,
    b2=QtGui.QPageSize.PageSizeId.B2,
    b3=QtGui.QPageSize.PageSizeId.B3,
    b4=QtGui.QPageSize.PageSizeId.B4,
    b5=QtGui.QPageSize.PageSizeId.B5,
    b6=QtGui.QPageSize.PageSizeId.B6,
    b7=QtGui.QPageSize.PageSizeId.B7,
    b8=QtGui.QPageSize.PageSizeId.B8,
    b9=QtGui.QPageSize.PageSizeId.B9,
    b10=QtGui.QPageSize.PageSizeId.B10,
    c5e=QtGui.QPageSize.PageSizeId.C5E,
    comm_10e=QtGui.QPageSize.PageSizeId.Comm10E,
    dle=QtGui.QPageSize.PageSizeId.DLE,
    executive=QtGui.QPageSize.PageSizeId.Executive,
    folio=QtGui.QPageSize.PageSizeId.Folio,
    ledger=QtGui.QPageSize.PageSizeId.Ledger,
    legal=QtGui.QPageSize.PageSizeId.Legal,
    letter=QtGui.QPageSize.PageSizeId.Letter,
    tabloid=QtGui.QPageSize.PageSizeId.Tabloid,
    custom=QtGui.QPageSize.PageSizeId.Custom,
    a10=QtGui.QPageSize.PageSizeId.A10,
    a3_extra=QtGui.QPageSize.PageSizeId.A3Extra,
    a4_extra=QtGui.QPageSize.PageSizeId.A4Extra,
    a4_plus=QtGui.QPageSize.PageSizeId.A4Plus,
    a4_small=QtGui.QPageSize.PageSizeId.A4Small,
    a5_extra=QtGui.QPageSize.PageSizeId.A5Extra,
    b5_extra=QtGui.QPageSize.PageSizeId.B5Extra,
    jis_b0=QtGui.QPageSize.PageSizeId.JisB0,
    jis_b1=QtGui.QPageSize.PageSizeId.JisB1,
    jis_b2=QtGui.QPageSize.PageSizeId.JisB2,
    jis_b3=QtGui.QPageSize.PageSizeId.JisB3,
    jis_b4=QtGui.QPageSize.PageSizeId.JisB4,
    jis_b5=QtGui.QPageSize.PageSizeId.JisB5,
    jis_b6=QtGui.QPageSize.PageSizeId.JisB6,
    jis_b7=QtGui.QPageSize.PageSizeId.JisB7,
    jis_b8=QtGui.QPageSize.PageSizeId.JisB8,
    jis_b9=QtGui.QPageSize.PageSizeId.JisB9,
    jis_b10=QtGui.QPageSize.PageSizeId.JisB10,
    # c5e=QtGui.QPageSize.PageSizeId.AnsiA, Letter
    # c5e=QtGui.QPageSize.PageSizeId.AnsiB, Ledger
    ansi_c=QtGui.QPageSize.PageSizeId.AnsiC,
    ansi_d=QtGui.QPageSize.PageSizeId.AnsiD,
    ansi_e=QtGui.QPageSize.PageSizeId.AnsiE,
    legal_extra=QtGui.QPageSize.PageSizeId.LegalExtra,
    letter_extra=QtGui.QPageSize.PageSizeId.LetterExtra,
    letter_plus=QtGui.QPageSize.PageSizeId.LetterPlus,
    letter_small=QtGui.QPageSize.PageSizeId.LetterSmall,
    tabloid_extra=QtGui.QPageSize.PageSizeId.TabloidExtra,
    arch_a=QtGui.QPageSize.PageSizeId.ArchA,
    arch_b=QtGui.QPageSize.PageSizeId.ArchB,
    arch_c=QtGui.QPageSize.PageSizeId.ArchC,
    arch_d=QtGui.QPageSize.PageSizeId.ArchD,
    arch_e=QtGui.QPageSize.PageSizeId.ArchE,
    imperial_7x9=QtGui.QPageSize.PageSizeId.Imperial7x9,
    imperial_8x10=QtGui.QPageSize.PageSizeId.Imperial8x10,
    imperial_9x11=QtGui.QPageSize.PageSizeId.Imperial9x11,
    imperial_9x12=QtGui.QPageSize.PageSizeId.Imperial9x12,
    imperial_10x11=QtGui.QPageSize.PageSizeId.Imperial10x11,
    imperial_10x13=QtGui.QPageSize.PageSizeId.Imperial10x13,
    imperial_10x14=QtGui.QPageSize.PageSizeId.Imperial10x14,
    imperial_12x11=QtGui.QPageSize.PageSizeId.Imperial12x11,
    imperial_15x11=QtGui.QPageSize.PageSizeId.Imperial15x11,
    executive_standard=QtGui.QPageSize.PageSizeId.ExecutiveStandard,
    note=QtGui.QPageSize.PageSizeId.Note,
    quarto=QtGui.QPageSize.PageSizeId.Quarto,
    statement=QtGui.QPageSize.PageSizeId.Statement,
    super_a=QtGui.QPageSize.PageSizeId.SuperA,
    super_b=QtGui.QPageSize.PageSizeId.SuperB,
    postcard=QtGui.QPageSize.PageSizeId.Postcard,
    double_postcard=QtGui.QPageSize.PageSizeId.DoublePostcard,
    prc_16_k=QtGui.QPageSize.PageSizeId.Prc16K,
    prc_32_k=QtGui.QPageSize.PageSizeId.Prc32K,
    prc_32_k_big=QtGui.QPageSize.PageSizeId.Prc32KBig,
    fan_fold_us=QtGui.QPageSize.PageSizeId.FanFoldUS,
    fan_fold_german=QtGui.QPageSize.PageSizeId.FanFoldGerman,
    fan_fold_german_legal=QtGui.QPageSize.PageSizeId.FanFoldGermanLegal,
    envelope_b4=QtGui.QPageSize.PageSizeId.EnvelopeB4,
    envelope_b5=QtGui.QPageSize.PageSizeId.EnvelopeB5,
    envelope_b6=QtGui.QPageSize.PageSizeId.EnvelopeB6,
    envelope_c0=QtGui.QPageSize.PageSizeId.EnvelopeC0,
    envelope_c1=QtGui.QPageSize.PageSizeId.EnvelopeC1,
    envelope_c2=QtGui.QPageSize.PageSizeId.EnvelopeC2,
    envelope_c3=QtGui.QPageSize.PageSizeId.EnvelopeC3,
    envelope_c4=QtGui.QPageSize.PageSizeId.EnvelopeC4,
    # envelope_c5=QtGui.QPageSize.PageSizeId.EnvelopeC5, c5e
    envelope_c6=QtGui.QPageSize.PageSizeId.EnvelopeC6,
    envelope_c65=QtGui.QPageSize.PageSizeId.EnvelopeC65,
    envelope_c7=QtGui.QPageSize.PageSizeId.EnvelopeC7,
    # envelope_dl=QtGui.QPageSize.PageSizeId.EnvelopeDL, dle
    envelope_9=QtGui.QPageSize.PageSizeId.Envelope9,
    # envelope_10=QtGui.QPageSize.PageSizeId.Envelope10, comm10e
    envelope_11=QtGui.QPageSize.PageSizeId.Envelope11,
    envelope_12=QtGui.QPageSize.PageSizeId.Envelope12,
    envelope_14=QtGui.QPageSize.PageSizeId.Envelope14,
    envelope_monarch=QtGui.QPageSize.PageSizeId.EnvelopeMonarch,
    envelope_personal=QtGui.QPageSize.PageSizeId.EnvelopePersonal,
    envelope_chou_3=QtGui.QPageSize.PageSizeId.EnvelopeChou3,
    envelope_chou_4=QtGui.QPageSize.PageSizeId.EnvelopeChou4,
    envelope_invite=QtGui.QPageSize.PageSizeId.EnvelopeInvite,
    envelope_italian=QtGui.QPageSize.PageSizeId.EnvelopeItalian,
    envelope_kaku_2=QtGui.QPageSize.PageSizeId.EnvelopeKaku2,
    envelope_kaku_3=QtGui.QPageSize.PageSizeId.EnvelopeKaku3,
    envelope_prc_1=QtGui.QPageSize.PageSizeId.EnvelopePrc1,
    envelope_prc_2=QtGui.QPageSize.PageSizeId.EnvelopePrc2,
    envelope_prc_3=QtGui.QPageSize.PageSizeId.EnvelopePrc3,
    envelope_prc_4=QtGui.QPageSize.PageSizeId.EnvelopePrc4,
    envelope_prc_5=QtGui.QPageSize.PageSizeId.EnvelopePrc5,
    envelope_prc_6=QtGui.QPageSize.PageSizeId.EnvelopePrc6,
    envelope_prc_7=QtGui.QPageSize.PageSizeId.EnvelopePrc7,
    envelope_prc_8=QtGui.QPageSize.PageSizeId.EnvelopePrc8,
    envelope_prc_9=QtGui.QPageSize.PageSizeId.EnvelopePrc9,
    envelope_prc_10=QtGui.QPageSize.PageSizeId.EnvelopePrc10,
    envelope_you_4=QtGui.QPageSize.PageSizeId.EnvelopeYou4,
    # last_page_size=QtGui.QPageSize.PageSizeId.LastPageSize, envelope_you_4
)

SIZE_MATCH_POLICY = bidict(
    fuzzy=QtGui.QPageSize.SizeMatchPolicy.FuzzyMatch,
    fuzzy_orientation=QtGui.QPageSize.SizeMatchPolicy.FuzzyOrientationMatch,
    exact=QtGui.QPageSize.SizeMatchPolicy.ExactMatch,
)

UNITS = bidict(
    millimeter=QtGui.QPageSize.Unit.Millimeter,
    point=QtGui.QPageSize.Unit.Point,
    inch=QtGui.QPageSize.Unit.Inch,
    pica=QtGui.QPageSize.Unit.Pica,
    didot=QtGui.QPageSize.Unit.Didot,
    cicero=QtGui.QPageSize.Unit.Cicero,
)

UnitStr = Literal["millimeter", "point", "inch", "pica", "didot", "cicero"]


class PageSize(QtGui.QPageSize):
    def __repr__(self):
        return f"{type(self).__name__}({self.get_id()!r})"

    def __reduce__(self):
        return type(self), (self.id(),)

    def get_definition_units(self) -> UnitStr:
        """Get the definition unit.

        Returns:
            unit
        """
        units = self.definitionUnits()
        if qt.flag_to_int(units) == -1:
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
