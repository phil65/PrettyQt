from __future__ import annotations

from typing import Literal

from prettyqt import core, network
from prettyqt.qt import QtNetwork
from prettyqt.utils import InvalidParamError, bidict


DNS_ELIGIBILITY_STATUS = bidict(
    unknown=QtNetwork.QNetworkAddressEntry.DnsEligibilityStatus.DnsEligibilityUnknown,
    eligible=QtNetwork.QNetworkAddressEntry.DnsEligibilityStatus.DnsEligible,
    ineligible=QtNetwork.QNetworkAddressEntry.DnsEligibilityStatus.DnsIneligible,
)

DnsEligibilityStatusStr = Literal["unknown", "eligible", "ineligible"]


class NetworkAddressEntry(QtNetwork.QNetworkAddressEntry):
    def get_dns_eligibility(self) -> DnsEligibilityStatusStr:
        """Return whether this address is eligible for publication in the DNS.

        Returns:
            DNS eligibility
        """
        return DNS_ELIGIBILITY_STATUS.inverse[self.dnsEligibility()]

    def set_dns_eligibility(self, status: DnsEligibilityStatusStr):
        """Set the DNS eligibility flag for this address to status.

        Args:
            status: DNS eligibility status

        Raises:
            InvalidParamError: dns eligibility status does not exist
        """
        if status not in DNS_ELIGIBILITY_STATUS:
            raise InvalidParamError(status, DNS_ELIGIBILITY_STATUS)
        self.setDnsEligibility(DNS_ELIGIBILITY_STATUS[status])

    def get_ip(self) -> network.HostAddress:
        return network.HostAddress(self.ip())

    def set_ip(self, ip: QtNetwork.QHostAddress | str):
        self.setIp(network.HostAddress(ip))

    def get_netmask(self) -> network.HostAddress:
        return network.HostAddress(self.netmask())

    def set_netmask(self, netmask: QtNetwork.QHostAddress | str):
        self.setNetmask(network.HostAddress(netmask))

    def get_preferred_lifetime(self) -> core.DeadlineTimer:
        return core.DeadlineTimer(self.preferredLifetime())

    def get_validity_lifetime(self) -> core.DeadlineTimer:
        return core.DeadlineTimer(self.validityLifetime())
