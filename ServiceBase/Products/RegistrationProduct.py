from Products.ProductBase import Product


class RegistrationProduct(Product):
    def __init__(self, stream, source=None, product_type=None, linkedin=None, first_name=None, last_name=None,
                 date_birth=None, mobile_number=None, email=None, gender=None, university=None, address=None,
                 alumni_year=None, martial_status=None, **kwargs):
        Product.__init__(self, stream, source, product_type, **kwargs)

        self.linkedin = linkedin
        self.first_name = first_name
        self.last_name = last_name
        self.mobile_number = mobile_number
        self.email = email
        self.gender = gender
        self.date_birth = date_birth
        self.university = university
        self.alumni_year = alumni_year
        self.martial_status = martial_status
        self.address = address
