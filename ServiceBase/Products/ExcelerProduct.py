from datetime import datetime

from Products.ProductBase import Product


class ExcelerProduct(Product):
    def __init__(self, stream, source=None, product_type=None, linkedin=None, first_name=None, last_name=None,
                 birthday=None, mobile_number=None, email=None, gender=None, university=None, address=None,
                 alumni_year=None, martial_status=None, salesforce_id=None, **kwargs):
        Product.__init__(self, stream, source, product_type, **kwargs)

        self.registration_date = None
        self.product_name = None
        self.update_time = datetime.now()
        self.linkedin = linkedin
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = None
        self.mobile_number = mobile_number
        self.email = email
        self.gender = gender
        self.birthday = birthday
        self.university = university
        self.alumni_year = alumni_year
        self.martial_status = martial_status
        self.salesforce_id = salesforce_id
        self.address = address
        self.id_fields = {}
       
