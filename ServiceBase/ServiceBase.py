import logging
import time
from logging import getLogger


class ServiceBase(object):
    def __init__(self, configuration):
        self.validate_configuration(configuration)
        self.input_devices = configuration["inputDevices"]
        self.output_devices = configuration["outputDevices"]
        self.bad_devices = configuration["badDevices"]
        self.parser_mappings = configuration["parserMapping"]
        self.logger = getLogger("ServiceBase")
        self.config_logger()

    def run(self):
        while True:
            for input_device in self.input_devices:
                did_parse = False
                with input_device:
                    try:
                        products= input_device.get_products()
                        for input_product in products:
                            did_parse = True
                            self.logger.info(
                                "Received Product: {}:{}.".format(input_product.source, input_product.product_type))

                            source = input_product.source
                            product_type = input_product.product_type
                            parser = self.get_parser_from_mapping(source, product_type)
                            result_products = parser.parse(input_product)
                            self.logger.info("Parsed Product: {}:{} using:{}.".format(input_product.source,
                                                                                      input_product.product_type,
                                                                                      type(parser)))

                            for result_product in result_products:
                                for output_device in self.output_devices:
                                    try:
                                        output_device.send_product(result_product)
                                    except Exception as e:
                                        self.logger.error(
                                            "output device failed to send product Sending to bad. reason:{}.".format(e))
                                        self.handle_bad_product(result_product)


                    except Exception as e:
                        self.logger.exception("Product failed, handling bad product. reason:{}.".format(e))
                        self.handle_bad_product(input_product)

                if not did_parse:
                    time.sleep(1)
                    self.logger.debug("No products found. sleeping till next round.")

    def handle_bad_product(self, product):
        for bad_device in self.bad_devices:
            bad_device.send_product(product)

    def get_parser_from_mapping(self, source, product_type):
        source_parsers = self.parser_mappings.get(source)
        if not source_parsers:
            raise Exception("no parser found for this product source: {}".format(source))
        parser = self.parser_mappings[source].get(product_type)
        if not parser:
            raise Exception("no parser found for this product. source: {}. type: {}".format(source, product_type))
        return parser

    def validate_configuration(self, configuration):
        pass  # TODO

    def config_logger(self):
        root_logger = getLogger()
        root_logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler('serviceBase.log')
        fh.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        root_logger.addHandler(fh)
        root_logger.addHandler(ch)
