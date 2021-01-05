from __future__ import annotations

from prettyqt.qt import QtBluetooth
from prettyqt.utils import bidict


md = QtBluetooth.QBluetoothServiceInfo

ATTRIBUTE_IDS = bidict(
    service_record_handle=md.ServiceRecordHandle,
    service_class_ids=md.ServiceClassIds,
    service_record_state=md.ServiceRecordState,
    service_id=md.ServiceId,
    protocol_descriptor_list=md.ProtocolDescriptorList,
    browse_group_list=md.BrowseGroupList,
    language_base_attribute_id_list=md.LanguageBaseAttributeIdList,
    service_info_time_to_live=md.ServiceInfoTimeToLive,
    service_availablity=md.ServiceAvailability,
    bluetooth_profile_descriptor_list=md.BluetoothProfileDescriptorList,
    documentation_url=md.DocumentationUrl,
    client_executable_url=md.ClientExecutableUrl,
    icon_url=md.IconUrl,
    additional_protocol_descriptor_list=md.AdditionalProtocolDescriptorList,
    primary_language_base=md.PrimaryLanguageBase,
    # service_name=md.ServiceName,
    service_description=md.ServiceDescription,
    service_provider=md.ServiceProvider,
)

PROTOCOLS = bidict(
    unknown=md.UnknownProtocol,
    l2_cap=md.L2capProtocol,
    rfcomm=md.RfcommProtocol,
)


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

    def __contains__(self, value: int) -> str:
        attr = ATTRIBUTE_IDS.inverse[value]
        return self.contains(attr)

    def __iter__(self):
        return iter(self.attributes())


if __name__ == "__main__":
    address = BluetoothServiceInfo()
