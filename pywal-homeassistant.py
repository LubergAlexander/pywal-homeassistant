#!/usr/bin/env python3
import json
import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "http://homeassistant:8123"
PASSWORD = "CHANGEME"
WAL_CACHE_FILE = "/home/alex/.cache/wal/colors.json"


def hex_to_rgb(value):
    value = value.lstrip("#")
    lv = len(value)

    return tuple(int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3))


def call_service(domain, service, data):
    return requests.post(
        "{base_url}/api/services/{domain}/{service}".format(
            base_url=BASE_URL, service=service, domain=domain
        ),
        json=data,
        headers={"X-HA-Access": PASSWORD},
    )


def set_light_color(entity_id, color, brightness_pct=60):
    return call_service(
        "light",
        "turn_on",
        {"entity_id": entity_id, "brightness_pct": brightness_pct, "rgb_color": color},
    )


def main():
    with open(WAL_CACHE_FILE, "r") as theme_file:
        theme = json.loads(theme_file.read())

    primary = hex_to_rgb(theme["colors"]["color3"])
    secondary = hex_to_rgb(theme["colors"]["color1"])

    set_light_color("light.officedesk", primary)
    set_light_color("light.aurora", secondary)


if __name__ == "__main__":
    main()
