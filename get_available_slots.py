#!/usr/bin/env python3
"""
Author: Sankha Karfa
Date: 02-May-2021

This script is used to generate slots availability based on cowin public api
"""
import sys
import requests
import json
from prettytable import PrettyTable
import datetime
import argparse


STATE_LIST_URL = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
DISTRICT_LIST_URL = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}"
DAILY_PINCODE_URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={}&date={}"
DAILY_DISTRICT_URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={}&date={}"
CALENDAR_BY_DISTRICT_URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}"
CALENDAR_BY_PINCODE_URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}"
DAILY_KEY = "sessions"
CALENDAR_KEY = "centers"


bcolors = {
    "BLACK": "\033[0;30m",
    "WHITE": "\033[0;37m",
    "HEADER": "\033[95m",
    "OKBLUE": "\033[94m",
    "OKCYAN": "\033[96m",
    "OKGREEN": "\033[92m",
    "WARNING": "\033[93m",
    "FAIL": "\033[91m",
    "ENDC": "\033[0m",
    "BOLD": "\033[1m",
    "UNDERLINE": "\033[4m",
}


class VaccineCenter:
    """
    Vaccine Center Class to store relevant data
    """

    def __init__(self, vaccine_center_data, daily=False):
        self._vaccine_center_data = vaccine_center_data
        self._age_slots = {"18": [], "45": []}
        self._slots = {}
        self._vaccine_type = [""]
        self._daily = daily
        self._min_age = 45
        self._check_availability()

    def get_min_age(self):
        return self._min_age

    def get_fee_type(self):
        return self._vaccine_center_data["fee_type"]

    def get_vaccine_type(self):
        return "".join(self._vaccine_type)

    def get_key(self, key):
        return self._vaccine_center_data[key]

    def get_slots_by_age(self, age):
        return self._age_slots[str(age)]

    def get_slots(self):
        return self._slots

    def get_slots_formatted(self):
        return ", ".join([f"{key}: {value}" for key, value in self._slots.items()])

    def get_slots_by_age_formatted(self, age):
        return " | ".join(self._age_slots[str(age)])

    def _check_availability(self):
        if self._daily:
            slots = self._vaccine_center_data
            self._min_age = min(self._min_age, int(slots["min_age_limit"]))
            self._slots[slots["date"]] = slots["available_capacity"]
            self._age_slots[str(slots["min_age_limit"])].extend(self._slots)
            self._age_slots[str(slots["min_age_limit"])].append(
                "> {}".format(slots["available_capacity"])
            )
            self._vaccine_type.append(slots["vaccine"])
        else:
            slots = self._vaccine_center_data["sessions"]
            for slot in slots:
                self._min_age = min(self._min_age, int(slot["min_age_limit"]))
                self._slots[slot["date"]] = slot["available_capacity"]
                if slot["available_capacity"] > 0:
                    self._age_slots[str(slot["min_age_limit"])].append(
                        "{} > {:03}".format(
                            slot["date"].replace("-2021", ""),
                            int(slot["available_capacity"]),
                        )
                    )
                    self._vaccine_type.append(slot["vaccine"])
                else:
                    self._booked = True
        self._vaccine_type = set(self._vaccine_type)


def get_slots_by_pincode(args):
    search_key = CALENDAR_KEY
    if args.daily:
        req = requests.get(DAILY_PINCODE_URL.format(args.pincode, args.date))
        search_key = DAILY_KEY
    else:
        req = requests.get(CALENDAR_BY_PINCODE_URL.format(args.pincode, args.date))
    if req.status_code == 400:
        print(req.json()["error"])
        return
    else:
        centers_data = req.json()[search_key]
        filter_and_print_center_list(centers_data, args, by_district=False)


def get_slots_by_district(args):
    """
    Retrieve and print slots when state district is mentioned
    """
    state = args.state.lower()
    district = args.district.lower()
    district_id = None
    state_id = None
    search_key = CALENDAR_KEY
    # Check for State and District from the prefetched json files
    with open("database/states.json") as json_file:
        states_data = json.load(json_file)["states"]
        state_table = PrettyTable(["Id", "State"])
        for state_item in states_data:
            state_table.add_row([state_item["state_id"], state_item["state_name"]])
            if state == state_item["state_name"].lower():
                state_id = state_item["state_id"]
                with open(
                    "database/{}.json".format(state_item["state_name"].lower())
                ) as district_file:
                    district_data = json.load(district_file)["districts"]
                    district_table = PrettyTable(["Id", "District"])
                    for district_item in district_data:
                        district_table.add_row(
                            [
                                district_item["district_id"],
                                district_item["district_name"],
                            ]
                        )
                        if district == district_item["district_name"].lower():
                            district_id = district_item["district_id"]
                            break
                    if district_id is None:
                        print(
                            "Please enter the correct District for {}:".format(
                                state_item["state_name"]
                            )
                        )

                        print(district_table)
                        return
                break
        if state_id is None:
            print("Please enter the correct state mentioned below:")
            print(state_table)
            return

    # Format the Url with district id and formatted date
    if args.daily:
        req = requests.get(DAILY_DISTRICT_URL.format(district_id, args.date))
        search_key = DAILY_KEY
    else:
        req = requests.get(CALENDAR_BY_DISTRICT_URL.format(district_id, args.date))
    # Check for any API error
    if req.status_code == 400:
        print(req.json()["error"])
        return
    # Store the list of centers
    centers_data = req.json()[search_key]
    filter_and_print_center_list(centers_data, args)


