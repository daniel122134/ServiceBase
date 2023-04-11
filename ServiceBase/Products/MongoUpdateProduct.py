from Products.ProductBase import Product


class MongoUpdateProduct(Product):
    def __init__(self, stream, source=None, product_type=None, **kwargs):
        Product.__init__(self, stream, source, product_type, **kwargs)

        self.update_fields = []
        self.append_fields = []
        self.id_fields = {}
