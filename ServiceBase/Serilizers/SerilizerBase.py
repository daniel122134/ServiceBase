import os
import re

from Products.ProductBase import Product


class Serializer(object):
    def __init__(self, headers_regex=None,override_source=None,override_type=None,override_name=None):
        self.headers_regex = headers_regex
        self.override_source = override_source
        self.override_type = override_type
        self.override_name = override_name

    def serialize(self, product: Product):
        pass

    def deserialize(self, stream, filename, headers=None, **kwargs):
        product = Product(stream)
        match = re.search(self.headers_regex, os.path.basename(filename))
        product.__setattr__("source", match.groupdict().get("source"))
        product.__setattr__("product_type", match.groupdict().get("type"))
        product.__setattr__("product_name", match.groupdict().get("name"))
        if self.override_source:
            product.__setattr__("source", self.override_source)
        if self.override_type:
            product.__setattr__("product_type", self.override_type)
        if self.override_name:
            product.__setattr__("product_name", self.override_name)
        return product
