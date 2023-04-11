from Devices.InputDevices.SplitCsvFolderInputDevice import SplitCsvFolderInputDevice
from Devices.OutputDevices.FolderOutputDevice import FolderOutputDevice
from Parsers.RegexExtractorParser import RegexExtractorParser
from Products.ExcelerProduct import ExcelerProduct
from Serilizers.CsvSeilizers import CsvSerializer
from Serilizers.jsonSeilizers import JsonSerializer
from ServiceBase import ServiceBase


def main():
    conf = {"inputDevices": [
        SplitCsvFolderInputDevice(CsvSerializer("(?P<source>\w+)_(?P<type>\w+).*"),
                                  "csv_files_input_device",
                                  "../queues/registration_csv_files")],
        "outputDevices": [FolderOutputDevice(JsonSerializer(), "post_parsing_output",
                                             "../queues/exceler_registration")],
        "badDevices": [FolderOutputDevice(JsonSerializer(), "bad_products", "../queues/bad")],
        "parserMapping": {
            "sales": {
                "profile": RegexExtractorParser(
                    {"LinkedIn Profile URL": {"re": "(?P<linkedin>.*)"},
                     "First Name": {"re": "(?P<first_name>.*)"},
                     "Last Name": {"re": "(?P<last_name>.*)"},
                     "Mobile": {"re": "(?P<mobile_number>.*)"},
                     "Email": {"re": "(?P<email>.*)"},
                     "Gender": {"re": "(?P<gender>.*)"},
                     "Age": {"re": "(?P<age>.*)", "lambda": lambda a: int(a)},
                     "College/University Name": {"re": "(?P<university>.*)"},
                     "Excel Alumni Year": {"re": "(?P<alumni_year>.*)"},
                     "Marital Status": {"re": "(?P<martial_status>.*)"},
                     "Mailing Address Line 1": {"re": "(?P<address>.*)"},
                     "Date Of Birth": {"re": "(?P<birthday>.*)"},
                     "ContactID": {"re": "(?P<salesforce_id>.*)"},
                     },
                    ExcelerProduct)
            }
        }
    }
    service = ServiceBase(conf)
    service.run()


if __name__ == '__main__':
    main()
