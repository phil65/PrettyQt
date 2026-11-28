from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import datatypes


class MessageAuthenticationCode(QtCore.QMessageAuthenticationCode):
    """Way to generate hash-based message authentication codes (HMAC)."""

    def __init__(
        self,
        method: core.cryptographichash.AlgorithmStr | QtCore.QCryptographicHash.Algorithm,
        key: datatypes.ByteArrayType = b"",
    ):
        algo = core.cryptographichash.ALGORITHM.get_enum_value(method)
        super().__init__(algo, datatypes.to_bytearray(key))

    def __bytes__(self):
        return self.get_result()

    def set_key(self, key: datatypes.ByteArrayType):
        self.setKey(datatypes.to_bytearray(key))

    def add_data(self, data: datatypes.ByteArrayType):
        self.addData(datatypes.to_bytearray(data))

    def get_result(self) -> bytes:
        return bytes(self.result().data())

    @staticmethod
    def compute_hash(
        message: datatypes.ByteArrayType,
        key: datatypes.ByteArrayType,
        method: core.cryptographichash.AlgorithmStr | QtCore.QCryptographicHash.Algorithm,
    ) -> bytes:
        algo = core.cryptographichash.ALGORITHM.get_enum_value(method)
        result = QtCore.QMessageAuthenticationCode.hash(
            datatypes.to_bytearray(message),
            datatypes.to_bytearray(key),
            algo,
        )
        return bytes(result.data())
