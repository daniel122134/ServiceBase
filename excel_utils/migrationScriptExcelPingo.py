import pymongo
import requests

excel_connection_string = "mongodb+srv://excel:Data2023@cluster0.nhaxlrp.mongodb.net/?retryWrites=true&w=majority"
pingo_connection_string = "mongodb+srv://barbot:barbot@barbot.ury12.mongodb.net/barbot?retryWrites=true&w=majority"
pingo_url = "https://pingoapp.net/api/contacts/createContacts"


def main():
    excel_client = pymongo.MongoClient(excel_connection_string, tls=True, tlsAllowInvalidCertificates=True)
    db = excel_client["excel"]
    profiles_collection = db["profile"]
    profiles = profiles_collection.find({"salesforceListed": True})
    for profile in profiles:
        number = profile.get("mobileNumber", None)
        hebrew_first_name = profile.get("hebrewFirstName", None)
        hebrew_last_name = profile.get("hebrewLastName", None)
        english_first_name = profile.get("firstName", None)
        english_last_name = profile.get("lastName", None)
        if number is not None and hebrew_first_name is not None:
            if hebrew_last_name is None:
                hebrew_last_name = ""
            hebrew_name = hebrew_first_name + " " + hebrew_last_name
            data = {
                "apikey": "64e5fcd0f0110baa3ed9fda9",
                "contacts": {
                    number:
                        {
                            "tags": [
                                {"field": "firstname", "value": hebrew_first_name},
                                {"field": "lastname", "value": hebrew_last_name},
                                {"field": "name", "value": hebrew_name},
                                {"field": "englishfirstname", "value": english_first_name},
                                {"field": "englishlastname", "value": english_last_name},

                            ]
                        }},
                "countryCode": "IL"

            }
            headers = {
                "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImlvVmM1OEJINFFTQmZ5NnpldHZsdyJ9.eyJodHRwczovL3BpbmdvYXBwLm5ldC9lbWFpbCI6ImV2ZW50c2V4Y2VsQHRhZ2xpdGJyaS5nbG9iYWwiLCJpc3MiOiJodHRwczovL2Rldi03YWZwd2R2MnFhbXVkMXl6LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwMjc5NzgwOTE3MzEwMjQ1NDcxNyIsImF1ZCI6WyJodHRwczovL25vZGUtanMtYmFja2VuZC8iLCJodHRwczovL2Rldi03YWZwd2R2MnFhbXVkMXl6LnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2OTczNjczMzUsImV4cCI6MTY5NzQ1MzczNSwiYXpwIjoia01XV0JrMmlyYkFnem93SFpibTdsVDVxa0piN1F1ZjEiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOltdfQ.H4FWPZvd2aznF-Tk9pllqsDYkwyMaFvQ2AzUCyp7pDW6VRccubPqCBdKs7MWrrIDq__ivQST9qMkX2e01iepWIehrIRMmDQ_o3CDskRDxp5TQ_s-D_KkCkcoMjHUs9XbgXZdDrKMc9B7mSlNjmXQiGU5YKCNKnHdEGL16VoqsztdK-VuCFA7MakhvqiPQOBl9h_eaefvhIoYlFHok9Jnk9HeoHaFFWjcdCxcxy60hA9uK0MFiCWNsrsZKxu7oHVFva9Gwn5TJ-d1L0b8RDWMehNZs1uY0xAkWfTZnO53QpjWAXRkyNjzbtZTF87IkrTyhC0jZtx-D3EmcKePagdY1w"
            }
            response = requests.post(pingo_url, json=data, headers=headers)
            print(response.content)
            x = 5


if __name__ == '__main__':
    main()
