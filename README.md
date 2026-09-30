# Gießen Parking Data

This project collects parking availability reported by the City of Gießen and turns repeated snapshots into historical occupancy data. A small Vue dashboard charts a selected car park's history by week and offers CSV downloads.

## What it is useful for

- Check reported free spaces before driving to a participating car park.
- Compare car-park utilization and identify busy periods from saved snapshots.
- Explore or export occupancy history for personal analysis, coursework, or research.

This is an analysis and information project, not a navigation or reservation service. Its data only covers car parks shown by the city's parking guidance page.

## How it works

1. `scraping_parkleitsystem.py` reads the city's parking page and prints a JSON snapshot containing the update time and each listed car park's free, occupied, and total spaces.
2. Save snapshots in `data/` to build an archive. The scraper prints to the console; it does not schedule or save snapshots automatically.
3. `parkhouse_aggregator/parkhouse_aggregator.py` groups archived snapshots by car park, sorts entries by time, and writes one JSON history per car park into `parkhouse_data/`.
4. `WEBPAGE/` contains a Vue dashboard with bundled historical datasets and weekly occupancy charts. Refresh its bundled data when updating the archive. A CSV download button is present, but its handler is not implemented yet.

Each scraped snapshot has this shape:

```json
{
  "timestamp": "ddmmyyyy-hhmm",
  "parkhouses": [
    {
      "name": "NAME",
      "free_spaces": 120,
      "occupied_spaces": 79,
      "max_spaces": 199
    }
  ]
}
```

## Run

Install Python dependencies and scrape the current page:

```bash
python3 -m venv Env
source Env/bin/activate
pip install -r requirements.txt
python scraping_parkleitsystem.py
```

To aggregate snapshots already saved in `data/`:

```bash
python -m parkhouse_aggregator.parkhouse_aggregator
```

To run the dashboard locally:

```bash
cd WEBPAGE
npm install
npm run dev
```

## Tests

Run the offline Python unit tests:

```bash
python -m unittest discover -s tests -v
```

Each test checks one behavior with one assertion. Tests use fixed HTML and sample snapshots; they do not depend on the city's website being reachable.

## Limitations

- Source data usually updates only between 09:00 and 21:00, so overnight changes are not captured.
- The city page omits some Gießen car parks; a closed car park may also retain stale availability.
- Historical analysis is only as complete as the snapshots collected and saved in `data/`.