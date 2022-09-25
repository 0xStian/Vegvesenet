import requests
import random
from threading import Thread

api_url = "https://www.vegvesen.no/ws/no/vegvesen/kjoretoy/felles/datautlevering/enkeltoppslag/kjoretoydata?kjennemerke="
regional_code = ["BT", "ZS", "RE", "RF", "RH", "RJ", "RK", "RL", "RN", "RP", "RR", "RS", "RT", "RU", "RV", "RX", "RY", "RW", "SC", "SD", "SE", "SF", "SH", "SJ", "SK", "SL", "RZ", "SA", "SB", "PX", "PY", "PZ", "RC", "RD", "PN", "PP", "PR", "PS", "PT", "PU", "PV", "RA", "RB", "DA", "DB", "DC", "DD", "DE", "DF", "DH", "DJ", "DK", "DL", "DN", "DP", "DR", "DS", "DT", "DU", "DV", "DX", "DY", "DZ", "EA", "EB", "EC", "ED", "EE", "EF", "EH", "EJ", "EK", "EN", "EP", "ER", "ES", "ET", "EU", "EV", "EX", "EY", "EZ"]
CAR_BRANDS = ["AUDI", "BMW", "CHEVROLET", "CITROEN", "DODGE", "FERRARI", "FIAT", "FISKER", "FORD", "HONDA", "HUMMER", "HYUNDAI", "INFINITI", "JAGUAR", "JEEP", "KIA", "LADA", "LAMBORGHINI", "LANCIA", "LAND ROVER", "LANDWIND", "LEXUS", "LOTUS", "MASERATI", "MAYBACH", "MAZDA", "MCLAREN", "MERCEDES-BENZ", "MITSUBISHI", "NISSAN", "OPEL", "PEUGEOT", "PORSCHE", "RENAULT", "ROVER", "SAAB", "SEAT", "SKODA", "SMART", "SSANGYONG", "SUBARU", "SUZUKI", "TESLA", "TOYOTA", "VOLKSWAGEN", "VOLVO"]
years = [1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
plates = open("plates.txt", "a")
request_limit = 0



def send_request(plate):
    headers = {"SVV-Authorization": "api-key"} # få api key her https://www.vegvesen.no/en/dinside/data-og-api-er/tilgang-til-api-for-kjoretoyopplysninger/
    response = requests.get(f"{api_url}{plate}", headers=headers)
    if response.status_code == 200:
        result = str(response.json())
        if result.find("politi") != -1:
            plates.write(f"{plate} politi\n")
            print(f"🚓 | {plate} | {find_car_production_year(result)} | {find_car_brand(result)}")
        else:
            print(f"❌ | {plate} | {find_car_production_year(result)} | {find_car_brand(result)}")


def generate_random_plate():
    five_letter_number = random.randrange(11111, 99999, 5)
    plate_generated = random.choice(regional_code) + str(five_letter_number)
    return plate_generated


def find_car_brand(result):
    for x in CAR_BRANDS:
        is_found = str(result.find(x))
        if int(is_found) != -1:
            return x


def find_car_production_year(result):
    for x in years:
        year = str(result.find(str(x)))
        if int(year) != -1:
            return x


def start_scanner():
    while True:
        send_request(generate_random_plate())


start_scanner()

threads = []
for n in range(1, 6):
    t = Thread(target=start_scanner())
    threads.append(t)
    t.start()


plates.close()
