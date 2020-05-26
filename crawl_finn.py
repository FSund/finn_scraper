from scrapy.crawler import CrawlerProcess
from properties.spiders.finn_spider import FinnSpider
from scrapy.utils.project import get_project_settings
import argparse
import os.path


def make_and_model_to_finn_numbers(make_, model_):
    make = make_.lower().replace(" ", "")
    model = model_.lower().replace(" ", "")

    make_map = {
        'volvo': '818',
        'skoda': '808'
    }

    def model_to_finn(make_number, model):
        model_map = {}
        if make == "volvo":
            model_map = {
                'xc70': '7781',
                'v70': '3077',
                'v90': '2000386'
            }
        if make == "skoda":
            model_map = {
                'superb': '7532'
            }

        return model_map[model]

    make_number = make_map[make.lower()]
    model_number = model_to_finn(make_number, model.lower())

    return f"1.{make_number}.{model_number}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Scrape data about cars from Finn.no')
    parser.add_argument(
        '-f', '--force', action='store_true', dest='force_rebuild',
        help='Force database rebuild'
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
    # print(f"Make: {make}")
    # print(f"Model: {model}")

    # filename = make.lower() + "-" + model.lower().replace(" ", "_") + ".json"
    finn_number = make_and_model_to_finn_numbers(make, model)
    filename = f"vehicle-{finn_number}.json"
    # print(filename)

    if os.path.isfile(filename):
        if args.force_rebuild:
            print(f"Database for '{make} {model}' already exists. Doing (forced) rebuild.")
            # delete file
            with open(filename, "w") as f:
                pass
        else:
            print(f"Database for '{make} {model}' already exists. Use argument '--force'/'-f' to force rebuild.")
            exit(0)
    else:
        print(f"Building database for '{make} {model}'.")

    make_number = finn_number.split('.')[1]
    FinnSpider.start_urls = [
        # use &sales_form=1 to avoid leasing
        f"https://www.finn.no/car/used/search.html?filters=&make={make_number}&model={finn_number}&sales_form=1"
    ]

    # Run properties spider
    settings = get_project_settings()
    settings['FEED_FORMAT'] = "json"
    settings['FEED_URI'] = filename
    process = CrawlerProcess(settings)
    process.crawl(FinnSpider)
    process.start()
