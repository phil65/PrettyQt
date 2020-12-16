from typing import Union

from qtpy import QtNetwork

from prettyqt import core, network
from prettyqt.utils import InvalidParamError, bidict


DNS_ELIGIBILITY_STATUS = bidict(
    unknown=QtNetwork.QNetworkAddressEntry.DnsEligibilityUnknown,
    eligible=QtNetwork.QNetworkAddressEntry.DnsEligible,
    ineligible=QtNetwork.QNetworkAddressEntry.DnsIneligible,
)


class NetworkAddressEntry(QtNetwork.QNetworkAddressEntry):
    def get_dns_eligibility(self) -> str:
        """Return whether this address is eligible for publication in the DNS.

        Possible values: "unknown", "eligible", "ineligible"

        Returns:
            DNS eligibility
        """
        return DNS_ELIGIBILITY_STATUS.inverse[self.dnsEligibility()]

    def set_dns_eligibility(self, status: str):
        """Set the DNS eligibility flag for this address to status.

        Valid values: "unknown", "eligible", "ineligible"

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

    def set_ip(self, ip: Union[QtNetwork.QHostAddress, str]):
        self.setIp(network.HostAddress(ip))

    def get_netmask(self) -> network.HostAddress:
        return network.HostAddress(self.netmask())

    def set_netmask(self, netmask: Union[QtNetwork.QHostAddress, str]):
        self.setNetmask(network.HostAddress(netmask))

    def get_preferred_lifetime(self) -> core.DeadlineTimer:
        return core.DeadlineTimer(self.preferredLifetime())

    def get_validity_lifetime(self) -> core.DeadlineTimer:
        return core.DeadlineTimer(self.validityLifetime())
