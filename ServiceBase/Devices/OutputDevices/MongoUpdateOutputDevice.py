import phonenumbers
import pymongo as pymongo

from Devices.OutputDevices.BaseOutputDevice import BaseOutputDevice
from Products.ExcelerProduct import ExcelerProduct
from Products.MongoUpdateProduct import MongoUpdateProduct


class MongoUpdateOutputDevice(BaseOutputDevice):
    def __init__(self, serializer, device_name, connection_string, db_name, id_fields):
        BaseOutputDevice.__init__(self, serializer, device_name)
        c = pymongo.MongoClient(connection_string, tls=True, tlsAllowInvalidCertificates=True)
        db = c[db_name]
        self.db = db
        self.device_name = device_name

    def convert_to_mongo_update_product(self, product):
        if type(product) == ExcelerProduct:
            return self.serialize_exceler_product(product)
        else:
            return self.serialize_product(product)

    def send_product(self, product):
        collection_name = product.product_type
        mongo_update_product = self.convert_to_mongo_update_product(product)
        mongo_update_product.__delattr__("stream")

        results = None
        mongo_id = None
        doc = {}
        for field, value in mongo_update_product.id_fields.items():
            results = self.db[collection_name].find({field: value})
            if results.count() == 1:
                doc = results[0]
                mongo_id = results[0]["_id"]
                break

        if results is None or results.count() == 0:
            self.logger.info(
                "no profile found for:{}, creating new profile, ids:{}".format(product.item_id, [value for key, value in
                                                                                                 mongo_update_product.id_fields.items()]))
            insert_result = self.db[collection_name].insert_one(mongo_update_product.id_fields)
            mongo_id = insert_result.inserted_id
            doc = self.db[collection_name].find_one({"_id": mongo_id})
        update_dict = {}
        fields_to_update = {tuple[0]: tuple[1] for tuple in mongo_update_product.update_fields if tuple[1] is not None}
        for key, value in fields_to_update.items():
            if doc.get(key) != value:
                if key != "itemId" and key != "updateTime" and doc.get(key) is not None:
                    mongo_update_product.append_fields.append({"history":{key: doc.get(key), "updateTime": doc.get("updateTime")}})
                update_dict[key] = value
        
        for append_field in mongo_update_product.append_fields:
            should_skip = False
            for key, value in append_field.items():
                current_data = doc.get(key, [])
                if value in current_data:
                    continue

                if type(value) is dict:
                    for current_item in current_data:
                        is_identical = True
                        for attr, attr_value in current_item.items():
                            if attr_value != value.get(attr,"") and attr_value != "" and value.get(attr,"") != "":
                                is_identical = False
                                break

                        if is_identical:
                            should_skip = True
                            break

                    if should_skip:
                        print("skipping identical item:{}".format(value))
                        continue
                update_object = {"$push": {key: value}}
                self.db[collection_name].update_one({"_id": mongo_id}, update_object)

        update_object = {
            "$set": update_dict}
        self.db[collection_name].update_one({"_id": mongo_id}, update_object)

        self.logger.info("sent product:{}".format(product.item_id))

    def is_hebrew(self, text):
        return any("\u0590" <= c <= "\u05EA" for c in text)

    def serialize_exceler_product(self, product: ExcelerProduct):
        new_product = MongoUpdateProduct(product.stream, product.source, product.product_type, **product.extra_params)

        if product.first_name:
            if not self.is_hebrew(product.first_name):
                product.first_name = product.first_name.title().replace("-", " ").strip()
            else:
                product.hebrew_first_name = product.first_name.replace("-", " ").strip()

        if product.last_name:
            if not self.is_hebrew(product.last_name):
                product.last_name = product.last_name.title().replace("-", " ").strip()
            else:
                product.hebrew_last_name = product.last_name.replace("-", " ").strip()

        if product.first_name and product.last_name:
            if not self.is_hebrew(product.last_name) and not self.is_hebrew(product.first_name):
                full_name = product.first_name + " " + product.last_name
                product.__setattr__("full_name", full_name.title().replace("-", " ").strip())
            else:
                hebrew_full_name = product.first_name + " " + product.last_name
                product.__setattr__("full_name", hebrew_full_name.title().replace("-", " ").strip())

        if product.full_name:
            if self.is_hebrew(product.full_name):
                product.hebrew_full_name = product.full_name.title().replace("-", " ").strip()
                product.full_name = None

        if product.full_name:
            product.full_name = product.full_name.title().replace("-", " ").strip()
            new_product.id_fields["fullName"] = product.full_name
        if product.linkedin:
            new_product.id_fields["linkedin"] = product.linkedin.lower()
            product.linkedin = product.linkedin.lower()
        if product.salesforce_id:
            new_product.id_fields["salesforceId"] = product.salesforce_id
        if product.email:
            new_product.id_fields["email"] = product.email.lower()
            product.email = product.email.lower()
            
        if product.mobile_number:
            if product.mobile_number.startswith("1"):
                product.mobile_number = "+" + product.mobile_number
            parsed_number = phonenumbers.parse(product.mobile_number, "IL")
            formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
            new_product.id_fields["mobileNumber"] = formatted_number
            product.mobile_number = formatted_number

        if product.registration_date:
            new_product.append_fields.append(
                {"registrations": {"eventName": product.product_name, "registrationDate": product.registration_date}})
            product.__delattr__("registration_date")
            product.__delattr__("product_name")

        for attr in [a for a in dir(product) if not a.startswith('__') and not callable(getattr(product, a))]:
            if attr != "stream" and attr != "source" and attr != "product_type":
                if product.__getattribute__(attr):
                    new_product.update_fields.append((underscore_to_camelcase(attr), product.__getattribute__(attr)))

        return new_product

    def serialize_product(self, product):
        for i, field in enumerate(product.update_fields):
            if "Name" in field[0]:
                field = (field[0], field[1].title().replace("-", " "))
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
