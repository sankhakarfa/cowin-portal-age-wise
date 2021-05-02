import requests
import json

STATE_LIST_URL = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
DISTRICT_LIST_URL = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}"


def main():
    r = requests.get(STATE_LIST_URL)
    full_state_list = r.json()["states"]
    for item in full_state_list:
        req = requests.get(DISTRICT_LIST_URL.format(item["state_id"]))
        data = req.json()
        with open('database/{}.json'.format(item["state_name"].lower()), 'w') as f:
            json.dump(data, f)

if __name__ == "__main__":
    main()