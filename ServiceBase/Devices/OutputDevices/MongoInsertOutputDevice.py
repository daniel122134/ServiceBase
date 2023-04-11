import pymongo as pymongo

from Devices.OutputDevices.BaseOutputDevice import BaseOutputDevice


class MongoInsertOutputDevice(BaseOutputDevice):
    def __init__(self, serializer, device_name, connection_string, db_name):
        BaseOutputDevice.__init__(self, serializer, device_name)
        c = pymongo.MongoClient(connection_string, tls=True, tlsAllowInvalidCertificates=True)
        db = c[db_name]
        self.db = db
        self.device_name = device_name

    def send_product(self, product):
        collection_name = product.product_type
        product.__delattr__("product_type")
        serialized_product = self.serializer.serialize(product)
        self.db[collection_name].insert_one(serialized_product)
        self.logger.info("sent product:{}".format(product.item_id))
