from datetime import datetime

import pandas as pd


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