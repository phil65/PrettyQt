from __future__ import annotations

from collections.abc import MutableMapping
from typing import Literal

from prettyqt.qt import QtBluetooth
from prettyqt.utils import bidict, datatypes


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


class BluetoothServiceInfo(
    QtBluetooth.QBluetoothServiceInfo, MutableMapping, metaclass=datatypes.QABCMeta
):
    def __getitem__(self, value: str | int | AttributeId):
        match value:
            case int():
                flag = value
            case str():
                flag = ATTRIBUTE_IDS[value].value
            case AttributeId():
                flag = value.value
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
        return iter(self.attributes())

    def __len__(self):
        return len(self.attributes())


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    address = BluetoothServiceInfo()
    address["documentation_url"] = "test"
    del address["documentation_url"]
