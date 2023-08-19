import re

from Parsers.ParserBase import ParserBase
from Products.ProductBase import Product
from Products.csvProducts import CsvProduct


class RegexExtractorParser(ParserBase):
    def __init__(self, config_mapping, result_product_class: type):
        ParserBase.__init__(self)
        self.result_product_class = result_product_class
        self.config_mapping = config_mapping

    def parse(self, product_to_parse: CsvProduct):
        result_products = []

        for record in product_to_parse.records:
            result_product: Product = product_to_parse.clone(self.result_product_class)

            for header, config in self.config_mapping.items():
                normalized_header = header.lower().strip().replace(" ", "").replace("_", "").replace("-", "").replace("?", "").replace("(", "").replace(")", "").replace(":", "")
                normalized_record = {key.lower().strip().replace(" ", "").replace("_", "").replace("-", "").replace("?", "").replace("(", "").replace(")", "").replace(":", ""): value for key, value in record.items()}
                if "re" in config:
                    raw_data = normalized_record.get(normalized_header)
                    if raw_data:
                        matches = re.search(config["re"], raw_data)
                        results = matches.groupdict()
                        if "lambda" in config:
                            for key, value in results.items():
                                results[key] = config["lambda"](value)
                        for key, value in results.items():
                            if key != "salesforce_id" and key != "linkedin":
                                value = None if type(value) == str and value.lower() in ["null", "", "none"] else re.sub(" {2,}"," ",value.lower().replace("-"," ").replace("\t"," ").replace("\n"," ")) if type(value) == str else value
                            value = value.strip() if type(value) == str else value
                            value = value.strip("/") if type(value) == str else value
                            result_product.__setattr__(key, value)
                    else:
                        self.logger.debug("{} was not provided".format(header))
            result_product.__delattr__("records")
            result_products.append(result_product)
        return result_products
