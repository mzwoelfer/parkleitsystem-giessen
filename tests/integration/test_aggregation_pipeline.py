import json
import tempfile
import unittest
from pathlib import Path

from parkhouse_aggregator.parkhouse_aggregator import (
    aggregate_parkhouse_data,
    export_parkhouse_data,
)
from scraping_parkleitsystem_logic import scrape_webpage


def parking_page(name, update_time, free_spaces):
    return f"""
    <div class="info-panel">
        <span class="slot-name">{name}</span>
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
                ("NeustÃ€dter Tor", "09:10 Uhr - 09.11.2023", 100),
                ("neustädter", "09:05 Uhr - 09.11.2023", 120),
            ]
            for name, update_time, free_spaces in pages:
                snapshot = scrape_webpage(
                    parking_page(name, update_time, free_spaces)
                )
                snapshot_path = snapshots_directory / f"{snapshot['timestamp']}.json"
                snapshot_path.write_text(json.dumps(snapshot))

            (export_directory / "neustã€dter tor.json").write_text("stale alias")
            (export_directory / "neustã€dter.json").write_text("stale alias")
            history = aggregate_parkhouse_data(snapshots_directory)
            export_parkhouse_data(export_directory, history)
            output_files = sorted(path.name for path in export_directory.glob("*.json"))
            exported_history = json.loads((export_directory / "neustädter.json").read_text())
            snapshot_count = len(list(snapshots_directory.glob("*.json")))

        self.assertEqual(
            (output_files, snapshot_count, exported_history),
            (
                ["neustädter.json"],
                2,
                {
                    "name": "Neustädter",
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
            ),
        )