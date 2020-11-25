# -*- coding: utf-8 -*-

from qtpy import QtLocation

from prettyqt import location


QtLocation.QPlaceContentReply.__bases__ = (location.PlaceReply,)


class PlaceContentReply(QtLocation.QPlaceContentReply):
    def __len__(self):
        return self.totalCount()

    def get_next_page_request(self) -> location.PlaceContentRequest:
        return location.PlaceContentRequest(self.nextPageRequest())

    def get_previous_page_request(self) -> location.PlaceContentRequest:
        return location.PlaceContentRequest(self.previousPageRequest())

    def get_request(self) -> location.PlaceContentRequest:
        return location.PlaceContentRequest(self.request())


if __name__ == "__main__":
    reply = PlaceContentReply()
