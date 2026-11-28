from typing import cast

from prettyqt import core, network


class RestAccessManager(core.ObjectMixin, network.QRestAccessManager):
    """Convenience wrapper around QNetworkAccessManager for RESTful APIs."""

    def get_network_access_manager(self) -> network.NetworkAccessManager:
        """Return the underlying NetworkAccessManager."""
        return cast(network.NetworkAccessManager, self.networkAccessManager())
