from Devices.InputDevices.SplitCsvFolderInputDevice import SplitCsvFolderInputDevice
from Devices.OutputDevices.FolderOutputDevice import FolderOutputDevice
from Parsers.RegexExtractorParser import RegexExtractorParser
from Products.PatientProduct import PatientProduct
from Products.TreatmentProduct import TreatmentProduct
from Serilizers.CsvSeilizers import CsvSerializer
from Serilizers.jsonSeilizers import JsonSerializer
from ServiceBase import ServiceBase


def main():
    conf = {"inputDevices": [
        SplitCsvFolderInputDevice(CsvSerializer("(?P<source>\w+_\d+)_(?P<type>\w+).*"),
                                  "csv_files_input_device",
                                  "../../queues/csv_files")],
        "outputDevices": [FolderOutputDevice(JsonSerializer(), "post_parsing_output",
                                             "../../queues/parsed")],
        "badDevices": [FolderOutputDevice(JsonSerializer(), "bad_products", "../../queues/bad")],
        "parserMapping": {
            "hospital_2": {
                "Treatment": RegexExtractorParser(
                    {"PatientId": {"re": "(?P<patient_id>.*)"},
                     "ProtocolID": {"re": "(?P<protocol>.*)"},
                     "StartDate": {"re": "(?P<start_date>.*)"},
                     "EndDate": {"re": "(?P<end_date>.*)"},
                     "Status": {"re": "(?P<status>.*)"},
                     "DisplayName": {"re": "(?P<display_name>.*)"},
                     "AssociatedDiagnoses": {"re": "(?P<diagnoses>.*)"},
                     "NumberOfCycles": {"re": "(?P<cycles>.*)", "lambda": lambda a: int(a)},
                     "TreatmentId": {"re": "(?P<treatment_id>.*)"}},
                    TreatmentProduct),
                "Patient": RegexExtractorParser(
                    {"PatientId": {"re": "(?P<patient_id>.*)"},
                     "MRN": {"re": "(?P<mrn>.*)"},
                     "PatientDOB": {"re": "(?P<date_birth>.*)"},
                     "IsPatientDeceased": {"re": "(?P<is_deceased>.*)"},
                     "DateDeath": {"re": "(?P<date_death>.*)"},
                     "LastName": {"re": "(?P<last_name>.*)"},
                     "FirstName": {"re": "(?P<first_name>.*)"},
                     "Gender": {"re": "(?P<gender>.*)"},
                     "Sex": {"re": "(?P<sex>.*)"},
                     "AddressLine": {"re": "(?P<address>.*)"},
                     "AddressCity": {"re": "(?P<city>.*)"},
                     "AddressState": {"re": "(?P<state>.*)"},
                     "AddressZipCode": {"re": "(?P<zip_code>.*)"}},
                    PatientProduct)
            },
            "hospital_1": {
                "Treatment": RegexExtractorParser(
                    {"PatientID": {"re": "(?P<patient_id>.*)"},
                     "StartDate": {"re": "(?P<start_date>.*)"},
                     "EndDate": {"re": "(?P<end_date>.*)"},
                     "Active": {"re": "(?P<status>.*)"},
                     "DisplayName": {"re": "(?P<display_name>.*)"},
                     "Diagnoses": {"re": "(?P<diagnoses>.*)"},
                     "TreatmentLine": {"re": "(?P<treatment_line>.*)"},
                     "CyclesXDays": {"re": "(?P<cycles>\\d+)X", "lambda": lambda a: int(a)},
                     "TreatmentID": {"re": "(?P<treatment_id>.*)"}},
                    TreatmentProduct),
                "Patient": RegexExtractorParser(
                    {"PatientID": {"re": "(?P<patient_id>.*)"},
                     "MRN": {"re": "(?P<mrn>.*)"},
                     "PatientDOB": {"re": "(?P<date_birth>.*)"},
                     "IsDeceased": {"re": "(?P<is_deceased>.*)"},
                     "DOD_TS": {"re": "(?P<date_death>.*)"},
                     "LastName": {"re": "(?P<last_name>.*)"},
                     "FirstName": {"re": "(?P<first_name>.*)"},
                     "Gender": {"re": "(?P<gender>.*)"},
                     "Sex": {"re": "(?P<sex>.*)"},
                     "Address": {"re": "(?P<address>.*)"},
                     "City": {"re": "(?P<city>.*)"},
                     "State": {"re": "(?P<state>.*)"},
                     "ZipCode": {"re": "(?P<zip_code>.*)"},
                     "LastModifiedDate": {"re": "(?P<date_modified>.*)"}},
                    PatientProduct)
            },
        }}
    service = ServiceBase(conf)
    service.run()


# move config to file
# add log handlers


if __name__ == '__main__':
    main()
