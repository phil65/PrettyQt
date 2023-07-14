from __future__ import annotations

from collections.abc import MutableMapping
from typing import Literal

from prettyqt.qt import QtBluetooth
from prettyqt.utils import bidict, datatypes


AttributeIdStr = Literal[
    "service_record_handle",
    "service_class_ids",
    "service_record_state",
    "service_id",
    "protocol_descriptor_list",
    "browse_group_list",
    "language_base_attribute_id_list",
    "service_info_time_to_live",
    "service_availablity",
    "bluetooth_profile_descriptor_list",
    "documentation_url",
    "client_executable_url",
    "icon_url",
    "additional_protocol_descriptor_list",
    "primary_language_base",
    "service_name",
    "service_description",
    "service_provider",
]

AttributeId = QtBluetooth.QBluetoothServiceInfo.AttributeId

ATTRIBUTE_IDS: bidict[AttributeIdStr, AttributeId] = bidict(
    service_record_handle=AttributeId.ServiceRecordHandle,
    service_class_ids=AttributeId.ServiceClassIds,
    service_record_state=AttributeId.ServiceRecordState,
    service_id=AttributeId.ServiceId,
    protocol_descriptor_list=AttributeId.ProtocolDescriptorList,
    browse_group_list=AttributeId.BrowseGroupList,
    language_base_attribute_id_list=AttributeId.LanguageBaseAttributeIdList,
    service_info_time_to_live=AttributeId.ServiceInfoTimeToLive,
    service_availablity=AttributeId.ServiceAvailability,
    bluetooth_profile_descriptor_list=AttributeId.BluetoothProfileDescriptorList,
    documentation_url=AttributeId.DocumentationUrl,
    client_executable_url=AttributeId.ClientExecutableUrl,
    icon_url=AttributeId.IconUrl,
    additional_protocol_descriptor_list=AttributeId.AdditionalProtocolDescriptorList,
    primary_language_base=AttributeId.PrimaryLanguageBase,
    # service_name=AttributeId.ServiceName,
    service_description=AttributeId.ServiceDescription,
    service_provider=AttributeId.ServiceProvider,
)

Protocol = QtBluetooth.QBluetoothServiceInfo.Protocol

ProtocolStr = Literal["unknown", "l2_cap", "rfcomm"]

PROTOCOL: bidict[ProtocolStr, Protocol] = bidict(
    unknown=Protocol.UnknownProtocol,
    l2_cap=Protocol.L2capProtocol,
    rfcomm=Protocol.RfcommProtocol,
)


class BluetoothServiceInfo(
    QtBluetooth.QBluetoothServiceInfo, MutableMapping, metaclass=datatypes.QABCMeta
):
    """Enables access to the attributes of a Bluetooth service.

    Also implements MutableMapping interface, can be used as a dicionary.
    """

    def __getitem__(self, value: str | int | AttributeId):
        match value:
            case int():
                flag = value
            case str():
                if value not in ATTRIBUTE_IDS:
                    raise KeyError(value)
                flag = ATTRIBUTE_IDS[value].value
            case AttributeId():
                flag = value.value
            case _:
                raise KeyError(value)
        return self.attribute(flag)

    def __delitem__(self, value: str | int | AttributeId):
        match value:
            case int():
                flag = value
            case str():
                flag = ATTRIBUTE_IDS[value].value
            case AttributeId():
                flag = value.value
        return self.removeAttribute(flag)

    def __setitem__(self, index: str | int | AttributeId, value):
        """Set attribute."""
        match index:
            case int():
                flag = index
            case str():
                flag = ATTRIBUTE_IDS[index].value
            case AttributeId():
                flag = index.value
        return self.setAttribute(flag, value)

    def __contains__(self, value: int) -> bool:
        attr = ATTRIBUTE_IDS.inverse[value]
        return self.contains(attr)

    def __iter__(self):
        """Iter the info attributes."""
        return iter(self.attributes())

    def __len__(self):
        return len(self.attributes())


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    address = BluetoothServiceInfo()
    address["documentation_url"] = "test"
    del address["documentation_url"]
