from logging import getLogger

from Products.ProductBase import Product


class ParserBase(object):
    def __init__(self):
        self.logger = getLogger("Parser")

    def parse(self, product: Product):
        yield product
