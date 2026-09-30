import os
import json
import logging

from parkhouse_aggregator.history import (
    PARKHOUSE_NAME_ALIASES,
    convert_timestamp_to_epoch_seconds,
    generate_parkhouse_data,
)


def aggregate_parkhouse_data(data_dir):
    data_files = [
        path for path in list_files_in_directory(data_dir) if path.endswith(".json")
    ]
    snapshots = [read_json_file(path) for path in data_files]
    return generate_parkhouse_data(snapshots)


def list_files_in_directory(data_dir):
    file_paths = [os.path.join(data_dir, filename) for filename in os.listdir(data_dir)]
    return file_paths


def read_json_file(json_path):
    with open(json_path) as json_file:
        json_data = json.load(json_file)
    return json_data


def create_parkhouse_data_folder(data_dir="parkhouse_data"):
    module_dir = os.path.dirname(os.path.dirname(__file__))
    parkhouse_data_dir = os.path.join(module_dir, data_dir)

    if os.path.exists(path=parkhouse_data_dir) and os.path.isdir(data_dir):
        logging.info(f"{data_dir} already exists")
        return

    os.makedirs(name=parkhouse_data_dir, exist_ok=True)
    return


def export_parkhouse_data(data_directory, parkhouses_data):
    for parkhouse in parkhouses_data.keys():
        export_filename = f"{parkhouse.lower()}.json"
        export_path = os.path.join(data_directory, export_filename)
        with open(export_path, mode="w") as export_file:
            json.dump(parkhouses_data[parkhouse], export_file)

        if parkhouse == "Neustädter":
            for alias in PARKHOUSE_NAME_ALIASES:
                alias_filename = f"{alias}.json"
                if alias_filename != export_filename:
                    alias_path = os.path.join(data_directory, alias_filename)
                    if os.path.isfile(alias_path):
                        os.remove(alias_path)
    return


def main():
    logging.basicConfig(level=logging.INFO)

    module_dir = os.path.dirname(os.path.dirname(__file__))
    data_directory = os.path.join(module_dir, "data/")

    create_parkhouse_data_folder("parkhouse_data")

    parkhouses_data = aggregate_parkhouse_data(data_directory)

    export_parkhouse_data("parkhouse_data", parkhouses_data)
    return


if __name__ == "__main__":
    main()
