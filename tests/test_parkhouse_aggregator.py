import json
import tempfile
import unittest
from pathlib import Path

from parkhouse_aggregator.parkhouse_aggregator import (
    convert_timestamp_to_epoch_seconds,
    export_parkhouse_data,
    generate_parkhouse_data,
)


class ParkingHistoryTests(unittest.TestCase):
    def test_winter_city_timestamp_converts_from_cet_to_utc_epoch_seconds(self):
        timestamp = convert_timestamp_to_epoch_seconds("09112023-0900")

        self.assertEqual(timestamp, 1699516800)

    def test_summer_city_timestamp_converts_from_cest_to_utc_epoch_seconds(self):
        timestamp = convert_timestamp_to_epoch_seconds("09072024-0900")

        self.assertEqual(timestamp, 1720508400)

    def test_snapshots_become_chronological_history_for_each_car_park(self):
        snapshots = [
            {
                "timestamp": "09112023-0910",
                "parkhouses": [
                    {
                        "name": "Dern-Passage",
                        "free_spaces": 100,
                        "occupied_spaces": 99,
                        "max_spaces": 199,
                    }
                ],
            },
            {
                "timestamp": "09112023-0905",
                "parkhouses": [
                    {
                        "name": "Dern-Passage",
                        "free_spaces": 120,
                        "occupied_spaces": 79,
                        "max_spaces": 199,
                    }
                ],
            },
        ]

        history = generate_parkhouse_data(snapshots)

        self.assertEqual(
            history["Dern-Passage"]["occupation_data"],
            [
                {
                    "timestamp": 1699517100,
                    "free_spaces": 120,
                    "occupied_spaces": 79,
                    "max_spaces": 199,
                },
                {
                    "timestamp": 1699517400,
                    "free_spaces": 100,
                    "occupied_spaces": 99,
                    "max_spaces": 199,
                },
            ],
        )

    def test_export_writes_per_car_park_history_as_json(self):
        history = {
            "Karstadt": {
                "name": "Karstadt",
                "occupation_data": [{"timestamp": 1, "free_spaces": 2}],
            }
        }

        with tempfile.TemporaryDirectory() as output_directory:
            export_parkhouse_data(output_directory, history)
            exported_history = json.loads(
                (Path(output_directory) / "karstadt.json").read_text()
            )

        self.assertEqual(exported_history, history["Karstadt"])


if __name__ == "__main__":
    unittest.main()