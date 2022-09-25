import requests

api_key = "api-key" # logg inn og få api key her https://www.vegvesen.no/en/dinside/data-og-api-er/tilgang-til-api-for-kjoretoyopplysninger/
api_url = "https://www.vegvesen.no/ws/no/vegvesen/kjoretoy/felles/datautlevering/enkeltoppslag/kjoretoydata?kjennemerke="

def ALPR(image):
    regions = ['no']
    try:
        with open(f'{image}', 'rb') as fp:
            response = requests.post(
                'https://api.platerecognizer.com/v1/plate-reader/',
                data=dict(regions=regions),  # Optional
                files=dict(upload=fp),
                headers={'Authorization': 'Token api-key'}) # registrer og bytt "api-key" med din api key https://platerecognizer.com/

        api_result = response.json()
        filtered_result = api_result['results']

        for x in filtered_result:
            plate_number = x['plate']
            return str(plate_number)
    except:
        print("error with opening image")
        exit()


def send_request(reg_nr):
    headers = {"SVV-Authorization": f"{api_key}"}
    response = requests.get(f"{api_url}{reg_nr}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Ikke Gyldig Skilt Nummer")
        return


while True:
    bilde_av_bil = input(">")
    ALPR_return = ALPR(bilde_av_bil)
    result = str(send_request(ALPR_return))

    if result.find("politi") != -1:
        print(f"{ALPR_return} | Tilhører Politiet")

    else:
        print(f"{ALPR_return} | Tilhører ikke Politiet")
