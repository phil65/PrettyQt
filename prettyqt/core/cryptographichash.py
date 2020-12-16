from typing import Literal, Union

from qtpy import QtCore

from prettyqt.utils import InvalidParamError, bidict


ALGORITHM = bidict(
    md_4=QtCore.QCryptographicHash.Md4,
    md_5=QtCore.QCryptographicHash.Md5,
    sha_1=QtCore.QCryptographicHash.Sha1,
    sha_224=QtCore.QCryptographicHash.Sha224,
    sha_256=QtCore.QCryptographicHash.Sha256,
    sha_384=QtCore.QCryptographicHash.Sha384,
    sha_512=QtCore.QCryptographicHash.Sha512,
    sha3_224=QtCore.QCryptographicHash.Sha3_224,
    sha3_256=QtCore.QCryptographicHash.Sha3_256,
    sha3_384=QtCore.QCryptographicHash.Sha3_384,
    sha3_512=QtCore.QCryptographicHash.Sha3_512,
    keccak_224=QtCore.QCryptographicHash.Keccak_224,
    keccak_256=QtCore.QCryptographicHash.Keccak_256,
    keccak_384=QtCore.QCryptographicHash.Keccak_384,
    keccak_512=QtCore.QCryptographicHash.Keccak_512,
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
    def __init__(self, method: Union[int, AlgorithmStr]):
        if method in ALGORITHM:
            method = ALGORITHM[method]
        super().__init__(method)

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
