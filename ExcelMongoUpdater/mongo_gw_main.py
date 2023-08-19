from Devices.InputDevices.FolderInputDevice import FolderInputDevice
from Devices.InputDevices.SplitCsvFolderInputDevice import SplitCsvFolderInputDevice
from Devices.OutputDevices.FolderOutputDevice import FolderOutputDevice
from Devices.OutputDevices.MongoInsertOutputDevice import MongoInsertOutputDevice
from Devices.OutputDevices.MongoUpdateOutputDevice import MongoUpdateOutputDevice
from Parsers.IndiaLinkedinParser import IndiaLinkedinParser
from Parsers.ParserBase import ParserBase
from Parsers.RegexExtractorParser import RegexExtractorParser
from Products.ExcelerProduct import ExcelerProduct
from Products.MongoUpdateProduct import MongoUpdateProduct
from Serilizers.BsonSerillizer import BsonSerializer
from Serilizers.CsvSeilizers import CsvSerializer
from Serilizers.MongoUpdateSerializer import MongoUpdateSerializer
from Serilizers.SerilizerBase import Serializer
from Serilizers.jsonSeilizers import JsonSerializer
from Serilizers.listSerilizer import ListSerializer
from ServiceBase import ServiceBase
import logging


def main():
    conf = {"inputDevices": [
        SplitCsvFolderInputDevice(ListSerializer("(?P<source>[a-z|A-Z]+)_(?P<type>[a-z|A-Z]+)"),
                                  "csv_files_input_device",
                                  "../queues/csv_files/sales_and_linkedin"),
        SplitCsvFolderInputDevice(ListSerializer("(?P<name>.*).csv", "registration", "profile"),
                                  "csv_files_input_device",
                                  "../queues/csv_files/registrations")
    ],
        "outputDevices": [MongoUpdateOutputDevice(Serializer(), "mongo_output",
                                            "mongodb+srv://excel:Data2023@cluster0.nhaxlrp.mongodb.net/?retryWrites=true&w=majority",
                                            "excel", [{"name": "linkedin",
                                                       "type" : str},
                                                      {"name": "email",
                                                       "type" : str},
                                                      {"name": "mobileNumber",
                                                       "type" : str},
                                                      {"name": "reportedEmails",
                                                       "type" : list,
                                                       "valueSource": "email"},
                                                      {"name": "fullName",
                                                       "type" : str},
                                                      {"name": "reportedNames",
                                                       "type" : list,
                                                       "valueSource": "fullName"},
                                                      ])],
        "badDevices": [FolderOutputDevice(JsonSerializer(), "bad_products", "../queues/bad")],
        "parserMapping": {
            "linkedin": {
                "profile": IndiaLinkedinParser(MongoUpdateProduct)
            },
            "sales": {
                "profile": RegexExtractorParser(
                    {"LinkedIn Profile URL": {"re": "(?P<linkedin>.*)"},
                     "First Name": {"re": "(?P<first_name>.*)"},
                     "Last Name": {"re": "(?P<last_name>.*)"},
                     "Mobile": {"re": "(?P<mobile_number>.*)"},
                     "Email": {"re": "(?P<email>.*)"},
                     "Gender": {"re": "(?P<gender>.*)"},
                     "College/University Name": {"re": "(?P<university>.*)"},
                     "Excel Alumni Year": {"re": "(?P<alumni_year>.*)"},
                     "Marital Status": {"re": "(?P<martial_status>.*)"},
                     "Mailing Address Line 1": {"re": "(?P<address>.*)"},
                     "Date of Birth": {"re": "(?P<birthday>.*)"},
                     "ContactID": {"re": "(?P<salesforce_id>.*)"},
                     "Hebrew First Name": {"re": "(?P<hebrew_first_name>.*)"},
                     "Hebrew Last Name": {"re": "(?P<hebrew_last_name>.*)"},
                     "Listed In Salesforce": {"re": "(?P<salesforce_listed>.*)", "lambda" : lambda x: x == "yes"},
                     },
                    ExcelerProduct)
            },
            "registration": {
                "profile": RegexExtractorParser(
                    {"LinkedIn Profile URL": {"re": "(?P<linkedin>.*)"},
                     "Your LinkedIn account": {"re": "(?P<linkedin>.*)"},
                     "Linkedin link": {"re": "(?P<linkedin>.*)"},
                     "First Name": {"re": "(?P<first_name>.*)"},
                     "Last Name": {"re": "(?P<last_name>.*)"},
                     "Mobile": {"re": "(?P<mobile_number>.*)"},
                     "Cell Phone Number:": {"re": "(?P<mobile_number>.*)"},
                     "Phone number": {"re": "(?P<mobile_number>.*)"},
                     "What phone number should we use to reach out to you?": {"re": "(?P<mobile_number>.*)"},
                     "Phone #": {"re": "(?P<mobile_number>.*)"},
                     "Phone": {"re": "(?P<mobile_number>.*)"},
                     "Email": {"re": "(?P<email>.*)"},
                     "Email address": {"re": "(?P<email>.*)"},
                     "What is your email address?": {"re": "(?P<email>.*)"},
                     "What Email address should we use to contact you?": {"re": "(?P<email>.*)"},
                     "Gender": {"re": "(?P<gender>.*)"},
                     "Gender_hebrew": {"re": "(?P<gender_hebrew>.*)"},
                     "College/University Name": {"re": "(?P<university>.*)"},
                     "University": {"re": "(?P<university>.*)"},
                     "Excel Alumni Year": {"re": "(?P<alumni_year>\d*)"},
                     "What is your cohort?": {"re": "(?P<alumni_year>\d*)"},
                     "What cohort are you?": {"re": "(?P<alumni_year>\d*)"},
                     "Birthright Israel Excel Participation Year (2011-2018):": {"re": "(?P<alumni_year>\d*)"},
                     "Excel Year": {"re": "(?P<alumni_year>\d*)"},
                     "Marital Status": {"re": "(?P<martial_status>.*)"},
                     "Mailing Address Line 1": {"re": "(?P<address>.*)"},
                     "Date of Birth": {"re": "(?P<birthday>.*)"},
                     "ContactID": {"re": "(?P<salesforce_id>.*)"},
                     "Hebrew First Name": {"re": "(?P<hebrew_first_name>.*)"},
                     "Hebrew Last Name": {"re": "(?P<hebrew_last_name>.*)"},
                     "Submit Date (UTC)": {"re": "(?P<registration_date>.*)"},
                     "Timestamp": {"re": "(?P<registration_date>.*)"},
                     "Global or Israeli Fellow?": {"re": "(?P<excel_community>.*)"},
                     "Name": {"re": "(?P<full_name>.*)"},
                     "Full name": {"re": "(?P<full_name>.*)"},
                     "What is your full name?": {"re": "(?P<full_name>.*)"},
                     "Where are you from?": {"re": "[^\d]*(?P<alumni_year>\d*)"},
                     "Company": {"re": "(?P<company>.*)"},
                     "Current Company (if applicable):": {"re": "(?P<company>.*)"},
                     "Workplace and position": {"re": "(?P<current_position>.*)"},
                     "Job": {"re": "(?P<current_position>.*)"},
                     "Position": {"re": "(?P<current_position>.*)"},
                     "Any dietary restrictions": {"re": "(?P<dietary_restrictions>.*)"},
                     "Dietary restrictions": {"re": "(?P<dietary_restrictions>.*)"},
                     "Please indicate any dietary requirements if any:": {"re": "(?P<dietary_restrictions>.*)"},
                     "Excel Cohort": {"re": "(?P<alumni_year>\d*)"},
                     "Excel class": {"re": "(?P<alumni_year>\d*)"},
                     "Cohort": {"re": "(?P<alumni_year>\d*)"},
                     "What's your preferred drink": {"re": "(?P<favorite_drink>.*)"},
                     "Rooming preferences": {"re": "(?P<rooming_preferences>.*)"},
                     "Current City:": {"re": "(?P<city>.*)"},
                     "City": {"re": "(?P<city>.*)"},
                     "City_hebrew": {"re": "(?P<city_hebrew>.*)"},
                     "Current Industry (if applicable):": {"re": "(?P<industry>.*)"},
                     "Working sector": {"re": "(?P<industry>.*)"},
                     "Sector": {"re": "(?P<industry>.*)"},
                     "Current Job lower (if applicable):": {"re": "(?P<job_lower>.*)"},
                     "Vegan? ": {"re": "(?P<is_vegan>.*)"},
                     "How many kids do you have?": {"re": "(?P<kids_count>.*)"},
                     "years of work at 2020": {"re": "(?P<experience_year_count_by_2020>.*)"},
                     "years of work at 2018": {"re": "(?P<experience_year_count_by_2018>.*)"},
                     "years of work at 2017": {"re": "(?P<experience_year_count_by_2017>.*)"},
                     "Where would you like to work? ": {"re": "(?P<workplace_desire>.*)"},
                     "Short bio about yourself": {"re": "(?P<short_bio>.*)"},
                     "excel board title": {"re": "(?P<excel_board_title>.*)"},
                     "Academic Status": {"re": "(?P<academic_status>.*)"},
                     "What are you studying": {"re": "(?P<field_of_study>.*)"},
                     },
                    ExcelerProduct)
            }
        }
    }
    service = ServiceBase(conf)
    service.run()


if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    main()
