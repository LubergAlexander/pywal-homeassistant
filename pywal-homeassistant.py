#!/usr/bin/env python3
import json
import requests

BASE_URL = "http://snowflake:8123"
TOKEN = "" # created a long lived token in HA
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
        headers={"Authorization": "Bearer {token}".format(token=TOKEN)},
    )


def set_light_color(entity_id, color, brightness_pct=30):
    return call_service(
        "light",
        "turn_on",
        {"entity_id": entity_id, "brightness_pct": brightness_pct, "rgb_color": color},
    )


def main():
    with open(WAL_CACHE_FILE, "r") as theme_file:
        theme = json.loads(theme_file.read())

    primary = hex_to_rgb(theme["colors"]["color1"])
    secondary = hex_to_rgb(theme["colors"]["color3"])
    third = hex_to_rgb(theme["colors"]["color5"])

    set_light_color("light.office_desk", primary, brightness_pct=40)
    set_light_color("light.nanoleaf", secondary, brightness_pct=70)


if __name__ == "__main__":
    main()
