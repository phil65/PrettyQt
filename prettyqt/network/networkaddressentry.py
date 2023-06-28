from __future__ import annotations

from typing import Literal

from prettyqt import core, network
from prettyqt.utils import bidict


DnsEligibilityStatusStr = Literal["unknown", "eligible", "ineligible"]

DNS_ELIGIBILITY_STATUS: bidict[
    DnsEligibilityStatusStr, network.QNetworkAddressEntry.DnsEligibilityStatus
] = bidict(
    unknown=network.QNetworkAddressEntry.DnsEligibilityStatus.DnsEligibilityUnknown,
    eligible=network.QNetworkAddressEntry.DnsEligibilityStatus.DnsEligible,
    ineligible=network.QNetworkAddressEntry.DnsEligibilityStatus.DnsIneligible,
)


class NetworkAddressEntry(network.QNetworkAddressEntry):
    def get_dns_eligibility(self) -> DnsEligibilityStatusStr:
        """Return whether this address is eligible for publication in the DNS.

        Returns:
            DNS eligibility
        """
        return DNS_ELIGIBILITY_STATUS.inverse[self.dnsEligibility()]

    def set_dns_eligibility(
        self,
        status: DnsEligibilityStatusStr
        | network.QNetworkAddressEntry.DnsEligibilityStatus,
    ):
        """Set the DNS eligibility flag for this address to status.

        Args:
            status: DNS eligibility status
        """
        self.setDnsEligibility(DNS_ELIGIBILITY_STATUS.get_enum_value(status))

    def get_ip(self) -> network.HostAddress:
        return network.HostAddress(self.ip())

    def set_ip(self, ip: network.QHostAddress | str):
        self.setIp(network.HostAddress(ip))

    def get_netmask(self) -> network.HostAddress:
        return network.HostAddress(self.netmask())

    def set_netmask(self, netmask: network.QHostAddress | str):
        self.setNetmask(network.HostAddress(netmask))

    def get_preferred_lifetime(self) -> core.DeadlineTimer:
        return core.DeadlineTimer(self.preferredLifetime())

    def get_validity_lifetime(self) -> core.DeadlineTimer:
        return core.DeadlineTimer(self.validityLifetime())
