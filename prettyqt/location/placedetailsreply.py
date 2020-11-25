# -*- coding: utf-8 -*-

from qtpy import QtLocation

from prettyqt import location


QtLocation.QPlaceDetailsReply.__bases__ = (location.PlaceReply,)


class PlaceDetailsReply(QtLocation.QPlaceDetailsReply):
    def get_place(self) -> location.Place:
        return location.Place(self.place())


if __name__ == "__main__":
    reply = PlaceDetailsReply()
    print(dir(reply))
