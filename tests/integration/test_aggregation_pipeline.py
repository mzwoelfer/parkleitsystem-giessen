import json
import tempfile
import unittest
from pathlib import Path

from parkhouse_aggregator.parkhouse_aggregator import (
    aggregate_parkhouse_data,
    export_parkhouse_data,
)
from scraping_parkleitsystem_logic import scrape_webpage


def parking_page(update_time, free_spaces):
    occupied_spaces = 199 - free_spaces
    return f"""
    <div class="info-panel">
        <span class="slot-name">Dern-Passage</span>
        <span class="free">Frei: {free_spaces}</span>
        <span class="max">Gesamt: 199</span>
    </div>
    <small class="last-update">Zuletzt aktualisiert: {update_time}</small>
    """


class AggregationPipelineTests(unittest.TestCase):
    def test_html_snapshots_are_read_aggregated_and_exported_as_history(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            snapshots_directory = Path(temporary_directory) / "snapshots"
            export_directory = Path(temporary_directory) / "history"
            snapshots_directory.mkdir()
            export_directory.mkdir()

            pages = [
                ("09:10 Uhr - 09.11.2023", 100),
                ("09:05 Uhr - 09.11.2023", 120),
            ]
            for update_time, free_spaces in pages:
                snapshot = scrape_webpage(parking_page(update_time, free_spaces))
                snapshot_path = snapshots_directory / f"{snapshot['timestamp']}.json"
                snapshot_path.write_text(json.dumps(snapshot))

            history = aggregate_parkhouse_data(snapshots_directory)
            export_parkhouse_data(export_directory, history)
            exported_history = json.loads(
                (export_directory / "dern-passage.json").read_text()
            )

        self.assertEqual(
            exported_history,
            {
                "name": "Dern-Passage",
                "occupation_data": [
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
            },
        )