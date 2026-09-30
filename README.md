# Gießen Parking Data

- Scrapes Gießen parking availability into timestamped JSON snapshots.
- Aggregates snapshots into per-car-park history.
- Charts bundled history in a Vue dashboard.

## Run

```bash
python3 -m venv Env
source Env/bin/activate
pip install -r requirements.txt
python scraping_parkleitsystem.py
```

Scraper prints current snapshot to stdout. Save output under `data/` to archive it. Aggregate archived snapshots with:

```bash
python -m parkhouse_aggregator.parkhouse_aggregator
```

Run dashboard:

```bash
cd WEBPAGE
npm install
npm run dev
```

Dashboard plots bundled weekly occupancy history. Its CSV button currently has no handler.

## Tests

```bash
python -m unittest discover -s tests -v
```

Offline tests use fixture HTML and sample snapshots; each test has one assertion.

## Contribute

Open a pull request with focused changes. Add or update offline tests for behavior changes; keep tests independent of the live city website.