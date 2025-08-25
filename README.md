# GRACE CLI Query Tool

This repository hosts the code allowing to perform SQL queries using a Python-based command line interface (CLI) on [the database designed to host ​spatiotemporal gravity data](https://github.com/SpaceGravimetryTUD/GRACE-Orbit-Residuals-db/tree/develop) recorded by the [GRACE (twin) satellites](https://grace.jpl.nasa.gov/mission/grace/). 

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
DATABASE_URL="postgresql://user:password@localhost:5432/${DATABASE_NAME}"
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

### Example Query Data


```bash
poetry run grace query \
  --start 2010-01 --end 2010-03 \
  --bbox xmin ymin xmax ymax \
  --polygon "lon1 lat1,lon2 lat2,...,lonN latN" \
  --polygon-file path/to/area.geojson \
  --params up_combined,postfit \
  --format netcdf \
  --out ./out/result.nc \
  --config query.yaml \
  --problematic-report ./out/problematic.json \
  --strict-cf
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

## 📜 Licensing & Waiver

Licensed under the MIT License.

**Technische Universiteit Delft** hereby disclaims all copyright
interest in the program "GRACE Geospatial Data Processing Stack" written by the Author(s).

— ***Prof. H.G.C. (Henri) Werij***, Dean of Aerospace Engineering at TU Delft




