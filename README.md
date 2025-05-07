# Auslesen Parkleitsystem Gießen
Data sourced from the webpage of the parking guidance system (`Parkleitsystem`) by the city **Gießen**.

🔗 URL: https://www.giessen.de/Umwelt_und_Verkehr/Parken/

<div align="center">
  <img src="https://www.giessen.de/layout/giessen2017/assets/img/giessen-logo.png" alt="Universitätsstadt Gießen Logo" width="150"/>
</div>


## 🚀 Usage
The `scraping_parkleitsstem.py` script reads the HTML table on the parkhouse webpage and prints it as JSON to the console.
```SHELL
python3 scraping_parkleitsstem.py
```

## 🏗️ How to use / Development?

```BASH
# Create / Activate Python Virtual Environment
python3 -m venv Env
source Env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Get last updated data in JSON format
python3 scraping_parkleitsystem.py
```

## The data format
```JSON
{
  "timestamp": "ddmmyyyy-hhmm",
  "parkhouses": [
    {
      "name": "NAME",
      "free_spaces": INT,
      "occupied_spaces": INT,
      "max_spaces": INT
    },
    {
        ...
    }
  ]
}
```


## What and Where?
- `data/`: JSON dumps form the parkhouse data approx. every 5 minutes
- `tests/`: Tests
- `parkhouse_aggregator/`: Python3 script that aggregate the raw data from `data/` per parkhouse
    - `parkhouse_aggregator.py`: Aggregates the raw data from the `data/` directory per parkhouse into the `parkhouse_data/` directory
- `parkhouse_data/`: Parkhouse occupation aggregated over time, per parkhouse

## 🚧 Limitations
- The data excludes nights: The data is only updated between 9am and 9pm. Nightly changes are not included
- Some large parkhouses in Gießen are not present in the dataset
- Parkhouses that are closed will sometimes not be updated on the webpage (Parkhaus "Am Kino")


