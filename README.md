# TableCheck Data Operations Take Home Project - ✅ COMPLETED

Take a look at the dataset located in `/data/data.csv`. Your goal is to interpret it and create a dashboard providing the answers to the following questions:
  - [x] How many customers visited the "Restaurant at the end of the universe"? **Answer: 689 customers**
  - [x] How much money did the "Restaurant at the end of the universe" make? **Answer: $186,944.00**
  - [x] What was the most popular dish at each restaurant? **See detailed answers below**
  - [x] What was the most profitable dish at each restaurant? **See detailed answers below**
  - [x] Who visited each store the most, and who visited the most stores? **See detailed answers below**

## ✅ Project Status: COMPLETED

### 🎯 Business Questions - Complete Answers

#### 1. Restaurant at the End of the Universe Analysis
- **Customers**: 689 unique customers visited
- **Revenue**: $186,944.00 generated

#### 2. Most Popular Dish at Each Restaurant
- **bean-juice-stand**: honey (1,185 orders)
- **johnnys-cashew-stand**: juice (1,196 orders)  
- **the-ice-cream-parlor**: beans (1,151 orders)
- **the-restaurant-at-the-end-of-the-universe**: cheese (1,158 orders)

#### 3. Most Profitable Dish at Each Restaurant
- **bean-juice-stand**: honey ($5,945.50)
- **johnnys-cashew-stand**: juice ($5,989.00)
- **the-ice-cream-parlor**: coffee ($5,789.50)
- **the-restaurant-at-the-end-of-the-universe**: cheese ($5,861.50)

#### 4. Customer Analysis
- **Most Frequent Customer per Restaurant**: Michael is the top customer at all restaurants (849-915 visits each)
- **Customers Who Visited Most Stores**: Aaron, Abigail, Adam, Adrian, and Adriana each visited all 4 restaurants

## ✅ Tasks Completed

- [x] Create a backing database and ingest the data from this dataset.
- [x] Create a dashboard.
- [x] Document your solution.

## 🚀 Dashboard Access

**Dashboard URL**: http://localhost:8501 (when running locally)

### Quick Start:
```bash
# Navigate to project directory
cd tablecheck-data-operations-take-home

# Install dependencies
pip install streamlit pandas plotly

# Setup database (if not already done)
python setup_database.py

# Run dashboard
streamlit run dashboard.py
```

## 📊 Dashboard Features

- **Interactive Analytics**: Real-time filtering and data exploration
- **Key Metrics**: Total customers, revenue, transactions, average order value
- **Visualizations**: 
  - Revenue by restaurant (bar charts)
  - Customer distribution (pie charts)
  - Average order value analysis
  - Top food items by revenue
- **Business Questions Section**: Direct answers to all 5 questions
- **Restaurant Filtering**: Dropdown to filter by specific restaurant

## 🛠️ Technology Stack

- **Database**: SQLite with optimized indexes
- **Dashboard**: Streamlit with Plotly visualizations
- **Data Processing**: Pandas
- **Language**: Python 3.x

## 📁 Project Structure

```
tablecheck-data-operations-take-home/
├── data/
│   └── data.csv                    # Original dataset (150K records)
├── setup_database.py               # Database creation & data ingestion
├── dashboard.py                    # Streamlit analytics dashboard
├── get_answers.py                  # Business questions answers script
├── requirements.txt                # Python dependencies
├── restaurant_data.db              # SQLite database (created after setup)
├── SOLUTION_DOCUMENTATION.md       # Comprehensive technical documentation
├── PROJECT_SUMMARY.md              # Project overview and results
└── README.md                       # This file
```

## 🔮 Deployment Questions Answered

### How would you build this differently if the data was being streamed from Kafka?

**Answer**: Would implement a real-time streaming architecture:
- **Kafka Consumer**: Process streaming events
- **Stream Processing**: Apache Kafka Streams or Apache Flink
- **Real-time Database**: PostgreSQL with connection pooling
- **WebSocket Dashboard**: Live updates using WebSockets
- **Benefits**: Real-time analytics, better scalability, fault tolerance

### How would you improve the deployment of this system?

**Answer**: Production-ready improvements:
- **Containerization**: Docker containers for easy deployment
- **Cloud Deployment**: AWS/GCP/Azure with auto-scaling
- **Database Migration**: PostgreSQL for multi-user access
- **Security**: Authentication, HTTPS, input validation
- **Monitoring**: Application metrics, logging, alerting
- **Performance**: Redis caching, CDN, load balancing

## 📈 Dataset Insights

- **Total Records**: 150,000 transactions
- **Restaurants**: 4 restaurants analyzed
- **Customers**: Thousands of unique customers
- **Revenue Range**: $1.00 - $10.00 per transaction
- **Most Active Customer**: Michael (3,462 total visits across all restaurants)

## 🎉 Project Completion Summary

All requirements have been successfully implemented:
- ✅ Database created and data ingested (150,000 records)
- ✅ Interactive web dashboard deployed
- ✅ All business questions answered with data
- ✅ Comprehensive documentation provided
- ✅ Deployment recommendations included

**Dashboard Link**: http://localhost:8501 (when running locally)

---

*Project completed successfully with full analytics dashboard and comprehensive documentation.*