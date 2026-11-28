from prettyqt import core, gui
from prettyqt.qt import QtGui
from prettyqt.utils import datatypes, get_repr


class PdfOutputIntent(QtGui.QPdfOutputIntent):
    """Metadata describing the color reproduction characteristics of a PDF document."""

    def __repr__(self):
        return get_repr(self, self.outputConditionIdentifier())

    def get_registry_name(self) -> core.Url:
        """Return the registry name URL."""
        return core.Url(self.registryName())

    def set_registry_name(self, url: datatypes.UrlType):
        """Set the registry name URL."""
        self.setRegistryName(datatypes.to_url(url))

    def get_output_profile(self) -> gui.ColorSpace:
        """Return the output color space profile."""
        return gui.ColorSpace(self.outputProfile())


if __name__ == "__main__":
    intent = PdfOutputIntent()
    print(repr(intent), intent.get_registry_name())
