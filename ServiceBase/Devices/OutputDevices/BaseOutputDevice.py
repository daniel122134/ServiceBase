from logging import getLogger

from Devices.BaseDevice import BaseDevice
from Products.ProductBase import Product


class BaseOutputDevice(BaseDevice):
    def __init__(self, serializer, device_name):
        BaseDevice.__init__(self, serializer)
        self.device_name = device_name
        self.logger = getLogger("Output")

    def send_product(self, product: Product):
        pass
