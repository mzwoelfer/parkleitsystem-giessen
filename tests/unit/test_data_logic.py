import unittest
from datetime import datetime

import pandas as pd

from parkhouse_aggregator.csv_export import epoch_to_hhmm
from parkhouse_aggregator.daily_summary import process_parkhouse_data
from parkhouse_aggregator.visualization import epoch_to_human, flatten_parkhouse_data


class InMemoryTransformTests(unittest.TestCase):
    def test_daily_summary_uses_max_occupied_and_min_free_spaces(self):
        data = {
            "name": "Central",
            "occupation_data": [
                {
                    "timestamp": 1704067200,
                    "occupied_spaces": 5,
                    "free_spaces": 10,
                },
                {
                    "timestamp": 1704070800,
                    "occupied_spaces": 9,
                    "free_spaces": 6,
                },
            ],
        }

        name, daily_data = process_parkhouse_data(data)

        self.assertEqual(
            (name, daily_data.to_dict("records")),
            (
                "Central",
                [
                    {
                        "date": pd.Timestamp("2024-01-01"),
                        "max_occupied_spaces": 9,
                        "min_free_spaces": 6,
                    }
                ],
            ),
        )

    def test_human_timestamp_uses_local_datetime_format(self):
        timestamp = 0
        expected = datetime.fromtimestamp(timestamp).strftime("%a. %d.%m - %H:%M")

        self.assertEqual(epoch_to_human(timestamp), expected)

    def test_flattened_data_contains_formatted_timestamp_and_occupancy(self):
        data = {"occupation_data": [{"timestamp": 0, "occupied_spaces": 7}]}

        result = flatten_parkhouse_data(data)

        self.assertEqual(
            result.to_dict("records"),
            [
                {
                    "timestamp": epoch_to_human(0),
                    "value": 7,
                }
            ],
        )

    def test_csv_timestamp_uses_iso_utc_format(self):
        self.assertEqual(epoch_to_hhmm(0), "1970-01-01T00:00:00")