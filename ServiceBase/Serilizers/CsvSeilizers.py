from Products.ProductBase import Product
from Serilizers.SerilizerBase import Serializer


class CsvSerializer(Serializer):
    def __init__(self, headers_regex):
        Serializer.__init__(self, headers_regex)

    def deserialize(self, stream, filename, headers=None, **kwargs):
        product = Serializer.deserialize(self, stream, filename, headers, **kwargs)
        records = []

        if not headers:
            pass
            # extract headers todo
        for line in stream.strip("\n").split("\n"):
            line = line.split(",")
            record = {headers[i]: line[i] for i in range(len(headers))}
            records.append(record)
        product.__setattr__("records", records)
        return product
