from qtpy import QtMultimedia


class MediaTimeInterval(QtMultimedia.QMediaTimeInterval):
    def __repr__(self):
        return f"{type(self).__name__}({self.start()}, {self.end()})"

    def __contains__(self, val: int):
        return self.contains(val)

    def __reduce__(self):
        return self.__class__, (self.start(), self.end())


if __name__ == "__main__":
    interval = MediaTimeInterval(0, 1000)
    print(repr(interval))
    assert 500 in interval
    import pickle

    with open("data.pkl", "wb") as jar:
        pickle.dump(interval, jar)
    with open("data.pkl", "rb") as jar:
        w = pickle.load(jar)
