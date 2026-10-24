# OBD-telematics

A Python project that logs live vehicle data from an OBD-II adapter into a local SQLite database. After it will show onto a Streamlit dashboad 

## Features

- Connects to an ELM327-compatible OBD-II adapter (or the ELM327 emulator for offline development)
- Polls engine RPM, vehicle speed, and coolant temperature once per second
- Stores each session as a "trip" with timestamped readings in SQLite
- Streamlit dashboard for viewing the logged readings

## Project structure

```
OBD-telematics/
├── src/
│   ├── connect.py     # Connects to the adapter and logs readings
│   ├── db.py          # Creates the SQLite schema
│   └── dashboard.py   # Streamlit dashboard
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10+
- An ELM327-compatible OBD-II adapter, or the bundled ELM327 emulator

## Setup

```bash
git clone https://github.com/DoctorIsaac/OBD-telematics.git
cd OBD-telematics

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

mkdir -p data                    # the database lives in data/trips.db
```

## Usage

Run everything from the repository root, since the database path (`data/trips.db`) is relative.

**1. Create the database**

```bash
python src/db.py
```

**2. Start logging**

Set `portstr` and `baudrate` at the top of `src/connect.py` to match your adapter, then:

```bash
python src/connect.py
```

Each run creates a new trip and logs RPM, speed, and coolant temperature every second. Press `Ctrl+C` to stop and close the connection.

**3. View the data**

```bash
streamlit run src/dashboard.py
```

### Developing without a car

The ELM327 emulator is included in `requirements.txt`. Start it in a separate terminal and note the pseudo-terminal port it reports:

```bash
python -m elm
```

Then set `portstr` in `src/connect.py` to that port (the current default is `/dev/ttys001`).

## Database schema

**trips**

| Column       | Type    | Notes                       |
|--------------|---------|-----------------------------|
| `id`         | INTEGER | Primary key, autoincrement  |
| `start_time` | TEXT    | `YYYY-MM-DD HH:MM:SS`       |

**readings**

| Column      | Type    | Notes                              |
|-------------|---------|------------------------------------|
| `id`        | INTEGER | Primary key, autoincrement         |
| `trip_id`   | INTEGER | Foreign key to `trips.id`          |
| `timestamp` | TEXT    | `YYYY-MM-DD HH:MM:SS`              |
| `pid_name`  | TEXT    | e.g. `RPM`, `Speed`                |
| `value`     | REAL    | Numeric value, units not stored    |

## Roadmap

- [ ] Charts and per-trip filtering in the dashboard
- [ ] Configurable port, baud rate, and PID list (CLI flags or config file)
- [ ] Store units alongside values
- [ ] Add more PIDs (throttle position, fuel level, etc.)
- [ ] Tests
- [ ] Build a model to predict driving behaviors 

## Built with

[python-OBD](https://github.com/brendan-w/python-OBD), [ELM327-emulator](https://github.com/Ircama/ELM327-emulator), [Streamlit](https://streamlit.io/), SQLite, pandas
