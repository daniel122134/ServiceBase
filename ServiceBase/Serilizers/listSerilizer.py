from Serilizers.SerilizerBase import Serializer


class ListSerializer(Serializer):

    def deserialize(self, stream, filename, headers=None, **kwargs):
        product = Serializer.deserialize(self, stream, filename, headers, **kwargs)
        records = []

        for line in stream:
            record = {headers[i]: line[i] for i in range(len(headers))}
            records.append(record)
        product.__setattr__("records", records)
        return product

    def serialize(self, product):
        return [[value for key, value in record] for record in product.__getattribute__("records")]
