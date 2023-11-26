import csv
import requests

BASE_URL = "http://localhost:8000"


def load_air():
    with open("Data/Airports.csv") as fd:
        airports_csv = csv.DictReader(fd)
        for airport in airports_csv:
            del airport["airport_id"]
            x = requests.post(BASE_URL+"/travel/airports", json=airport)
            if not x.ok:
                print(f"Failed to post airport {x} - {airport}")


def load_camp():
    with open("Data/Campaigns.csv") as fd:
        camps_csv = csv.DictReader(fd)
        for camp in camps_csv:
            del camp["campaign_id"]
            x = requests.post(BASE_URL + "/travel/campaigns", json=camp)
            if not x.ok:
                print(f"Failed to post campaign {x} - {camp}")


def load_travels():
    with open("Data/flight_passengers.csv") as fd:
        travels_csv = csv.DictReader(fd)
        for travel in travels_csv:
            x = requests.post(BASE_URL + "/travel/travels", json=travel)
            if not x.ok:
                print(f"Failed to post travel {x} - {travel}")


if __name__ == "__main__":
    # Mandamos ejecutar las cargas de datos
    load_air()
    load_camp()
    load_travels()
