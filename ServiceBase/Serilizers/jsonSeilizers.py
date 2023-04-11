import json
from copy import deepcopy

from Products.ProductBase import Product
from Serilizers.SerilizerBase import Serializer


class JsonSerializer(Serializer):

    def deserialize(self, stream, filename, headers=None, **kwargs):
        product = Serializer.deserialize(self, stream, filename, headers, **kwargs)

        dict_repr = json.loads(stream)

        for key, value in dict_repr.items():
            product.__setattr__(key, value)
        return product

    def serialize(self, product):

        dict_repr = {}
        for name, attr in product.__dict__.items():
            try:
                hash(attr)
                dict_repr[name] = attr

            except TypeError:
                # Assume lack of __hash__ implies mutability. This is NOT
                # a bullet proof assumption but good in many cases.
                dict_repr[name] = deepcopy(attr)

        return json.dumps(dict_repr)
