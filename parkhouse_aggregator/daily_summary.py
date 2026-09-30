import pandas as pd


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