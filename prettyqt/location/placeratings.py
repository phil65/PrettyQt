from qtpy import QtLocation


class PlaceRatings(QtLocation.QPlaceRatings):
    def __bool__(self):
        return not self.isEmpty()

    def __float__(self):
        return self.average()


if __name__ == "__main__":
    ratings = PlaceRatings()
    print(bool(ratings))
