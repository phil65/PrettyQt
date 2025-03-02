from __future__ import annotations

from typing import TYPE_CHECKING, Self

from prettyqt import location


if TYPE_CHECKING:
    from collections.abc import Iterator


class PlaceSearchReply(location.PlaceReplyMixin, location.QPlaceSearchReply):
    """Manages a place search operation started by an instance of QPlaceManager."""

    def __iter__(self) -> Iterator[location.PlaceSearchResult]:
        return iter(self.get_results())

    def __getitem__(self, index: int) -> location.PlaceSearchResult:
        return self.get_results()[index]

    def __len__(self):
        return len(self.get_results())

    @classmethod
    def clone_from(cls, obj: location.QPlaceSearchReply) -> Self:
        reply = cls(obj.parent())
        reply.setResults([location.PlaceSearchResult(i) for i in obj.results()])
        request = location.PlaceSearchRequest(obj.nextPageRequest())
        reply.setNextPageRequest(request)
        request = location.PlaceSearchRequest(obj.previousPageRequest())
        reply.setPreviousPageRequest(request)
        request = location.PlaceSearchRequest(obj.request())
        reply.setRequest(request)
        return reply

    def get_results(self) -> list[location.PlaceSearchResult]:
        return [location.PlaceSearchResult(i) for i in self.results()]

    def get_next_page_request(self) -> location.PlaceSearchRequest:
        return location.PlaceSearchRequest(self.nextPageRequest())

    def get_previous_page_request(self) -> location.PlaceSearchRequest:
        return location.PlaceSearchRequest(self.previousPageRequest())

    def get_request(self) -> location.PlaceSearchRequest:
        return location.PlaceSearchRequest(self.request())


if __name__ == "__main__":
    reply = PlaceSearchReply()