def filter_and_print_center_list(centers_data, options=[], by_district=True):
    title = ""
    first_text = "Next 7 Days Vaccine Slots"
    end_format = bcolors["ENDC"]
    if options.daily:
        first_text = "Daily Vaccine Slots"
    if options.all_centers:
        first_text = "Showing Centers allowing Vaccines"

    center_list = []
    objective = "on" if options.daily else "from"
    for center in centers_data:
        center_list.append(VaccineCenter(center, options.daily))

    center_list_table = PrettyTable(
        ["Center Name", "Fee", "Location", "Pincode", "Slots"]
    )
    html_list_table = PrettyTable(
        ["Center Name", "Min Age", "Fee", "Vaccine", "Location", "Pincode", "Slots"]
    )
    for center in center_list:
        if (len(center.get_slots_by_age(options.min_age)) > 0) or options.all_centers:

            name_colors = (
                bcolors["OKGREEN"]
                if len(center.get_slots_by_age(options.min_age)) > 0
                else bcolors["FAIL"]
            )
            fee_colors = bcolors["OKBLUE"] if "Paid" in center.get_fee_type() else ""
            center_list_table.add_row(
                [
                    "{}{}{}".format(name_colors, center.get_key("name"), end_format),
                    "{}{}{}".format(fee_colors, center.get_fee_type(), end_format),
                    center.get_key("block_name"),
                    center.get_key("pincode"),
                    center.get_slots_by_age_formatted(options.min_age),
                ]
            )
        if options.output_html is not None:
            html_list_table.add_row(
                [
                    center.get_key("name"),
                    center.get_min_age(),
                    center.get_fee_type(),
                    center.get_vaccine_type(),
                    center.get_key("block_name"),
                    center.get_key("pincode"),
                    center.get_slots_formatted(),
                ]
            )

    center_list_table.sortby = "Location"
    center_list_table.align["Center Name"] = "l"
    center_list_table.align["Slots"] = "l"
    if by_district:
        title = "\n\n{}{} for Age: {} yrs+ State: {} District: {} {} {} {}".format(
            bcolors["WARNING"],
            first_text,
            options.min_age,
            options.state.capitalize(),
            options.district.capitalize(),
            objective,
            options.date,
            end_format,
        )
        print(title)
    else:
        title = "\n\n{}{} for Age: {} yrs+ Pincode {} {} {} {}".format(
            bcolors["WARNING"],
            first_text,
            options.min_age,
            options.pincode,
            objective,
            options.date,
            end_format,
        )
        print(title)
    print(center_list_table)

    if options.output_html is not None:
        if not options.output_html.endswith(".html"):
            options.output_html = options.output_html + ".html"
        with open(options.output_html, "w") as html_file:
            template = (
                "<html><head><title>{}</title></head><body><h1>{}</h1>{}</html>".format(
                    first_text, title, html_list_table.get_html_string()
                )
            )
            template = template.replace(end_format, "")
            template = template.replace(bcolors["WARNING"], "")
            html_file.write(template)


def my_date_type(arg_value, format="%d-%m-%Y"):
    if not datetime.datetime.strptime(arg_value, format):
        # Date has to be in dd-mm-yyyy format
        raise argparse.ArgumentTypeError
    return arg_value


def parse_args():
    parser = argparse.ArgumentParser(
        description="Options to run this Co-WIN Vaccine Slot availability"
    )
    parser.add_argument("--state", type=str, default="", help="State")
    parser.add_argument("--district", type=str, default="", help="District")
    parser.add_argument("--pincode", type=int, default=0, help="Area pincode")
    parser.add_argument(
        "--daily", default=False, action="store_true", help="Get input dates data"
    )
    parser.add_argument(
        "--all-centers",
        default=False,
        action="store_true",
        help="Show all centers irrespective of availability",
    )
    parser.add_argument(
        "--date",
        type=my_date_type,
        default=datetime.date.today().strftime("%d-%m-%Y"),
        help="Date in dd-mm-yyyy",
    )
    parser.add_argument(
        "--min-age", type=int, default=18, help="Min Age Limit [Default is 18]"
    )
    parser.add_argument(
        "--output-html", type=str, default=None, help="Output html to OUTPUT_HTML file "
    )
    args = parser.parse_args()

    return args, parser.print_help


if __name__ == "__main__":
    ARGS, HELP = parse_args()
    if len(sys.argv) == 1:
        HELP()
        exit()
    else:
        # Check for Minimum Age
        if ARGS.min_age >= 18 and ARGS.min_age < 45:
            ARGS.min_age = 18
        elif ARGS.min_age >= 45:
            ARGS.min_age = 45
        else:
            print("Minimum Age has to be 18")
            exit()

    if ARGS.pincode > 9999:
        get_slots_by_pincode(ARGS)
    else:
        get_slots_by_district(ARGS)
