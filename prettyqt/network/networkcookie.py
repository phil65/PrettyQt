from typing import Literal

from prettyqt.qt import QtNetwork
from prettyqt.utils import bidict, datatypes, get_repr


RawFormStr = Literal["name_and_value_only", "full"]

RAW_FORMS: bidict[RawFormStr, QtNetwork.QNetworkCookie.RawForm] = bidict(
    name_and_value_only=QtNetwork.QNetworkCookie.RawForm.NameAndValueOnly,
    full=QtNetwork.QNetworkCookie.RawForm.Full,
)

SameSiteStr = Literal["default", "none", "lax", "strict"]

SAME_SITE: bidict[SameSiteStr, QtNetwork.QNetworkCookie.SameSite] = bidict(
    default=QtNetwork.QNetworkCookie.SameSite.Default,
    none=QtNetwork.QNetworkCookie.SameSite.None_,
    lax=QtNetwork.QNetworkCookie.SameSite.Lax,
    strict=QtNetwork.QNetworkCookie.SameSite.Strict,
)


class NetworkCookie(QtNetwork.QNetworkCookie):
    """Holds one network cookie."""

    def __repr__(self):
        return get_repr(self, self.name(), self.value())

    def to_raw_form(self, full: bool = True):
        form = RAW_FORMS["full"] if full else RAW_FORMS["name_and_value_only"]
        return self.toRawForm(form)

    def set_same_site_policy(
        self, policy: SameSiteStr | QtNetwork.QNetworkCookie.SameSite
    ):
        self.setSameSitePolicy(SAME_SITE.get_enum_value(policy))

    def get_same_site_policy(self) -> SameSiteStr:
        return SAME_SITE.inverse[self.sameSitePolicy()]

    def set_name(self, name: datatypes.ByteArrayType):
        name = datatypes.to_bytearray(name)
        self.setName(name)

    def get_name(self) -> str:
        return bytes(self.name().data()).decode()

    def set_value(self, value: datatypes.ByteArrayType):
        value = datatypes.to_bytearray(value)
        self.setValue(value)

    def get_value(self) -> str:
        return bytes(self.value().data()).decode()

    def set_expiration_date(self, date: datatypes.DateTimeType | None):
        self.setExpirationDate(datatypes.to_datetime(date))


if __name__ == "__main__":
    cookie = NetworkCookie()
