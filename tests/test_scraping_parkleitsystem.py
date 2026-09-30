import unittest

import scraping_parkleitsystem


PARKING_PAGE_HTML = """
<div class="parken-giessen">
    <div class="info-panel">
        <span class="slot-name">Dern-Passage</span>
        <span class="free">Frei: 120</span>
        <span class="max">Gesamt: 199</span>
    </div>
    <small class="last-update">Zuletzt aktualisiert: 09:15 Uhr - 01.01.2024</small>
</div>
"""


class ParkingSnapshotTests(unittest.TestCase):
    def test_scrape_returns_timestamped_parking_snapshot(self):
        snapshot = scraping_parkleitsystem.scrape_webpage(PARKING_PAGE_HTML)

        self.assertEqual(
            snapshot,
            {
                "timestamp": "01012024-0915",
                "parkhouses": [
                    {
                        "name": "Dern-Passage",
                        "free_spaces": 120,
                        "occupied_spaces": 79,
                        "max_spaces": 199,
                    }
                ],
            },
        )

    def test_occupied_spaces_are_capacity_minus_free_spaces(self):
        parkhouse = scraping_parkleitsystem.extract_parkhouse_data_from_html_tag(
            """
            <div class="info-panel">
                <span class="slot-name">Dern-Passage</span>
                <span class="free">Frei: 120</span>
                <span class="max">Gesamt: 199</span>
            </div>
            """
        )

        self.assertEqual(parkhouse["occupied_spaces"], 79)

    def test_missing_requested_html_element_raises_a_clear_error(self):
        with self.assertRaisesRegex(TypeError, "No div element with class 'missing' found"):
            scraping_parkleitsystem.get_text_from_html_tag(
                PARKING_PAGE_HTML,
                {
                    "html_element": "div",
                    "html_attribute": "class",
                    "attribute_value": "missing",
                },
            )


if __name__ == "__main__":
    unittest.main()