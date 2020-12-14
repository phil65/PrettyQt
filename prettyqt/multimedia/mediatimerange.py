from typing import Iterator

from qtpy import QtMultimedia

from prettyqt import multimedia


class MediaTimeRange(QtMultimedia.QMediaTimeRange):
    # def __repr__(self):
    #     return f"{type(self).__name__}()"

    def __contains__(self, val: int):
        return self.contains(val)

    def __getitem__(self, index: int) -> multimedia.MediaTimeInterval:
        return multimedia.MediaTimeInterval(self.intervals()[index])

    def __delitem__(self, index: slice):
        self.removeInterval(index.start, index.stop)

    def __len__(self):
        return len(self.intervals())

    def __iter__(self) -> Iterator[multimedia.MediaTimeInterval]:
        intervals = self.intervals()
        return iter(multimedia.MediaTimeInterval(i) for i in intervals)


if __name__ == "__main__":
    interval = MediaTimeRange(0, 1000)
    assert 500 in interval
    del interval[200:700]
    assert len(interval) == 2
    assert interval[0] == multimedia.MediaTimeInterval(0, 199)
    assert list(interval) == [
        multimedia.MediaTimeInterval(0, 199),
        multimedia.MediaTimeInterval(701, 1000),
    ]
    # import pickle

    # with open("data.pkl", "wb") as jar:
    #     pickle.dump(interval, jar)
    # with open("data.pkl", "rb") as jar:
    #     w = pickle.load(jar)
