from __future__ import annotations

from typing import Literal

from prettyqt.qt import QtBluetooth
from prettyqt.utils import bidict


AttributeId = QtBluetooth.QBluetoothServiceInfo.AttributeId

ATTRIBUTE_IDS = bidict(
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

PROTOCOL = bidict(
    unknown=Protocol.UnknownProtocol,
    l2_cap=Protocol.L2capProtocol,
    rfcomm=Protocol.RfcommProtocol,
)

ProtocolStr = Literal["unknown", "l2_cap", "rfcomm"]


class BluetoothServiceInfo(QtBluetooth.QBluetoothServiceInfo):
    def __getitem__(self, value: str):
        attr = ATTRIBUTE_IDS.inverse[value]
        return self.attribute(attr)

    def __delitem__(self, value: str):
        attr = ATTRIBUTE_IDS.inverse[value]
        return self.removeAttribute(attr)

    def __setitem__(self, index: str, value):
        attr = ATTRIBUTE_IDS.inverse[index]
        return self.setAttribute(attr, value)

    def __contains__(self, value: int) -> bool:
        attr = ATTRIBUTE_IDS.inverse[value]
        return self.contains(attr)

    def __iter__(self):
        return iter(self.attributes())


if __name__ == "__main__":
    address = BluetoothServiceInfo()
