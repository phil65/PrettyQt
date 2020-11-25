# -*- coding: utf-8 -*-

from qtpy import QtLocation

from prettyqt import location


QtLocation.QPlaceContentReply.__bases__ = (location.PlaceReply,)


class PlaceContentReply(QtLocation.QPlaceContentReply):
    def __len__(self):
        return self.totalCount()


if __name__ == "__main__":
    reply = PlaceContentReply()
