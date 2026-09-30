from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import pandas as pd


def convert_timestamp_to_epoch_seconds(timestamp):
    date_object = datetime.strptime(timestamp, "%d%m%Y-%H%M")
    return int(date_object.replace(tzinfo=ZoneInfo("Europe/Berlin")).timestamp())


def generate_parkhouse_data(aggregated_data_list):
    parkhouses_data = {}

    for raw_data in aggregated_data_list:
        timestamp = raw_data.get("timestamp", "")

        for parkhouse_info in raw_data.get("parkhouses", []):
            parkhouse_name = parkhouse_info.get("name").strip()

            if parkhouse_name not in parkhouses_data:
                parkhouses_data[parkhouse_name] = {
                    "name": parkhouse_name,
                    "occupation_data": [],
                }

            parkhouses_data[parkhouse_name]["occupation_data"].append(
                {
                    "timestamp": convert_timestamp_to_epoch_seconds(timestamp),
                    "free_spaces": parkhouse_info.get("free_spaces"),
                    "occupied_spaces": parkhouse_info.get("occupied_spaces"),
                    "max_spaces": parkhouse_info.get("max_spaces"),
                }
            )

    for parkhouse in parkhouses_data:
        parkhouses_data[parkhouse]["occupation_data"] = sorted(
            parkhouses_data[parkhouse]["occupation_data"],
            key=lambda item: item["timestamp"],
        )

    return parkhouses_data


def process_parkhouse_data(data):
    parkhouse_name = data["name"]
    occupation_data = data["occupation_data"]

    frame = pd.DataFrame(occupation_data)
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], unit="s")
    frame.set_index("timestamp", inplace=True)

    daily_max = frame.resample("D").max()
    daily_min = frame.resample("D").min()
    daily_data = pd.DataFrame(
        {
            "date": daily_max.index,
            "max_occupied_spaces": daily_max["occupied_spaces"],
            "min_free_spaces": daily_min["free_spaces"],
        }
    )

    return parkhouse_name, daily_data


def epoch_to_human(timestamp):
    return datetime.fromtimestamp(timestamp).strftime("%a. %d.%m - %H:%M")


def flatten_parkhouse_data(data):
    flat_data = [
        {
            "timestamp": epoch_to_human(entry["timestamp"]),
            "value": entry["occupied_spaces"],
        }
        for entry in data["occupation_data"]
    ]
    return pd.DataFrame(flat_data)


def epoch_to_hhmm(epoch_time):
    timestamp = datetime.fromtimestamp(epoch_time, timezone.utc).replace(tzinfo=None)
    return timestamp.isoformat()