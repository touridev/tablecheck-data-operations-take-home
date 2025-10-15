# TableCheck Data Operations – README

This repository turns a CSV of restaurant transactions into a small analytics product: a SQLite database and a Streamlit dashboard that answers the five questions in the brief (visits, revenue, most popular and most profitable dishes, and customer behavior).

## What you’ll get out of the box
- A one-command ETL that loads `data/data.csv` into SQLite
- An interactive dashboard (filters, KPIs, charts)
- Clear, reproducible answers to all five questions

## Quick start (local)
```bash
cd tablecheck-data-operations-take-home
pip install streamlit pandas plotly numpy
python setup_database.py     # creates restaurant_data.db
streamlit run dashboard.py   # prints a local URL to open
```
If port 8501 is busy, add `--server.port 8502`.

## Answers at a glance (from this dataset)
- “Restaurant at the end of the universe”
  - Customers: 689
  - Revenue: $186,944.00
- Most popular dish by restaurant
  - bean-juice-stand: honey (1,185 orders)
  - johnnys-cashew-stand: juice (1,196 orders)
  - the-ice-cream-parlor: beans (1,151 orders)
  - the-restaurant-at-the-end-of-the-universe: cheese (1,158 orders)
- Most profitable dish by restaurant
  - bean-juice-stand: honey ($5,945.50)
  - johnnys-cashew-stand: juice ($5,989.00)
  - the-ice-cream-parlor: coffee ($5,789.50)
  - the-restaurant-at-the-end-of-the-universe: cheese ($5,861.50)
- Customer behavior
  - Most frequent visitor per restaurant: Michael (tops each restaurant)
  - Most restaurants visited: several customers hit all four (e.g., Aaron, Abigail, Adam, Adrian, Adriana)

## What’s in the dashboard
- KPIs: customers, revenue, transactions, average order value
- Restaurant filter (All or single restaurant)
- Charts: revenue by restaurant, customer distribution, AOV by restaurant, top food items by revenue
- Tables that show the exact answers to the five questions

## How it’s built
- Database: SQLite (`restaurant_data.db`) created by `setup_database.py`
- Loader: Pandas reads the CSV and writes to a single table `restaurant_transactions`, with helpful indexes
- UI: Streamlit + Plotly for fast, interactive visuals
- Caching: Streamlit caching to avoid repeated reads and keep the app snappy

## Repository layout
```
tablecheck-data-operations-take-home/
├── data/
│   └── data.csv
├── dashboard.py
├── get_answers.py
├── requirements.txt
├── restaurant_data.db          # generated after running the loader
├── setup_database.py
├── PROJECT_SUMMARY.md
└── SOLUTION_DOCUMENTATION.md
```

## Deploying
For Streamlit Community Cloud:
1) Push this folder to GitHub
2) In Streamlit Cloud, set the app entry point to `tablecheck-data-operations-take-home/dashboard.py`
3) Make sure `requirements.txt` includes:
```
streamlit
pandas
plotly
numpy
```
The app will create `restaurant_data.db` on first run.

## Troubleshooting
- Port already in use → `streamlit run dashboard.py --server.port 8502`
- Fresh machine/deploy → ensure requirements are installed
- No data showing → run `python setup_database.py` again to (re)create the DB

## Notes
This is intentionally lightweight: a single-file database, clear transforms, and an approachable dashboard. It’s easy to run locally, and there’s a straightforward path to scale (Postgres + containers) if requirements grow.