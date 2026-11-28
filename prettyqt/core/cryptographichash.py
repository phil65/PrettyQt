from typing import Literal

from prettyqt.qt import QtCore
from prettyqt.utils import bidict


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
    "blake2b_160",
    "blake2b_256",
    "blake2b_384",
    "blake2b_512",
    "blake2s_128",
    "blake2s_160",
    "blake2s_224",
    "blake2s_256",
]


ALGORITHM: bidict[AlgorithmStr, QtCore.QCryptographicHash.Algorithm] = bidict(
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
    blake2b_160=QtCore.QCryptographicHash.Algorithm.Blake2b_160,
    blake2b_256=QtCore.QCryptographicHash.Algorithm.Blake2b_256,
    blake2b_384=QtCore.QCryptographicHash.Algorithm.Blake2b_384,
    blake2b_512=QtCore.QCryptographicHash.Algorithm.Blake2b_512,
    blake2s_128=QtCore.QCryptographicHash.Algorithm.Blake2s_128,
    blake2s_160=QtCore.QCryptographicHash.Algorithm.Blake2s_160,
    blake2s_224=QtCore.QCryptographicHash.Algorithm.Blake2s_224,
    blake2s_256=QtCore.QCryptographicHash.Algorithm.Blake2s_256,
)


class CryptographicHash(QtCore.QCryptographicHash):
    """Way to generate cryptographic hashes."""

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
        return bytes(self.result().data())

    @staticmethod
    def get_hash_length(
        method: AlgorithmStr | QtCore.QCryptographicHash.Algorithm,
    ) -> int:
        return CryptographicHash.hashLength(ALGORITHM.get_enum_value(method))
