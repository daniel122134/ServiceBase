import os

from Devices.OutputDevices.BaseOutputDevice import BaseOutputDevice


class FolderOutputDevice(BaseOutputDevice):
    def __init__(self, serializer, device_name, path):
        BaseOutputDevice.__init__(self, serializer, device_name)
        self.path = path
        self.device_name = device_name
        os.makedirs(os.path.join(self.path), exist_ok=True)

    def send_product(self, product):
        if not os.path.exists(self.path):
            os.makedirs(self.path, exist_ok=True)

        with open(os.path.join(self.path, product.item_id), "w") as output_file:
            output_file.write(self.serializer.serialize(product))
            self.logger.info("sent product:{}".format(product.item_id))
