import argparse
import csv
from datetime import datetime, timedelta
from random import choice, randint, randrange


airlines = ["American Airlines", "Delta Airlines", "Alaska", "Aeromexico", "Volaris"]
airports = ["PDX", "GDL", "CDMX", "SJC", "LAX", "JFK"]
airports_name = ["Portland", "Guadalajara", "Ciudad de México", "San Jose", "Los Angeles", "New York"]
airports_country = ["USA", "MEX", "MEX", "USA", "USA", "USA"]
genders = ["male", "female", "unspecified", "undisclosed"]
reasons = ["On vacation/Pleasure", "Business/Work", "Back Home"]
stays = ["Hotel", "Short-term homestay", "Home", "Friend/Family"]
transits = ["Airport cab", "Car rental", "Mobility as a service", "Public Transportation", "Pickup", "Own car"]
connections = [True, False]


def random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = randrange(days_between_dates)
    rand_date = start_date + timedelta(days=random_number_of_days)
    return rand_date


def generate_airports():
    with open("Airports.csv", "w") as ad:
        field_names = ["airport_id", "airport_name", "city", "country"]
        air_dict = csv.DictWriter(ad, fieldnames=field_names)
        air_dict.writeheader()
        for i in range(len(airports)):
            row = dict()
            row["airport_id"] = i
            row["airport_name"] = airports[i]
            row["city"] = airports_name[i]
            row["country"] = airports_country[i]
            air_dict.writerow(row)


def generate_campaigns(n_campaigns):
    with open("Campaigns.csv", "w") as ad:
        field_names = ["campaign_id", "airport_name", "year", "month"]
        camp_dict = csv.DictWriter(ad, fieldnames=field_names)
        camp_dict.writeheader()
        for i in range(n_campaigns):
            row = dict()
            row["campaign_id"] = i
            row["airport_name"] = choice(airports)
            date = random_date(datetime(2013, 1, 1), datetime(2023, 4, 25))
            row["year"] = date.year
            row["month"] = date.month
            camp_dict.writerow(row)


def generate_dataset(output_file, rows):
    with open(output_file, "w") as fd:
        fieldnames = ["airline", "from_airport", "to_airport", "day", "month", "year",
                      "age", "gender", "reason", "stay", "transit", "connection", "wait"]
        fp_dict = csv.DictWriter(fd, fieldnames=fieldnames)
        fp_dict.writeheader()
        for i in range(rows):
            from_airport = choice(airports)
            to_airport = choice(airports)
            while from_airport == to_airport:
                to_airport = choice(airports)
            date = random_date(datetime(2013, 1, 1), datetime(2023, 4, 25))
            reason = choice(reasons)
            stay = choice(stays)
            connection = choice(connections)
            wait = randint(30, 720)
            transit = choice(transits)
            if not connection:
                wait = 0
            else:
                transit = ""
            if reason == "Back Home":
                stay = "Home"
                connection = False
                wait = 0
                transit = choice(transits)
                
            line = {
                "airline": choice(airlines),
                "from_airport":  from_airport,
                "to_airport":  to_airport,
                "day": date.day,
                "month": date.month,
                "year": date.year,
                "age": randint(1, 90),
                "gender": choice(genders),
                "reason": reason,
                "stay": stay,
                "transit": transit,
                "connection": connection,
                "wait": wait,
            }
            fp_dict.writerow(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-o", "--output",
                        help="Specify the output filename of your csv, defaults to: flight_passengers.csv",
                        default="flight_passengers.csv")
    parser.add_argument("-r", "--rows", help="Amount of random generated entries for the dataset, defaults to: 100",
                        type=int, default=100)
    parser.add_argument("-c", "--campaigns",
                        help="Amount of random generated campaigns for the dataset, defaults to: 20",
                        type=int, default=20)
    args = parser.parse_args()
    
    print(f"Generating {args.rows} for flight passenger dataset")
    generate_dataset(args.output, args.rows)
    print(f"Generating {args.campaigns} for campaigns dataset")
    generate_campaigns(args.campaigns)
    print("Generating unique airports")
    generate_airports()
