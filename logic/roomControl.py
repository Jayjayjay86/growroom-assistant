from miio.miot_device import MiotDevice
from miio.exceptions import *
import time


class RoomController:
    def __init__(self, ip, token):
        self.ip = ip
        self.token = token
        self.start_id = 0
        self.debug = 0
        self.timeout = None
        self.model = None
        self.mapping = 0
        self.retry_count = 3
        self.retry_delay = 30

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
                return {
                    "data": self.device.get_property_by(
                        siid=prop_info["siid"], piid=prop_info["piid"]
                    ),
                    "connected": True,
                }
            except DeviceException:
                time.sleep(self.retry_delay)

        return {
            "data": "Failed to get {} after {} retries".format(
                prop_name, self.retry_count
            ),
            "connected": False,
        }

    def _set_property(self, prop_name, value):
        prop_info = self.prop_map[prop_name]
        for i in range(self.retry_count):
            try:
                return {
                    "data": self.device.set_property_by(
                        siid=prop_info["siid"], piid=prop_info["piid"], value=value
                    ),
                    "connected": True,
                }
            except DeviceException:
                time.sleep(self.retry_delay)
        return {
            "data": "Failed to get {} after {} retries".format(
                prop_name, self.retry_count
            ),
            "connected": False,
        }

    def get_temperature(self):
        unit_temp = self._get_property("temp")["data"][0]["value"]
        dispensation_between_unit_room = 2
        return unit_temp - dispensation_between_unit_room

    def get_humidity(self):
        result = self._get_property("humidity")
        if result["connected"]:
            return result["data"][0]["value"]
        else:
            print(result["data"])

    def get_target(self):
        result = self._get_property("target")

        if result["connected"]:
            return result["data"][0]["value"]
        else:
            print(result["data"])

    def set_target(self, value):
        command = self._set_property(prop_name="target", value=value)
        if command["connected"]:
            return command["data"]
        else:
            print(command["data"])

    def getStatus(self):
        return self.device._fetch_info()

    def return_all_sensors(self):
        x = []
        x.append(self.get_humidity())
        x.append(self.get_target())
        x.append(self.get_temperature())

        return x


# try:
#     RoomController(
#     ip="192.168.1.37", token="7110c3e10ebfc68c55bf44f0e610a15c"
# ).device.info()
#     print("ok")
# except:
#     print("not ok")
