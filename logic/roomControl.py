import socket
from miio.miot_device import MiotDevice
from miio.exceptions import *
import time
import json


class RoomController:
    def __init__(self, ip, token):
        self.ip = ip
        self.token = token
        self.start_id = 0
        self.debug = 0
        self.timeout = None
        self.model = None
        self.mapping = 0
        self.retry_count = 1
        self.retry_delay = 1

        # Mapping of properties for dehumidifier
        self.prop_map = {
            "temp": {"siid": 3, "piid": 7},
            "humidity": {"siid": 3, "piid": 1},
            "target": {"siid": 2, "piid": 5},
            "switch": {"siid": 2, "piid": 1},
            "device_fault": {"siid": 2, "piid": 2},
            "mode_status": {"siid": 2, "piid": 3},
            "unit_lights": {"siid": 5, "piid": 1},
            "child_lock": {"siid": 6, "piid": 2},
            "compressor": {"siid": 7, "piid": 2},
            "coil_temp": {"siid": 7, "piid": 1},
            "water_tank": {"siid": 7, "piid": 3},
        }

        # Connect to the device using the miio module
        self.device = MiotDevice(
            ip=self.ip,
            token=self.token,
            start_id=self.start_id,
            debug=self.debug,
            lazy_discover=True,
            timeout=self.timeout,
            model=self.model,
            mapping=self.mapping,
        )

    def _get_property(self, prop_name):
        prop_info = self.prop_map[prop_name]
        for i in range(self.retry_count):
            try:
                data = {
                    "data": self.device.get_property_by(
                        siid=prop_info["siid"], piid=prop_info["piid"]
                    )
                }

                return data
            except DeviceException:
                time.sleep(self.retry_delay)

        return 0

    def _set_property(self, prop_name, value):
        prop_info = self.prop_map[prop_name]
        for i in range(self.retry_count):
            try:
                return {
                    "data": self.device.set_property_by(
                        siid=prop_info["siid"], piid=prop_info["piid"], value=value
                    )
                }
            except DeviceException:
                time.sleep(self.retry_delay)
        return 0

    def get_temperature(self):
        try:
            unit_temp = self._get_property("temp")["data"][0]["value"]
        except:
            unit_temp = 0
        if unit_temp != 0:
            dispensation_between_unit_room = 2
            return unit_temp - dispensation_between_unit_room
        else:
            return unit_temp

    def get_humidity(self):
        try:
            result = self._get_property("humidity")
        except:
            result = 0
        if result != 0:
            return result["data"][0]["value"]
        else:
            return result

    def get_target(self):
        try:
            result = self._get_property("target")
        except:
            result = 0
        if result != 0:
            return result["data"][0]["value"]
        else:
            return result

    def set_target(self, value):
        try:
            command = self._set_property(prop_name="target", value=value)
        except:
            command = 0
        if command != 0:
            return command["data"]
        else:
            return command

    def return_all_sensors(self):
        data = []
        humidity = self.get_humidity()
        temperature = self.get_temperature()
        target = self.get_target()
        if humidity == 0 or temperature == 0 or target == 0:
            return 0
        data.extend([humidity, temperature, target])
        return data
