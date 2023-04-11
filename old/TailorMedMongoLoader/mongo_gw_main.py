from Devices.InputDevices.FolderInputDevice import FolderInputDevice
from Devices.OutputDevices.FolderOutputDevice import FolderOutputDevice
from Devices.OutputDevices.MongoInsertOutputDevice import MongoInsertOutputDevice
from Parsers.ParserBase import ParserBase
from Serilizers.BsonSerillizer import BsonSerializer
from Serilizers.jsonSeilizers import JsonSerializer
from ServiceBase import ServiceBase


def main():
    conf = {"inputDevices": [
        FolderInputDevice(JsonSerializer(), "json_files_input_device", "../../queues/parsed")],
        "outputDevices": [MongoInsertOutputDevice(BsonSerializer(), "mongo_output",
                                            "mongodb+srv://excel:Data2023@cluster0.nhaxlrp.mongodb.net/?retryWrites=true&w=majority",
                                            "excel")],
        "badDevices": [FolderOutputDevice(JsonSerializer(), "bad_products", "../../queues/bad")],
        "parserMapping": {
            "hospital_2": {
                "Treatment": ParserBase(),
                "Patient": ParserBase()
            },
            "hospital_1": {
                "Treatment": ParserBase(),
                "Patient": ParserBase()
            },
        }}
    service = ServiceBase(conf)
    service.run()


# move config to file
# add log handlers


if __name__ == '__main__':
    main()
