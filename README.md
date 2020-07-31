# Pokemon Scraper

Retrieves **ALL 893 Pokemon** (Gen I to XIII) from *Serebii* in a single request and saves to **.json** or **.csv file**. Includes basic information only like types and stats.

## Sample

```
    {
        "num": 892,
        "name": "Urshifu",
        "types": [
            "fighting",
            "dark"
        ],
        "hp": 100,
        "atk": 130,
        "def": 100,
        "sp_atk": 63,
        "sp_def": 60,
        "spd": 97
    },
    {
        "num": 893,
        "name": "Zarude",
        "types": [
            "dark",
            "grass"
        ],
        "hp": 105,
        "atk": 120,
        "def": 105,
        "sp_atk": 70,
        "sp_def": 95,
        "spd": 105
    }
```


## Prerequisites

* Python 3.6+
* Pip

## How to run

1. Install dependencies: `pip install -r requirements.txt`
2. Run via python
    * Linux - `python3 scripts/scrape-mons.py --output path/pokedex.json`
    * Windows - `python scripts/scrape-mons.py --output path/pokedex.json`

