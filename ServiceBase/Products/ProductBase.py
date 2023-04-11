from copy import deepcopy
from uuid import uuid4


class Product(object):
    def __init__(self, stream, source=None, product_type=None, **kwargs):
        self.stream = stream
        self.product_type = product_type
        self.product_name = None
        self.source = source
        self.extra_params = kwargs
        self.item_id = str(uuid4())

    def clone(self, cls):
        new_product = cls(self.stream)
        for name, attr in self.__dict__.items():
            try:
                hash(attr)
                new_product.__setattr__(name, attr)

            except TypeError:
                # Assume lack of __hash__ implies mutability. This is NOT
                # a bullet proof assumption but good in many cases.
                new_product.__setattr__(name, deepcopy(attr))
        return new_product

