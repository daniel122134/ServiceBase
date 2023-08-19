import json
from copy import deepcopy

from Products.ExcelerProduct import ExcelerProduct
from Products.MongoUpdateProduct import MongoUpdateProduct
from Products.ProductBase import Product
from Serilizers.SerilizerBase import Serializer
import phonenumbers

class MongoUpdateSerializer(Serializer):

    def deserialize(self, stream, filename, headers=None, **kwargs):
        product = Product(stream)
        dict_repr = json.loads(stream)

        for key, value in dict_repr.items():
            product.__setattr__(key, value)
        return product

    def serialize(self, product):

        if type(product) == ExcelerProduct:
            return self.serialize_exceler_product(product)
        else:
            return self.serialize_product(product)
        

    def serialize_exceler_product(self, product :ExcelerProduct):
        new_product = MongoUpdateProduct(product.stream, product.source, product.product_type, **product.extra_params)

        full_name = product.first_name + " " + product.last_name
        product.__setattr__("full_name", full_name.lower().replace("-", " "))
        new_product.id_fields["fullName"] = full_name.lower().replace("-", " ")

        if product.linkedin:
            new_product.id_fields["linkedin"] = product.linkedin.lower()
            product.linkedin = product.linkedin.lower()
        if product.salesforce_id:
            new_product.id_fields["salesforceId"] = product.salesforce_id
        if product.email:
            new_product.id_fields["email"] = product.email.lower()
        if product.mobile_number:
            if product.mobile_number.startswith("1"):
                product.mobile_number = "+"+product.mobile_number
            parsed_number = phonenumbers.parse(product.mobile_number, "IL")
            formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
            new_product.id_fields["mobileNumber"] = formatted_number
            product.mobile_number = formatted_number
        if product.first_name:
            product.first_name= product.first_name.lower().replace("-", " ")
        if product.last_name:
            product.last_name= product.last_name.lower().replace("-", " ")



        for attr in [a for a in dir(product) if not a.startswith('__') and not callable(getattr(product, a))]:
            if attr != "stream" and attr != "source" and attr != "product_type":
                new_product.update_fields.append((underscore_to_camelcase(attr), product.__getattribute__(attr)))
        
        return new_product

    def serialize_product(self, product):
        for i, field in  enumerate(product.update_fields):
            if "Name" in field[0]:
                field = (field[0], field[1].lower().replace("-", " "))
                product.update_fields[i] = field
            if field[0] == "linkedin":
                field = (field[0], field[1].lower())
                product.update_fields[i] = field
        
        return product


def underscore_to_camelcase(value):
    def camelcase():
        yield str.lower
        while True:
            yield str.capitalize

    c = camelcase()
    return "".join(next(c)(x) if x else '_' for x in value.split("_"))