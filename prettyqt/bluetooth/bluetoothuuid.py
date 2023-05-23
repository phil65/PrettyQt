from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtBluetooth
from prettyqt.utils import bidict


md = QtBluetooth.QBluetoothUuid.CharacteristicType


CHARACTERISTIC_TYPES = bidict(
    aerobic_heart_rate_lower=md.AerobicHeartRateLowerLimit,
    aerobic_heart_rate_upper=md.AerobicHeartRateUpperLimit,
    aerobic_threshold=md.AerobicThreshold,
    age=md.Age,
    anaerobic_heart_rate_lower=md.AnaerobicHeartRateLowerLimit,
    anaerobic_heart_rate_upper=md.AnaerobicHeartRateUpperLimit,
    anaerobic_threshold=md.AnaerobicThreshold,
    alert_category_id=md.AlertCategoryID,
    alert_category_id_bitmask=md.AlertCategoryIDBitMask,
    alert_level=md.AlertLevel,
    alert_notification_control_point=md.AlertNotificationControlPoint,
    alert_status=md.AlertStatus,
    apparent_wind_direction=md.ApparentWindDirection,
    apparent_wind_speed=md.ApparentWindSpeed,
    appearance=md.Appearance,
    barometric_pressure_trend=md.BarometricPressureTrend,
    battery_level=md.BatteryLevel,
    blood_pressure_feature=md.BloodPressureFeature,
    blood_pressure_measurement=md.BloodPressureMeasurement,
    body_composition_feature=md.BodyCompositionFeature,
    body_composition_measurement=md.BodyCompositionMeasurement,
    body_sensor_location=md.BodySensorLocation,
    boot_keyboard_input_report=md.BootKeyboardInputReport,
    boot_keyboard_output_report=md.BootKeyboardOutputReport,
    boot_mouse_input_report=md.BootMouseInputReport,
    csc_feature=md.CSCFeature,
    csc_measurement=md.CSCMeasurement,
    current_time=md.CurrentTime,
    cycling_power_control_point=md.CyclingPowerControlPoint,
    cycling_power_feature=md.CyclingPowerFeature,
    cycling_power_measurement=md.CyclingPowerMeasurement,
    cycling_power_vector=md.CyclingPowerVector,
    database_change_increment=md.DatabaseChangeIncrement,
    date_of_birth=md.DateOfBirth,
    date_of_threshold_assessment=md.DateOfThresholdAssessment,
    date_time=md.DateTime,
    day_date_time=md.DayDateTime,
    day_of_week=md.DayOfWeek,
    descriptor_value_changed=md.DescriptorValueChanged,
    device_name=md.DeviceName,
    dew_point=md.DewPoint,
    dst_offset=md.DSTOffset,
    elevation=md.Elevation,
    email_address=md.EmailAddress,
    exact_time_256=md.ExactTime256,
    fat_burn_hear_rate_lower_limit=md.FatBurnHeartRateLowerLimit,
    fat_burn_hear_rate_upper_limit=md.FatBurnHeartRateUpperLimit,
    firmware_revision_string=md.FirmwareRevisionString,
    first_name=md.FirstName,
    five_zone_heart_rate_limits=md.FiveZoneHeartRateLimits,
    gender=md.Gender,
    glucose_feature=md.GlucoseFeature,
    glucose_measurement=md.GlucoseMeasurement,
    glucose_measurement_context=md.GlucoseMeasurementContext,
    gust_factor=md.GustFactor,
    hardware_revision_string=md.HardwareRevisionString,
    max_recommended_heart_rate=md.MaximumRecommendedHeartRate,
    heart_rate_control_point=md.HeartRateControlPoint,
    heart_rate_max=md.HeartRateMax,
    heart_rate_measurement=md.HeartRateMeasurement,
    heat_index=md.HeatIndex,
    height=md.Height,
    hid_control_point=md.HIDControlPoint,
    hid_information=md.HIDInformation,
    hip_circum_reference=md.HipCircumference,
    humidity=md.Humidity,
    regulatory_certification_list=md.IEEE1107320601RegulatoryCertificationDataList,
    intermediate_cuff_pressure=md.IntermediateCuffPressure,
    intermediate_temperature=md.IntermediateTemperature,
    irradiance=md.Irradiance,
    language=md.Language,
    last_name=md.LastName,
    ln_control_point=md.LNControlPoint,
    ln_feature=md.LNFeature,
    local_time_information=md.LocalTimeInformation,
    location_and_speed=md.LocationAndSpeed,
    magnetic_declination=md.MagneticDeclination,
    magnetic_flux_density_2d=md.MagneticFluxDensity2D,
    magnetic_magnetic_flux_density_3d=md.MagneticFluxDensity3D,
    manufacturer_name_string=md.ManufacturerNameString,
    measurement_interval=md.MeasurementInterval,
    model_number_string=md.ModelNumberString,
    navigation=md.Navigation,
    new_alert=md.NewAlert,
    peripheral_preferred_connection_parameters=md.PeripheralPreferredConnectionParameters,
    peripheral_privacy_flag=md.PeripheralPrivacyFlag,
    pn_pid=md.PnPID,
    pollen_concentration=md.PollenConcentration,
    position_quality=md.PositionQuality,
    pressure=md.Pressure,
    protocol_mode=md.ProtocolMode,
    rainfall=md.Rainfall,
    reconnection_address=md.ReconnectionAddress,
    record_access_control_point=md.RecordAccessControlPoint,
    reference_time_information=md.ReferenceTimeInformation,
    report=md.Report,
    report_map=md.ReportMap,
    resting_heart_rate=md.RestingHeartRate,
    ringer_control_point=md.RingerControlPoint,
    ringer_setting=md.RingerSetting,
    rsc_feature=md.RSCFeature,
    rsc_measurement=md.RSCMeasurement,
    sc_control_point=md.SCControlPoint,
    scan_interval_window=md.ScanIntervalWindow,
    scan_refresh=md.ScanRefresh,
    sensor_location=md.SensorLocation,
    serial_number_string=md.SerialNumberString,
    service_changed=md.ServiceChanged,
    software_revision_string=md.SoftwareRevisionString,
    sport_type_for_aerobic_anaerobic_thresholds=md.SportTypeForAerobicAnaerobicThresholds,
    supported_new_alert_category=md.SupportedNewAlertCategory,
    supported_unread_alert_category=md.SupportedUnreadAlertCategory,
    system_id=md.SystemID,
    temperature=md.Temperature,
    temperature_measurement=md.TemperatureMeasurement,
    temperature_type=md.TemperatureType,
    three_zone_heart_rate_limits=md.ThreeZoneHeartRateLimits,
    time_accuracy=md.TimeAccuracy,
    time_source=md.TimeSource,
    time_update_control_point=md.TimeUpdateControlPoint,
    time_update_state=md.TimeUpdateState,
    time_with_dst=md.TimeWithDST,
    time_zone=md.TimeZone,
    true_wind_direction=md.TrueWindDirection,
    true_wind_speed=md.TrueWindSpeed,
    two_zone_hear_rate_limits=md.TwoZoneHeartRateLimits,
    tx_power_level=md.TxPowerLevel,
    unread_alert_status=md.UnreadAlertStatus,
    user_control_point=md.UserControlPoint,
    user_index=md.UserIndex,
    uv_index=md.UVIndex,
    vo_2_max=md.VO2Max,
    waist_circumference=md.WaistCircumference,
    weight=md.Weight,
    weight_measurement=md.WeightMeasurement,
    weight_scale_feature=md.WeightScaleFeature,
    wind_chill=md.WindChill,
)

