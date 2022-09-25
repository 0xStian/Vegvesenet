import requests


api_key = "api-key" # https://www.vegvesen.no/en/dinside/data-og-api-er/tilgang-til-api-for-kjoretoyopplysninger/
api_url = "https://www.vegvesen.no/ws/no/vegvesen/kjoretoy/felles/datautlevering/enkeltoppslag/kjoretoydata?kjennemerke="
debug_info = False
reg_nr = input("Reg Nummer >")


def send_request():
    headers = {"SVV-Authorization": f"{api_key}"}
    response = requests.get(f"{api_url}{reg_nr}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Ikke Gyldig Skilt Nummer")
        if debug_info is True:
            print(response)
        exit()


result = str(send_request())

if result.find("politi") != -1:
    print("Bil tilhører politiet")

else:
    print("Bil tilhører ikke politiet")

if debug_info is True:
    print(result)
