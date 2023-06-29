from __future__ import annotations

import datetime

from typing import Literal

from prettyqt import constants, core, widgets
from prettyqt.utils import bidict, datatypes


SectionStr = Literal[
    "none",
    "am_pm",
    "msec",
    "second",
    "minute",
    "hour",
    "day",
    "month",
    "year",
]

SECTIONS: bidict[SectionStr, widgets.QDateTimeEdit.Section] = bidict(
    none=widgets.QDateTimeEdit.Section.NoSection,
    am_pm=widgets.QDateTimeEdit.Section.AmPmSection,
    msec=widgets.QDateTimeEdit.Section.MSecSection,
    second=widgets.QDateTimeEdit.Section.SecondSection,
    minute=widgets.QDateTimeEdit.Section.MinuteSection,
    hour=widgets.QDateTimeEdit.Section.HourSection,
    day=widgets.QDateTimeEdit.Section.DaySection,
    month=widgets.QDateTimeEdit.Section.MonthSection,
    year=widgets.QDateTimeEdit.Section.YearSection,
)


class DateTimeEditMixin(widgets.AbstractSpinBoxMixin):
    value_changed = core.Signal(datetime.datetime)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCalendarPopup(True)
        self.dateTimeChanged.connect(self.datetime_changed)

    def _get_map(self):
        maps = super()._get_map()
        maps |= {
            "timeSpec": constants.TIME_SPEC,
            "currentSection": SECTIONS,
        }
        return maps

    def datetime_changed(self, date):
        dt = self.get_datetime()
        self.value_changed.emit(dt)

    def set_to_today(self):
        self.setDateTime(core.DateTime.currentDateTime())

    def get_section_text(
        self, section: SectionStr | widgets.QDateTimeEdit.Section
    ) -> str:
        return self.sectionText(SECTIONS.get_enum_value(section))

    def get_current_section(self) -> SectionStr:
        return SECTIONS.inverse[self.currentSection()]

    def set_current_section(self, section: SectionStr | widgets.QDateTimeEdit.Section):
        self.setCurrentSection(SECTIONS.get_enum_value(section))

    def get_displayed_sections(self) -> list[SectionStr]:
        return SECTIONS.get_list(self.displayedSections())

    def set_range(
        self,
        lower: datatypes.DateTimeType,
        upper: datatypes.DateTimeType,
    ):
        lower = datatypes.to_datetime(lower)
        upper = datatypes.to_datetime(upper)
        self.setToolTip(f"{lower} <= x <= {upper}")
        self.setDateTimeRange(lower, upper)

    def set_format(self, fmt: str):
        self.setDisplayFormat(fmt)

    def get_value(self) -> datetime.datetime:
        return self.get_datetime()

    def set_value(self, value: datetime.datetime | core.DateTime):
        self.setDateTime(value)

    def get_datetime(self) -> datetime.datetime:
        return self.dateTime().toPython()  # type: ignore

    def min_datetime(self) -> datetime.datetime:
        return self.minimumDateTime().toPython()  # type: ignore

    def max_datetime(self) -> datetime.datetime:
        return self.maximumDateTime().toPython()  # type: ignore

    def min_date(self) -> datetime.date:
        return self.minimumDate().toPython()  # type: ignore

    def max_date(self) -> datetime.date:
        return self.maximumDate().toPython()  # type: ignore

    def get_date(self) -> datetime.date:
        return self.date().toPython()  # type: ignore

    def min_time(self) -> datetime.time:
        return self.minimumTime().toPython()  # type: ignore

    def max_time(self) -> datetime.time:
        return self.maximumTime().toPython()  # type: ignore

    def get_time(self) -> datetime.time:
        return self.time().toPython()  # type: ignore


class DateTimeEdit(DateTimeEditMixin, widgets.QDateTimeEdit):
    pass


if __name__ == "__main__":
    app = widgets.app()
    widget = DateTimeEdit()
    widget.show()
    app.exec()
