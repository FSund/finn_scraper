import json
import numpy as np
import matplotlib.pyplot as plt
import argparse
from crawl_finn import make_and_model_to_finn_numbers

def plot_the_stuff(filename, min_year, max_year, min_mileage, max_mileage):
    with open(filename) as f:
        cars = json.load(f)

    data = []
    filtered_cars = []
    for car in cars:
        if car['mileage'] < max_mileage and car['mileage'] > min_mileage:
            if car['year'] <= max_year and car['year'] >= min_year:
                data.append([car['price'], car['mileage'], car['year']])
                filtered_cars.append(car)

    data = np.asarray(data)

    ## plot price (y) vs. kilometer (x) with different colors per year
    # sort data by both year (first) and mileage (second)
    ind = np.lexsort((data[:, 1], data[:, 2]))
    sorted_data = data[ind]
    
    # 
    plt.figure()
    datas = []
    min_year_actual = max(min_year, min(data[:, 2]))
    max_year_actual = min(max_year, max(data[:, 2]))
    for year in range(min_year_actual, max_year_actual+1):
        cars = sorted_data[np.where(sorted_data[:,2] == year)]
        datas.append(cars)

        plt.plot(cars[:, 1], cars[:, 0], "-o", label=f"Årsmod. {year}")
    plt.legend()
    plt.ylabel("Pris [kr]")
    plt.xlabel("Kilometer")
    plt.tight_layout()
    plt.grid()
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Plot car data scraped from Finn.no')
    parser.add_argument(
        '--years', '-y', action='store', nargs=2,
        default=[0, 9999],
        help='Year range (inclusive)'
    )
    parser.add_argument(
        '--mileage', '-m', action='store', nargs=2,
        default=[0, 10000000],
        help='Mileage range (inclusive)'
    )
    parser.add_argument(
        'make', action='store',
        help='Car make/brand (Volvo, Ford etc.)'
    )
    parser.add_argument(
        'model', action='store',
        help='Car model (V70, Mondeo etc.)'
    )

    args, remainder = parser.parse_known_args()

    make = args.make

    # use remainder in case model name contains spaces
    model = args.model + ' ' + ' '.join(remainder)
    # remove quotes in case user tried to use quoted strings to pass model name
    # with spaces in it (using quoted strings doesn't help with argparse)
    model = model.replace("'", "")
    model = model.replace('"', "")

    finn_number = make_and_model_to_finn_numbers(make, model)
    filename = f"vehicle-{finn_number}.json"

    min_year = int(args.years[0])
    max_year = int(args.years[1])
    min_mileage = int(args.mileage[0])
    max_mileage = int(args.mileage[1])

    plot_the_stuff(filename, min_year, max_year, min_mileage, max_mileage)