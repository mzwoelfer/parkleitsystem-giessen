from datetime import datetime
from zoneinfo import ZoneInfo


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