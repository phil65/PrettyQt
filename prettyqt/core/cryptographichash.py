from __future__ import annotations

from typing import Literal

from prettyqt.qt import QtCore
from prettyqt.utils import InvalidParamError, bidict


ALGORITHM = bidict(
    md_4=QtCore.QCryptographicHash.Algorithm.Md4,
    md_5=QtCore.QCryptographicHash.Algorithm.Md5,
    sha_1=QtCore.QCryptographicHash.Algorithm.Sha1,
    sha_224=QtCore.QCryptographicHash.Algorithm.Sha224,
    sha_256=QtCore.QCryptographicHash.Algorithm.Sha256,
    sha_384=QtCore.QCryptographicHash.Algorithm.Sha384,
    sha_512=QtCore.QCryptographicHash.Algorithm.Sha512,
    sha3_224=QtCore.QCryptographicHash.Algorithm.Sha3_224,
    sha3_256=QtCore.QCryptographicHash.Algorithm.Sha3_256,
    sha3_384=QtCore.QCryptographicHash.Algorithm.Sha3_384,
    sha3_512=QtCore.QCryptographicHash.Algorithm.Sha3_512,
    keccak_224=QtCore.QCryptographicHash.Algorithm.Keccak_224,
    keccak_256=QtCore.QCryptographicHash.Algorithm.Keccak_256,
    keccak_384=QtCore.QCryptographicHash.Algorithm.Keccak_384,
    keccak_512=QtCore.QCryptographicHash.Algorithm.Keccak_512,
)

AlgorithmStr = Literal[
    "md_4",
    "md_5",
    "sha_1",
    "sha_224",
    "sha_256",
    "sha_384",
    "sha_512",
    "sha3_224",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "keccak_224",
    "keccak_256",
    "keccak_384",
    "keccak_512",
]


class CryptographicHash(QtCore.QCryptographicHash):
    def __init__(self, method: QtCore.QCryptographicHash.Algorithm | AlgorithmStr):
        if isinstance(method, QtCore.QCryptographicHash.Algorithm):
            arg = method
        else:
            arg = ALGORITHM[method]
        super().__init__(arg)

    # def __str__(self):
    #     return bytes(self.result()).decode()

    def __bytes__(self):
        return self.get_result()

    def get_result(self) -> bytes:
        return bytes(self.result())

    @staticmethod
    def get_hash_length(method: AlgorithmStr) -> int:
        if method not in ALGORITHM:
            raise InvalidParamError(method, ALGORITHM)
        return CryptographicHash.hashLength(ALGORITHM[method])
