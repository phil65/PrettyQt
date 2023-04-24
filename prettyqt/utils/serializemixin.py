from prettyqt import core


class SerializeMixin:
    def __getstate__(self):
        ba = core.DataStream.create_bytearray(self)
        return ba.data()

    def __setstate__(self, ba):
        core.DataStream.write_bytearray(ba, self)

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __bytes__(self):
        return self.__getstate__()
