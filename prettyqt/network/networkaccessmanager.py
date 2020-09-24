# -*- coding: utf-8 -*-

from qtpy import QtNetwork

from prettyqt import core, network
from prettyqt.utils import bidict, InvalidParamError

OPERATIONS = bidict(
    head=QtNetwork.QNetworkAccessManager.HeadOperation,
    get=QtNetwork.QNetworkAccessManager.GetOperation,
    put=QtNetwork.QNetworkAccessManager.PutOperation,
    post=QtNetwork.QNetworkAccessManager.PostOperation,
    delete=QtNetwork.QNetworkAccessManager.DeleteOperation,
    custom=QtNetwork.QNetworkAccessManager.CustomOperation,
)

REDIRECT_POLICIES = network.networkrequest.REDIRECT_POLICIES

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

    # def get(self, url, params=None):
    #     pass

    # def post(self, url, data=None, json=None):
    #     pass

    # def put(self, url, data=None, json=None):
    #     pass

    # def patch(self, url, data=None):
    #     pass

    # def delete(self, url):
    #     pass

    def set_redirect_policy(self, policy: str):
        """Set redirect policy.

        Valid values: "manual", "no_less_safe", "same_origin", "user_verified"

        Args:
            policy: redirect policy

        Raises:
            InvalidParamError: redirect policy does not exist
        """
        if policy not in REDIRECT_POLICIES:
            raise InvalidParamError(policy, REDIRECT_POLICIES)
        self.setRedirectPolicy(REDIRECT_POLICIES[policy])

    def get_redirect_policy(self) -> str:
        """Get the current redirect policy.

        Possible values: "manual", "no_less_safe", "same_origin", "user_verified"

        Returns:
            redirect policy
        """
        return REDIRECT_POLICIES.inv[self.redirectPolicy()]
