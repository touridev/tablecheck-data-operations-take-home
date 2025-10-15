# TableCheck Data Operations Take-Home Project - Solution Documentation

## Overview
This project analyzes restaurant transaction data to answer key business questions about customer behavior, revenue, and popular items across multiple restaurants.

## Dataset Analysis
- **Size**: 150,000 transaction records
- **Columns**: restaurant_names, food_names, first_name, food_cost
- **Restaurants**: Multiple restaurants including "the-restaurant-at-the-end-of-the-universe"

## Solution Architecture

### 1. Database Setup
- **Technology**: SQLite (lightweight, file-based database)
- **Schema**: Single table `restaurant_transactions` with indexes for performance
- **Ingestion**: Python script (`setup_database.py`) reads CSV and loads into database

### 2. Dashboard
- **Technology**: Streamlit (Python web framework)
- **Features**: 
  - Interactive filters
  - Key metrics display
  - Business question answers
  - Data visualizations using Plotly

### 3. Key Components
- `setup_database.py`: Database creation and data ingestion
- `dashboard.py`: Streamlit web application
- `requirements.txt`: Python dependencies

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
