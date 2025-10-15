# GRACE CLI Query Tool

This repository hosts the code allowing to perform SQL queries using a Python-based command line interface (CLI) on [the database designed to host ​spatiotemporal gravity data](https://github.com/SpaceGravimetryTUD/GRA## 👥 Contributors

This project was developed by the Space Gravimetry research group at Delft University of Technology:

- **Jose Carlos Urra Llanusa** - Research Software Engineer
- **Joao De Teixeira da Encarnacao** - Research Scientist  
- **Selin Kubilay** - Research Engineer
- **João Guimarães** - Software Developer
- **Miguel Cuadrat-Grzybowski** - Research Engineer

## 📜 Licensing & Waiveresiduals-db/tree/develop) recorded by the [GRACE (twin) satellites](https://grace.jpl.nasa.gov/mission/grace/).

---

## 🌍 Context & Background

We work with high-frequency geospatial time-series data from the GRACE satellite mission, specifically Level-1B range-rate residuals derived from inter-satellite Ka-band observations. These residuals may contain unexploited high-frequency geophysical signals used for scientific applications.

### Key dataset characteristics:

- **Temporal resolution**: 5-second intervals
- **Spatial attributes**: Latitude, longitude, altitude for GRACE A & B
- **Data volume**: 2002–2017, approx. \~95 million records
- **Target queries**: Time-span filtering, spatial bounding, and signal-based statistical analysis

---

## 🚀 Quick Start

### Prerequisites

This project targets Unix-based systems. If you're on Windows, install [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) and proceed as if on Ubuntu.

Install the following tools:

- **Python 3.10+**
- **[Poetry 2.x](https://python-poetry.org/docs/#installation)**

---

### Ubuntu

NB: These instructions were written after the fact. YMMV

Install prerequisites:

```bash
pipx ensurepath
```

Install and check poetry:

```bash
pipx install poetry
poetry -V
```

---

### Clone the Repository

```bash
git clone https://github.com/SpaceGravimetryTUD/GRACE-Client.git
cd GRACE-Client
```

---

### Environment Configuration

Make sure to have a data directory where you store your data.

> ⚠️ Security Note on Pickle Files
> Warning: This application loads data using pandas.read\_pickle(), which internally uses Python's pickle module.
> While this format is convenient for fast internal data loading, it is not secure against untrusted input. Never upload or load `.pkl` files from unverified or external sources, as they can execute arbitrary code on your system.

Create a `.env` file at the project root:

```ini
# .env
TABLE_NAME=kbr_gravimetry_v2
EXTERNAL_PORT=XXXX #Replace XXXX with available external port; in grace-cube.lr.tudelft.nl, port 3306 is open
DATABASE_NAME=geospatial_db
DATABASE_URL="postgresql://user:password@localhost:${EXTERNAL_PORT}/${DATABASE_NAME}"
DATA_PATH=/mnt/GRACEcube/Data/L1B_res/CSR_latlon_data/flat-data/v2/flat-data-2003.v2.pkl
```

To load environmental variables in `.env` run:

```bash
source .env
```

---

### Install Python Dependencies

```bash
poetry install
```

> If you get the error:
>
> ```
> Installing psycopg2 (2.9.10): Failed
> PEP517 build of a dependency failed
> Backend subprocess exited when trying to invoke get_requires_for_build_wheel
> ```
>
> Then:
>
> ```
> sudo apt install libpq-dev gcc
> ```

From now on, run all Python commands via:

```bash
poetry run <your-command>
```

> ⚠️ ISSUE: Poetry doesn't like pyenv: removing it from PATH works

---

### How to query Data

The following example command line bellow shows how you can run your queries, with all the recognized arguments explicitly stated:

```bash
poetry run grace query \
  --start-time "${YYYY}-${MM}-${DD}T${HH}:${MM}:${SS}" \
  --end-time "${YYYY}-${MM}-${DD}T${HH}:${MM}:${SS}" \
  --bbox xmin ymin xmax ymax \
  --polygon-str "xmin ymin, xmin ymax, xmax ymax, xmax ymin, xmin ymin" \
  --polygon-file path/to/area.geojson \
  --polygon-crs "EPSG:4326"\
  --config path/to/query.yaml \
  --columns cX,cY,... \
  --out-format netcdf \
  --out-path ./out/result.nc \
  --problematic-report ./out/problematic.json \
  --strict-cf False \
  --db-url $DATABASE_URL \
  --table  $TABLE_NAME
```

> x = lon; 
> y = lat; 
> YYYY = Year; 
> MM = Month; 
> DD = Day; 
> HH = Hours; 
> MM = Minutes;
> SS = Seconds'; 

```
Default arguments:
 --polygon-crs "EPSG:4326" -> For simplicity, supply EPSG:4326 geometries.
 --out-format netcdf -> csv and parquet exporting also supported
 --strict-cf False -> netcdf exporting specific, related to "minimal CF assertions — extend as needed"
 --db-url $DATABASE_URL
 --table $TABLE_NAME
```

#### Examples

To query data for a spective time interval, e.g. covering the whole March 2017, you can run:

```bash
poetry run grace query --start-time="2012-03-01T00:00:00" --end-time="2012-04-01T00:00:00"
```

If you want to focus on a specific set of locations within the same time interval, you can do so be either using one of the following spatial parsing options:

1. `--bbox`

```bash
poetry run grace query  --start-time "2012-03-01T00:00:00" --end-time "2012-04-01T00:00:00" --bbox 110 -7 200 5
```

2. `--polygon_str`

```bash
 poetry run grace query --start-time "2012-03-01T00:00:00" --end-time "2012-04-01T00:00:00"  --polygon-str '110 -7,200 -7,200 0
5,110 05,110 -7'
```

3. `--polygon_file`

```bash
poetry run grace query  --start-time "2012-03-01T00:00:00" --end-time "2012-04-01T00:00:00"  --polygon-file path/to/area.geojson
```

By default the following columns will be selected in the querying: `id`, `datetime`, `latitude_A`, `longitude_A`, `postfit`, `up_combined`. If would like to include more table columns, you can do so by stating them after `--columns`:

```bash
poetry run grace query  --start-time "2012-03-01T00:00:00" --end-time "2012-04-01T00:00:00" --bbox 110 -7 200 5 --columns latitude_B,longitude_B
```

By default the output is exported as a netcdf formatted file with the pathname `./query_output.nc`. As alternatives, the current client code release allows you to export the data as csv or parquet using `-out-format`. The output's pathname can be edited using '--out-path'. For example:

```bash
poetry run grace query  --start-time "2012-03-01T00:00:00" --end-time "2012-04-01T00:00:00" --bbox 110 -7 200 5 --columns latitude_B,longitude_B --out-format "parquet" --out-path "./test_query.parquet"
```

---

## 📊 Running Tests

Tests rely on a running local database and valid `.env` configuration. The PostGIS Extension should also be enabled (to get no failed tests).

```bash
poetry run pytest
```

> ✅ Ensure:
>
> * `$DATABASE_NAME` is running (defined in `.env`).
> * `$TABLE_NAME` table exists (defined in `.env`).
> * Sample data is loaded.

---

## 📁 Project Structure (simplified overview)

```text
.
├─ pyproject.toml # Poetry project config
├─ README.md
├── tests/            # Unit tests for ingestion, queries, and extension validation
├── .env              # Local environment variables (not committed)
├── LICENSE
└─ grace_query/
   ├─ __init__.py
   ├─ cli.py
   ├─ config.py
   ├─ sql.py
   ├─ polygons.py
   ├─ problematic.py
   └─ export/
      ├─ __init__.py
      ├─ netcdf_cf.py
      ├─ csv_writer.py
      └─ parquet_writer.py

```

---

## � Contributors

This project was developed by the Space Gravimetry research group at Delft University of Technology:

- **Jose Carlos Urra Llanusa** - Research Software Engineer
- **Joao De Teixeira da Encarnacao** - Research Scientist  
- **Selin Kubilay** - Research Engineer
- **João Guimarães** - Software Developer

## �📜 Licensing & Waiver

Licensed under the MIT License.

**Technische Universiteit Delft** hereby disclaims all copyright
interest in the program "GRACE Geospatial Data Processing Stack" written by the Author(s).

— ***Prof. H.G.C. (Henri) Werij***, Dean of Aerospace Engineering at TU Delft




