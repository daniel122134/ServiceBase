import csv
import os

from Devices.InputDevices.FolderInputDevice import FolderInputDevice


class SplitCsvFolderInputDevice(FolderInputDevice):
    def __init__(self, serializer, device_name, path):
        FolderInputDevice.__init__(self, serializer, device_name, path)
        self.device_name = device_name

    def get_products(self):
        if self.current_file:
            metadata = {"filename": os.path.basename(self.current_file.name),
                        "directory": os.path.dirname(self.current_file.name)}
            csv_reader = csv.reader(self.current_file, delimiter=',')
            headers = csv_reader.__next__()
            
            for line in csv_reader:
                try:
                    product = self.serializer.deserialize([line], headers=headers, **metadata)
                    self.logger.info("received new product:{}".format(product.item_id))
                    yield product
                except Exception as e:
                    self.logger.fatal("corrupted line received - skipping.error:{} content:{}".format(e, line))
                    continue
