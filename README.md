# DE Sales Pipeline (Capstone 1)

A Databricks data pipeline built on synthetic retail orders, using bronze,
silver and gold layers. Work in progress.

## Data generator

`src/generate_orders.py` creates synthetic daily order files in `data/raw/`
(one CSV per day, 5 days by default). The files contain deliberate data
problems so the pipeline can be tested against them:

- 2 duplicate rows per file
- 1 late-arriving row per file (an order dated two days earlier)

### Run it

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python src/generate_orders.py
```

### Test it

```
pytest -v
```

Generated files are not committed (`data/` is listed in `.gitignore`).