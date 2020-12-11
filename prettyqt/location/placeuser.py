from qtpy import QtLocation


class PlaceUser(QtLocation.QPlaceUser):
    def __str__(self):
        return self.name()


if __name__ == "__main__":
    user = PlaceUser()
