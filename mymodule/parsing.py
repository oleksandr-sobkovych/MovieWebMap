"""Handle list file parsing and json file reading and writing."""
"""Build an html Web map."""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-


import pycountry as pcount
import json


def parse_file(name: str = "test_locations.list", out: str = "locations_data.txt"):
    """Read a list file and write its contents into a json file.

    json file's structure is:
    {year:
        {country:
            {"lat", "long", "place":
                {place: "lat", "long", "name":
                    {movie:
                        [lat, long]
                    }
                }
            }
        }
    }
    :param out:
    :param name: name of the file
    """
    locations = {}
    memo = {"UK": "United Kingdom", "UAE": "United Arabic Emirates"}
    print("Generating...")

    with open(name) as file:
        for i, line in enumerate(file):
            if (i+1) % 50000 == 0:
                print("Got through {} lines...".format(i+1))
            line = line.strip("\n").split("\t")
            if not (line[-1].isprintable() and line[-2].isprintable()):
                continue

            if "(" in line[-1]:
                line = [line[0], line[-2]]
            else:
                line = [line[0], line[-1]]

            line[0] = line[0].split(" (")
            year = line[0][1][:4]
            if not year.isnumeric():
                year = line[0][-1][:4]
                if not year.isnumeric():
                    continue

            movie = line[0][0]

            line = line[-1].split(", ")

            if line[-1] in memo:
                country = memo[line[-1]]
            else:
                try:
                    country = pcount.countries.search_fuzzy(line[-1])[0].name
                except LookupError:
                    country = line[-1]
                memo[line[-1]] = country

            city = ", ".join(line)

            if year not in locations:
                locations[year] = {}
            if country not in locations[year]:
                locations[year][country] = {"lat": None,
                                            "long": None,
                                            "place": {}}
            if city not in locations[year][country]["place"]:
                locations[year][country]["place"][city] = {"lat": None,
                                                           "long": None,
                                                           "name": {}}
            locations[year][country]["place"][city]["name"].setdefault(movie, [])

    with open(out, "w+") as outfile:
        json.dump(locations, outfile)


def read_from_json(name: str = "locations_data.txt") -> dict:
    """Read data from json file.

    json file's structure is:
    {year:
        {country:
            {"lat", "long", "place":
                {place: "lat", "long", "name":
                    {movie:
                        [lat, long]
                    }
                }
            }
        }
    }
    :param name: name of the json file
    :return: a dictionary from json
    """
    with open(name) as json_file:
        return json.load(json_file)


def write_to_json(database: dict, name: str = "locations_data.txt"):
    """Write data to a jsi=on file.

    :param database: data to be written
    :param name: name of the file
    :return: None
    """
    with open(name, "w+") as outfile:
        json.dump(database, outfile)