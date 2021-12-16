from __future__ import annotations

from typing import Literal

from prettyqt import core, network
from prettyqt.qt import QtNetwork
from prettyqt.utils import InvalidParamError, bidict, types


OPERATION = bidict(
    head=QtNetwork.QNetworkAccessManager.Operation.HeadOperation,
    get=QtNetwork.QNetworkAccessManager.Operation.GetOperation,
    put=QtNetwork.QNetworkAccessManager.Operation.PutOperation,
    post=QtNetwork.QNetworkAccessManager.Operation.PostOperation,
    delete=QtNetwork.QNetworkAccessManager.Operation.DeleteOperation,
    custom=QtNetwork.QNetworkAccessManager.Operation.CustomOperation,
)

OperationStr = Literal["head", "get", "put", "post", "delete", "custom"]

QtNetwork.QNetworkAccessManager.__bases__ = (core.Object,)


class NetworkAccessManager(QtNetwork.QNetworkAccessManager):
    # def request(
    #     self,
    #     method,
    #     url,
    #     headers=None,
    #     cookies=None,
    #     files=None,
    #     auth=None,
    #     timeout=None,
    #     allow_redirects=True,
    # ):
    #     req = network.NetworkRequest()
    #     if allow_redirects:
    #         pass

    def get(self, request: types.UrlType | QtNetwork.QNetworkRequest):
        if isinstance(request, str):
            request = core.Url(request)
        request = network.NetworkRequest(request)
        return super().get(request)

    # def post(self, url, data=None, json=None):
    #     pass

    # def put(self, url, data=None, json=None):
    #     pass

    # def patch(self, url, data=None):
    #     pass

    # def delete(self, url):
    #     pass

    def set_redirect_policy(self, policy: network.networkrequest.RedirectPolicyStr):
        """Set redirect policy.

        Args:
            policy: redirect policy

        Raises:
            InvalidParamError: redirect policy does not exist
        """
        if policy not in network.networkrequest.REDIRECT_POLICIES:
            raise InvalidParamError(policy, network.networkrequest.REDIRECT_POLICIES)
        self.setRedirectPolicy(network.networkrequest.REDIRECT_POLICIES[policy])

    def get_redirect_policy(self) -> network.networkrequest.RedirectPolicyStr:
        """Get the current redirect policy.

        Returns:
            redirect policy
        """
        return network.networkrequest.REDIRECT_POLICIES.inverse[self.redirectPolicy()]