dt = QtBluetooth.QBluetoothUuid.DescriptorType

DESCRIPTOR_TYPE = bidict(
    characteristic_extended_properties=dt.CharacteristicExtendedProperties,
    characteristic_user_description=dt.CharacteristicUserDescription,
    client_characteristic_configuration=dt.ClientCharacteristicConfiguration,
    server_characteristic_configuration=dt.ServerCharacteristicConfiguration,
    characteristic_presentation_format=dt.CharacteristicPresentationFormat,
    characteristic_aggregate_format=dt.CharacteristicAggregateFormat,
    valid_range=dt.ValidRange,
    external_report_reference=dt.ExternalReportReference,
    report_reference=dt.ReportReference,
    environmental_sensing_configuration=dt.EnvironmentalSensingConfiguration,
    environmental_sensing_measurement=dt.EnvironmentalSensingMeasurement,
    environmental_sensing_trigger_setting=dt.EnvironmentalSensingTriggerSetting,
    unknown_descriptor_type=dt.UnknownDescriptorType,
)

pu = QtBluetooth.QBluetoothUuid.ProtocolUuid

PROTOCOL_UUID = bidict(
    sdp=pu.Sdp,
    udp=pu.Udp,
    rfcomm=pu.Rfcomm,
    tcp=pu.Tcp,
    tcs_bin=pu.TcsBin,
    tcs_at=pu.TcsAt,
    att=pu.Att,
    obex=pu.Obex,
    ip=pu.Ip,
    ftp=pu.Ftp,
    http=pu.Http,
    wsp=pu.Wsp,
    bnep=pu.Bnep,
    upnp=pu.Upnp,
    hidp=pu.Hidp,
    hardcopy_control_channel=pu.HardcopyControlChannel,
    hardcopy_data_channel=pu.HardcopyDataChannel,
    hardcopy_notification=pu.HardcopyNotification,
    avctp=pu.Avctp,
    avdtp=pu.Avdtp,
    cmtp=pu.Cmtp,
    udi_c_plain=pu.UdiCPlain,
    mcap_control_channel=pu.McapControlChannel,
    mcap_data_channel=pu.McapDataChannel,
    l2_cap=pu.L2cap,
)

