import os
import json

from parkhouse_aggregator.daily_summary import process_parkhouse_data as process_json_file


def read_json_file(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


def main():
    all_parkhouses_data = {}
    data_directory = "parkhouse_data"

    for filename in os.listdir(data_directory):
        if filename.endswith(".json"):
            file_path = os.path.join(data_directory, filename)
            data = read_json_file(file_path)
            parkhouse_name, daily_data = process_json_file(data)
            all_parkhouses_data[parkhouse_name] = daily_data

    for parkhouse_name, daily_data in all_parkhouses_data.items():
        print(f"Parkhouse: {parkhouse_name}")
        print(daily_data.head())
        break

    for parkhouse_name, daily_data in all_parkhouses_data.items():
        daily_data.to_csv(f"{data_directory}/{parkhouse_name}_daily_data.csv", index=False)


if __name__ == "__main__":
    main()
