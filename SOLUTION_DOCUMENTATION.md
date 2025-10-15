# TableCheck Data Operations – Solution Documentation

## 1) What this project does (in plain English)
We took a flat CSV of restaurant transactions and turned it into a small analytics product. A lightweight database stores the data, and a web dashboard answers the five questions in the brief: visits, revenue, most popular dish, most profitable dish, and customer behavior across restaurants.

The end result is a simple, reproducible setup that you can run locally or deploy to a hosted environment.

## 2) The data at a glance
- Rows: ~150k (150,000 transactions)
- Columns: `restaurant_names`, `food_names`, `first_name`, `food_cost`
- Restaurants include: `bean-juice-stand`, `johnnys-cashew-stand`, `the-ice-cream-parlor`, and `the-restaurant-at-the-end-of-the-universe`

We keep the raw CSV intact under `data/data.csv` and load it into a normalized table for fast queries.

## 3) How the system is put together
- Database: SQLite (file `restaurant_data.db`). It’s ideal here: zero setup, good performance for a 150k-row dataset, and portable.
- ETL/Load: `setup_database.py` reads the CSV with Pandas and loads it into a single table: `restaurant_transactions`.
- Dashboard: `dashboard.py` (Streamlit + Plotly) provides filters, KPIs, and charts. Data is read straight from SQLite. Streamlit caching is used appropriately to keep it fast.

### Table schema (created by the loader)
`restaurant_transactions`
- `id` INTEGER PRIMARY KEY (autoincrement)
- `restaurant_name` TEXT
- `food_name` TEXT
- `customer_name` TEXT
- `food_cost` REAL
- `created_at` TIMESTAMP (defaults to now; mostly useful for auditing)

Indexes are created on `restaurant_name`, `food_name`, and `customer_name` to keep group-bys and distincts snappy.

## 4) How to run it locally
1. Navigate into the project folder:
   ```bash
   cd tablecheck-data-operations-take-home
   ```
2. Install dependencies:
   ```bash
   pip install streamlit pandas plotly numpy
   ```
3. Create the database (one-time or when the CSV changes):
   ```bash
   python setup_database.py
   ```
4. Start the dashboard:
   ```bash
   streamlit run dashboard.py
   ```
5. Open the app in your browser (Streamlit prints the local URL, typically `http://localhost:8501`).

If port 8501 is in use, run with a custom port, e.g. `--server.port 8502`.

## 5) What the dashboard shows
The top of the page displays key metrics (customers, revenue, transactions, average order value). Below that, each business question is answered directly with tables and charts. A sidebar filter lets you focus on a single restaurant or view everything combined.

### The five required answers (from the dataset provided)
1. Customers who visited “the-restaurant-at-the-end-of-the-universe”: 689
2. Revenue for “the-restaurant-at-the-end-of-the-universe”: $186,944.00
3. Most popular dish (by order count) per restaurant:
   - bean-juice-stand: honey (1,185 orders)
   - johnnys-cashew-stand: juice (1,196 orders)
   - the-ice-cream-parlor: beans (1,151 orders)
   - the-restaurant-at-the-end-of-the-universe: cheese (1,158 orders)
4. Most profitable dish (by total revenue) per restaurant:
   - bean-juice-stand: honey ($5,945.50)
   - johnnys-cashew-stand: juice ($5,989.00)
   - the-ice-cream-parlor: coffee ($5,789.50)
   - the-restaurant-at-the-end-of-the-universe: cheese ($5,861.50)
5. Customer behavior:
   - Most frequent visitor per restaurant: Michael (top at each restaurant)
   - Customers who visited the most distinct restaurants: several customers visited all four (e.g., Aaron, Abigail, Adam, Adrian, Adriana)

#### Summary tables

Key metrics for “the-restaurant-at-the-end-of-the-universe”

| Metric   | Value        |
|----------|--------------|
| Customers| 689          |
| Revenue  | $186,944.00  |

Most popular dish by restaurant

| Restaurant                              | Dish  | Orders |
|-----------------------------------------|-------|--------|
| bean-juice-stand                        | honey | 1,185  |
| johnnys-cashew-stand                    | juice | 1,196  |
| the-ice-cream-parlor                    | beans | 1,151  |
| the-restaurant-at-the-end-of-the-universe | cheese| 1,158  |

Most profitable dish by restaurant

| Restaurant                              | Dish   | Revenue   |
|-----------------------------------------|--------|-----------|
| bean-juice-stand                        | honey  | $5,945.50 |
| johnnys-cashew-stand                    | juice  | $5,989.00 |
| the-ice-cream-parlor                    | coffee | $5,789.50 |
| the-restaurant-at-the-end-of-the-universe | cheese | $5,861.50 |

