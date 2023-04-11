from Parsers.ParserBase import ParserBase
from Products.ProductBase import Product
from Products.csvProducts import CsvProduct

class IndiaLinkedinParser(ParserBase):
    def __init__(self, result_product_class: type):
        ParserBase.__init__(self)
        self.result_product_class = result_product_class
        self.job_fields_prefixes = ["company", "jobTitle", "jobDateRange", "companyUrl", "jobDescription",
                                    "jobLocation"]
        self.school_fields_prefixes = ["school", "schoolUrl", "schoolDegree", "schoolDescription", "schoolDateRange"]
        self.skill_prefix = "skill"
        self.interest_prefix = "interestGroup"
        self.volunteering_fields_prefix = ["volunteeringPosition", "volunteeringInstatution", "volunteeringField"]
        self.update_fields = ["fullName", "linkedinProfile", "firstName", "lastName", "headline", "location",
                              "description", "connectionCount"]

    def parse_set_to_list_from_string(self, data):
        if data.startswith("{"):
            data = eval(data)
        else:
            data = [data]
        data = list(data)
        data.remove("")
        data.remove("missing")
        return data
    
    def clean(self,value):
        value = value.lower()
        if value=="missing":
            value=""
        value = value.strip()
        value = value.strip("/")
        first_word = value.split(" ")[0]
        if value.endswith(first_word) and len(first_word) != len(value):
            value = value[:-len(first_word)]
        return value
    
    def parse(self, product_to_parse: CsvProduct):
        result_products = []

        for record in product_to_parse.records:

            for attr, value in record.items():
                value = self.clean(value)
                record[attr] = value
                
            result_product: Product = product_to_parse.clone(self.result_product_class)
            result_product.id_fields = {"linkedin": record.get("linkedinProfile"),
                                         "fullName": record.get("fullName").title()}
            result_product.append_fields = []
            result_product.update_fields = []
            for i in range(6):
                numeral = "" if i == 0 else str(i)

                job = {}
                for job_prefix in self.job_fields_prefixes:
                    job[job_prefix] = record.get(job_prefix + numeral)
                if any(job.values()):
                    result_product.append_fields.append({"jobs": job})

                school = {}
                for school_prefix in self.school_fields_prefixes:
                    school[school_prefix] = record.get(school_prefix + numeral)
                if any(school.values()):
                    result_product.append_fields.append({"schools": school})

                volunteer = {}
                for volunteer_prefix in self.volunteering_fields_prefix:
                    volunteer[volunteer_prefix] = record.get(volunteer_prefix + numeral)
                if any(volunteer.values()):
                    result_product.append_fields.append({"volunteering": volunteer})

                skill = record.get(self.skill_prefix + numeral)
                if skill:
                    result_product.append_fields.append({"skills": skill})

                interest = record.get(self.interest_prefix + numeral)
                if interest:
                    result_product.append_fields.append({"interests": interest})

            for field in self.update_fields:
                value = record.get(field)
                result_product.update_fields.append((field, value))

            result_product.__delattr__("records")
            result_products.append(result_product)
        return result_products
