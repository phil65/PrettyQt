from __future__ import annotations

from typing import Self

from prettyqt import location


class PlaceContentReply(location.PlaceReplyMixin, location.QPlaceContentReply):
    """Manages a content retrieval operation started by an instance of QPlaceManager."""

    def __len__(self):
        return self.totalCount()

    @classmethod
    def clone_from(cls, obj: location.QPlaceContentReply) -> Self:
        reply = cls(obj.parent())
        reply.setContent(obj.content())
        reply.setTotalCount(obj.totalCount())
        request = location.PlaceContentRequest(obj.nextPageRequest())
        reply.setNextPageRequest(request)
        request = location.PlaceContentRequest(obj.previousPageRequest())
        reply.setPreviousPageRequest(request)
        request = location.PlaceContentRequest(obj.request())
        reply.setRequest(request)
        return reply

    def get_next_page_request(self) -> location.PlaceContentRequest:
        return location.PlaceContentRequest(self.nextPageRequest())

    def get_previous_page_request(self) -> location.PlaceContentRequest:
        return location.PlaceContentRequest(self.previousPageRequest())

    def get_request(self) -> location.PlaceContentRequest:
        return location.PlaceContentRequest(self.request())


if __name__ == "__main__":
    reply = PlaceContentReply()
