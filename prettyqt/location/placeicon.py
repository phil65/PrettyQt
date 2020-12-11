from qtpy import QtLocation

from prettyqt import core


class PlaceIcon(QtLocation.QPlaceIcon):
    def __bool__(self):
        return not self.isEmpty()

    def __setitem__(self, index: str, val):
        attrs = self.parameters()
        attrs[index] = val
        self.setParameters(attrs)

    def __getitem__(self, index: str):
        attr = self.parameters()
        if index not in attr:
            raise KeyError(f"Key {index!r} does not exist.")
        return attr[index]

    # def get_manager(self) -> location.PlaceManager:
    #     return location.PlaceManager(self.manager())

    def get_url(self) -> core.Url:
        return core.Url(self.url())


if __name__ == "__main__":
    icon = PlaceIcon()
    print(bool(icon))
