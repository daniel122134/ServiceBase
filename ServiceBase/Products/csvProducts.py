from Products.ProductBase import Product


class CsvProduct(Product):
    def __init__(self, stream, source=None, product_type=None, records=None, **kwargs):
        Product.__init__(self, stream, source, product_type, **kwargs)
        self.records = records
