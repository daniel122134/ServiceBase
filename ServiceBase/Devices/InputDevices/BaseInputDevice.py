from logging import getLogger

from Devices.BaseDevice import BaseDevice


class BaseInputDevice(BaseDevice):
    def __init__(self, serializer, device_name):
        BaseDevice.__init__(self, serializer)
        self.device_name = device_name
        self.logger = getLogger("Input")
