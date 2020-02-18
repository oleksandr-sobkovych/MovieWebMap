"""Build an html Web map."""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-


import geopy as gp
from geopy.distance import distance
from geopy.exc import GeocoderTimedOut
from mymodule.parsing import *
from mymodule.web_map_construction import *


def prompt_all_data(locator) -> tuple:
    """Prompt a user to input all necessary data.

    :param locator: to find a country by coordinates
    :return: a tuple of coordinates, country name, whether to generate json
    from scratch and a year string.
    """
    while True:
        try:
            generate = input("Generate file from scratch (may take longer than 3 minutes)(y/n): ")
            generate = generate.lower()
            if generate in "true yes y t 1":
                generate = True
            elif generate in "false no n f 0":
                generate = False
            else:
                raise AssertionError

            x = float(input("Enter your latitude:"))
            y = float(input("Enter your longitude:"))
            assert -85 <= x <= 85
            assert -180 <= y <= 180

            year = input("Enter the year: ")
            assert 1725 <= int(year) <= 2020
            same_country = locator.reverse((x, y), language="en").raw["address"]["country"]
            try:
                same_country = pcount.countries.search_fuzzy(same_country)[0].name
            except LookupError:
                break
            break
        except (ValueError, TypeError, AssertionError):
            print("Invalid input! Try again...")
            continue
        except (KeyError):
            same_country = False
            break

    return (x, y), same_country, generate, year


def main(verbose: bool = True):
    """Compose the map considering the input and json file.

    As a result, in the same directory a map appears.
    :param verbose: whether to print initial info
    :return: None
    """
    locator = gp.Nominatim(user_agent="alex", timeout=5)

    location, necessary_check, to_generate, year = prompt_all_data(locator)

    if to_generate:
        parse_file()
    data = read_from_json()
    data = data[year]

    webmap = setup()

    print("\nThere are {} countries too look through...\n\n".format(len(data)))
    closest = []
    for i, country in enumerate(data):
        try:
            center = locator.geocode(query=country, language="en")
            assert i < 400
        except GeocoderTimedOut:
            center = None
        except AssertionError:
            break
        if verbose:
            print("{}: {} -> {}".format(i+1, country, center))

        if center is not None:
            closest.append((country, center,
                            distance(location, (center.latitude, center.longitude))))
    closest = sorted(closest, key=lambda x: x[-1].miles)
    if len(closest) > 15:
        closest = closest[:16]
    if necessary_check:
        closest.insert(0, (necessary_check, None))
    print("\nWent through {} countries...\n\n".format(i+1))

    closest_places = []
    for country in closest:
        country = country[0]
        try:
            print()
            for i, place in enumerate(data[country]["place"]):
                try:
                    center = locator.geocode(query=place+", "+country, language="en")
                except TimeoutError:
                    center = None
                if verbose:
                    print("{}: {} -> {}".format(i+1, place, center))
                if center is not None:
                    closest_places.append((place, center, country,
                                          distance(location, (center.latitude, center.longitude))))
                    if i > 30:
                        break
        except KeyError:
            continue
    closest_places = sorted(closest_places, key=lambda x: x[-1].miles)
    if len(closest_places) > 10:
        closest_places = closest_places[:11]
    for place in closest_places:
        add_marker(webmap, place, tooltip='Click to see movies!', data=data)

    print("\nPlease check out file map.html")
    map_constr(webmap, location)


if __name__ == "__main__":
    main()