## 6) Design choices (and why)
**SQLite over a server DB**: For a single-file dataset and a single-user dashboard, SQLite keeps the setup frictionless. If concurrency or multi-user writes become requirements, move to Postgres.

**Streamlit for the UI**: The brief calls for a browser-accessible dashboard. Streamlit excels at turning dataframes into useful UI quickly, without heavy front-end work.

**Pandas for transforms**: It’s the fastest way to aggregate and pivot a CSV of this size. We keep transformations simple and explicit.

**Caching strategy**: Database connections are cached with `st.cache_resource` (safe for non-serializable resources). Dataframes are cached with `st.cache_data` to avoid repeated reads and group-bys.

Compact view of key choices

| Area        | Choice     | Rationale |
|-------------|------------|-----------|
| Storage     | SQLite     | Zero setup, fast enough for 150k rows, portable |
| ETL         | Pandas     | Simple, explicit transforms over CSV |
| UI          | Streamlit  | Fast to build, browser-based, minimal boilerplate |
| Charts      | Plotly     | Interactive, readable defaults |
| Caching     | Streamlit  | Keeps queries and UI responsive |

## 7) Reliability, performance, and testing
- Indexes support the heavy group-bys (by restaurant, by food, by customer).
- The loader script validates row counts after load and prints a small sample.
- Visual elements are built on simple aggregations so they’re explainable and easy to verify.

Quick checks you can run:
```bash
# Verify database row count
python - << 'PY'
import sqlite3
conn = sqlite3.connect('tablecheck-data-operations-take-home/restaurant_data.db')
print('Row count:', conn.execute('select count(*) from restaurant_transactions').fetchone()[0])
conn.close()
PY
```

## 8) Deploying this (and what changes in production)
For quick hosting, Streamlit Community Cloud works well. Add a `requirements.txt` with:
```
streamlit
pandas
plotly
numpy
```
Set the app entry point to `tablecheck-data-operations-take-home/dashboard.py`. On first run, the database file is created next to the app.

### Production improvements
If this grew beyond a take-home project:
- Move from SQLite to Postgres for multi-user access and reliability.
- Containerize (Docker) and deploy behind a reverse proxy (TLS, auth).
- Add background jobs for scheduled loads if the source is updated regularly.
- Introduce a simple CI check to validate dataset integrity (row counts, required columns, value ranges).

## 9) If the data arrived via Kafka instead of a CSV
Switch the ingestion from batch to streaming:
- Producers write transaction events to Kafka (topic per domain, e.g., `transactions`).
- A consumer service (Python or a stream processor like Kafka Streams/Flink) validates and writes to the operational store (e.g., Postgres).
- Materialized, query-friendly tables or views (daily revenue, top dishes, unique visitors) are maintained either with incremental jobs or directly by the stream processor.
- The dashboard reads from these pre-aggregated tables for consistent, low-latency queries.

Benefits: real-time dashboards, horizontal scalability, and natural decoupling of producers/consumers. Tradeoffs: more moving parts, operational overhead, and schema evolution discipline.

## 10) What to look at in the repo
- `data/data.csv` – the raw dataset
- `setup_database.py` – loads and indexes the data
- `dashboard.py` – Streamlit app (KPIs, filters, charts)
- `get_answers.py` – prints the five answers in the console
- `requirements.txt` – minimal dependencies
- `restaurant_data.db` – created after running the loader

## 11) Limitations and follow-ups
- Prices are treated as-is; there’s no tax, discount, or currency logic.
- No user authentication on the dashboard (fine for local use or private links).
- If the dataset grows well beyond a few million rows, an analytical store (DuckDB/BigQuery/ClickHouse) could be more appropriate than SQLite.

## 12) One-paragraph wrap-up
This implementation keeps things pragmatic: a tiny ETL, a single-file relational store, and a clean dashboard that answers the brief clearly. It’s easy to run, easy to reason about, and leaves a clear path to production hardening if requirements expand.

## Business Questions Answered

### 1. Restaurant at the End of the Universe Analysis
- **Customer Count**: 689 unique customers
- **Revenue**: $186,944.00

### 2. Most Popular Dish at Each Restaurant
- **bean-juice-stand**: honey (1,185 orders)
- **johnnys-cashew-stand**: juice (1,196 orders)  
- **the-ice-cream-parlor**: beans (1,151 orders)
- **the-restaurant-at-the-end-of-the-universe**: cheese (1,158 orders)

