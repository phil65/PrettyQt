from qtpy import QtCore


class Singleton(type(QtCore.QObject), type):  # type: ignore
    def __init__(cls, name, bases, dict):
        super().__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super().__call__(*args, **kw)
        return cls.instance


if __name__ == "__main__":

    class Test(QtCore.QObject, metaclass=Singleton):
        pass