su = QtBluetooth.QBluetoothUuid.ServiceClassUuid

SERVICE_CLASS_UUID = bidict(
    service_discovery_server=su.ServiceDiscoveryServer,
    browser_group_descriptor=su.BrowseGroupDescriptor,
    public_browse_group=su.PublicBrowseGroup,
    serial_port=su.SerialPort,
    lan_access_using_ppp=su.LANAccessUsingPPP,
    dial_up_networking=su.DialupNetworking,
    ir_mc_sync=su.IrMCSync,
    obex_object_push=su.ObexObjectPush,
    obex_file_transfer=su.OBEXFileTransfer,
    ir_mc_sync_command=su.IrMCSyncCommand,
    headset=su.Headset,
    audio_source=su.AudioSource,
    audio_sink=su.AudioSink,
    av_remove_control_target=su.AV_RemoteControlTarget,
    advanced_audio_distribution=su.AdvancedAudioDistribution,
    av_remote_control=su.AV_RemoteControl,
    av_remote_control_controller=su.AV_RemoteControlController,
    headset_ag=su.HeadsetAG,
    panu=su.PANU,
    nap=su.NAP,
    gn=su.GN,
    direct_printing=su.DirectPrinting,
    reference_printing=su.ReferencePrinting,
    basic_image=su.BasicImage,
    imaging_responder=su.ImagingResponder,
    imaging_automatic_archive=su.ImagingAutomaticArchive,
    imaging_reference_objects=su.ImagingReferenceObjects,
    hands_free=su.Handsfree,
    hands_free_audio_gateway=su.HandsfreeAudioGateway,
    direct_printing_reference_objects_service=su.DirectPrintingReferenceObjectsService,
    reflected_ui=su.ReflectedUI,
    basic_printing=su.BasicPrinting,
    printing_status=su.PrintingStatus,
    human_interface_device_service=su.HumanInterfaceDeviceService,
    hardcopy_cable_replacement=su.HardcopyCableReplacement,
    hcr_print=su.HCRPrint,
    hcr_scan=su.HCRScan,
    sim_access=su.SIMAccess,
    phonebook_access_pce=su.PhonebookAccessPCE,
    phonebook_access_pse=su.PhonebookAccessPSE,
    phonebook_access=su.PhonebookAccess,
    headset_hs=su.HeadsetHS,
    message_access_server=su.MessageAccessServer,
    message_notification_server=su.MessageNotificationServer,
    message_access_profile=su.MessageAccessProfile,
    gnss=su.GNSS,
    gnss_server=su.GNSSServer,
    display_3d=su.Display3D,
    glasses_3d=su.Glasses3D,
    synchronization_3d=su.Synchronization3D,
    mps_profile=su.MPSProfile,
    mps_service=su.MPSService,
    pnp_information=su.PnPInformation,
    generic_networking=su.GenericNetworking,
    generic_file_transfer=su.GenericFileTransfer,
    generic_audio=su.GenericAudio,
    generic_telephony=su.GenericTelephony,
    video_source=su.VideoSource,
    video_sink=su.VideoSink,
    video_distribution=su.VideoDistribution,
    hdp=su.HDP,
    hdp_source=su.HDPSource,
    hdp_sink=su.HDPSink,
    generic_access=su.GenericAccess,
    generic_attribute=su.GenericAttribute,
    immediate_alert=su.ImmediateAlert,
    link_loss=su.LinkLoss,
    tx_power=su.TxPower,
    current_time_service=su.CurrentTimeService,
    reference_time_update_service=su.ReferenceTimeUpdateService,
    next_dst_change_service=su.NextDSTChangeService,
    glucose=su.Glucose,
    health_thermometer=su.HealthThermometer,
    device_information=su.DeviceInformation,
    heart_rate=su.HeartRate,
    phone_alert_status_service=su.PhoneAlertStatusService,
    battery_service=su.BatteryService,
    blood_pressure=su.BloodPressure,
    alert_notification_service=su.AlertNotificationService,
    human_interface_device=su.HumanInterfaceDevice,
    scan_parameters=su.ScanParameters,
    running_speed_and_cadence=su.RunningSpeedAndCadence,
    cycling_speed_and_cadence=su.CyclingSpeedAndCadence,
    cycling_power=su.CyclingPower,
    location_and_navigation=su.LocationAndNavigation,
    environmental_sensing=su.EnvironmentalSensing,
    body_composition=su.BodyComposition,
    user_data=su.UserData,
    weight_scale=su.WeightScale,
    bond_management=su.BondManagement,
    continuous_glucose_monitoring=su.ContinuousGlucoseMonitoring,
)


class BluetoothUuid(core.UuidMixin, QtBluetooth.QBluetoothUuid):
    pass


if __name__ == "__main__":
    address = BluetoothUuid()