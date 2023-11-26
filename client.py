import argparse
import logging
import os
import requests
import calendar

# Obtén un diccionario de números de mes a nombres de mes
meses_dict = {str(i): calendar.month_name[i] for i in range(1, 13)}

# Set logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('airports.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Read env vars related to API connection
AIRPORTS_API_URL = os.getenv("AIRPORTS_API_URL", "http://localhost:8000")


def print_airport(airport):
    for k in airport.keys():
        print(f"{k}: {airport[k]}")
    print("="*50)


def list_airports(country):
    suffix = "/travel/airports"
    endpoint = AIRPORTS_API_URL + suffix
    params = {
        "country": country
    }
    response = requests.get(endpoint, params=params)
    if response.ok:
        json_resp = response.json()
        for airport in json_resp:
            print_airport(airport)
    else:
        print(f"Error: {response}")


def list_optimal_advertising_months(airport_name, n_months):
    suffix = f"/travel/advertising-months/{airport_name}"
    endpoint = AIRPORTS_API_URL + suffix
    response = requests.get(endpoint)
    if response.ok:
        json_resp = response.json()
        months_print = json_resp[:n_months]
        print("=" * 50)
        print(f"Optimal advertising months for airport {airport_name}:")
        for i in months_print:
            print(f"\t- {meses_dict[i]}")
        print("=" * 50)
    else:
        print(f"Error: {response}")


def main():
    log.info(f"Welcome to airport advertising scheduler. App requests to: {AIRPORTS_API_URL}")
    list_of_actions = ["search", "get"]
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=list_of_actions,
                        help="Action to be user for the travel database")
    parser.add_argument("-c", "--country", help="Search airports in a country", default="USA")
    parser.add_argument("-a", "--airport", help="Provide an airport to see recommended months to advertising",
                        default=None)
    parser.add_argument("-n", "--nmonths", help="Select the number of months to recommend", default=3, type=int)
    args = parser.parse_args()
    if args.action == "search" and args.country:
        list_airports(args.country)
    elif args.action == "get" and args.airport:
        list_optimal_advertising_months(args.airport, args.nmonths)
    else:
        log.error("Not possible to do")
        exit(1)


if __name__ == "__main__":
    main()
