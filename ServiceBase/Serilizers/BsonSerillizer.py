from copy import deepcopy

from Products.ProductBase import Product
from Serilizers.SerilizerBase import Serializer


class BsonSerializer(Serializer):
    def __init__(self):
        Serializer.__init__(self)

    def serialize(self, product: Product):
        dict_repr = {}
        for name, attr in product.__dict__.items():
            try:
                hash(attr)
                dict_repr[underscore_to_camelcase(name)] = attr

            except TypeError:
                # Assume lack of __hash__ implies mutability. This is NOT
                # a bullet proof assumption but good in many cases.
                dict_repr[underscore_to_camelcase(name)] = deepcopy(attr)

        return dict_repr


def underscore_to_camelcase(value):
    def camelcase():
        yield str.lower
        while True:
            yield str.capitalize

    c = camelcase()
    return "".join(next(c)(x) if x else '_' for x in value.split("_"))