### 3. Most Profitable Dish at Each Restaurant
- **bean-juice-stand**: honey ($5,945.50)
- **johnnys-cashew-stand**: juice ($5,989.00)
- **the-ice-cream-parlor**: coffee ($5,789.50)
- **the-restaurant-at-the-end-of-the-universe**: cheese ($5,861.50)

### 4. Customer Analysis
- **Most Frequent Customer per Restaurant**: Michael is the top customer at all restaurants (849-915 visits each)
- **Customers Who Visited Most Stores**: Aaron, Abigail, Adam, Adrian, and Adriana each visited all 4 restaurants

## Installation and Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup Database**:
   ```bash
   python setup_database.py
   ```

3. **Run Dashboard**:
   ```bash
   streamlit run dashboard.py
   ```

4. **Access Dashboard**: Open browser to `http://localhost:8501`

## Dashboard Features

### Key Metrics
- Total customers
- Total revenue
- Total transactions
- Average order value

### Interactive Filters
- Restaurant selection dropdown
- Real-time data filtering

### Visualizations
- Revenue by restaurant (bar chart)
- Customer distribution (pie chart)
- Average order value by restaurant
- Top food items by revenue

## Technical Decisions

### Database Choice: SQLite
- **Pros**: 
  - No server setup required
  - File-based, easy to deploy
  - Good performance for this dataset size
  - Built into Python
- **Cons**: 
  - Single-user access
  - Limited concurrent writes

### Dashboard Framework: Streamlit
- **Pros**:
  - Rapid development
  - Built-in caching
  - Easy deployment
  - Good for data analysis dashboards
- **Cons**:
  - Less customizable than full web frameworks
  - Limited real-time capabilities

## Deployment Considerations

### Current Setup
- Local development environment
- File-based SQLite database
- Single-user Streamlit app

### Production Improvements

1. **Database Migration**:
   - Move to PostgreSQL or MySQL for multi-user access
   - Add connection pooling
   - Implement database backups

2. **Application Deployment**:
   - Containerize with Docker
   - Deploy to cloud platform (AWS, GCP, Azure)
   - Add load balancing for multiple instances
   - Implement proper logging and monitoring

3. **Security**:
   - Add authentication/authorization
   - Implement HTTPS
   - Add input validation and sanitization

4. **Performance**:
   - Add Redis caching layer
   - Implement database query optimization
   - Add CDN for static assets

## Kafka Streaming Implementation

If data was streaming from Kafka, the architecture would change significantly:

### 1. Data Pipeline
```
Kafka Topics → Kafka Consumer → Data Processing → Database
```

### 2. Technology Stack
- **Message Broker**: Apache Kafka
- **Stream Processing**: Apache Kafka Streams or Apache Flink
- **Database**: PostgreSQL with connection pooling
- **Dashboard**: Real-time updates using WebSockets

### 3. Implementation Approach
- **Real-time Processing**: Process events as they arrive
- **Batch Processing**: Aggregate data in time windows
- **Data Validation**: Validate incoming data before processing
- **Error Handling**: Dead letter queues for failed messages
- **Monitoring**: Kafka metrics and application monitoring

### 4. Benefits of Streaming
- **Real-time Analytics**: Immediate insights into business metrics
- **Scalability**: Handle high-volume data streams
- **Fault Tolerance**: Built-in replication and failover
- **Decoupling**: Loose coupling between data producers and consumers

## Performance Optimizations

### Database Level
- Indexes on frequently queried columns
- Query optimization
- Connection pooling

### Application Level
- Streamlit caching for expensive operations
- Pagination for large datasets
- Lazy loading of visualizations

### Infrastructure Level
- Horizontal scaling
- Load balancing
- CDN for static assets

## Monitoring and Alerting

### Key Metrics to Monitor
- Database query performance
- Application response times
- Error rates
- User engagement metrics

### Alerting Thresholds
- Database connection failures
- High response times (>2 seconds)
- Error rate >1%
- Dashboard availability

## Future Enhancements

1. **Advanced Analytics**:
   - Customer segmentation
   - Predictive analytics
   - Seasonal trend analysis

2. **Real-time Features**:
   - Live data updates
   - Push notifications
   - Real-time alerts

3. **Mobile Support**:
   - Responsive design improvements
   - Mobile app development

4. **Integration**:
   - API endpoints for external access
   - Webhook support
   - Third-party tool integrations

## Conclusion

This solution provides a solid foundation for restaurant analytics with room for scaling and enhancement. The choice of technologies balances development speed with production readiness, while the architecture allows for future improvements as requirements evolve.
