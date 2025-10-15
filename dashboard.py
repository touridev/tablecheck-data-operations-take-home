import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="TableCheck Restaurant Analytics Dashboard",
    page_icon="🍽️",
    layout="wide"
)

# Database connection
@st.cache_resource
def get_db_connection():
    return sqlite3.connect('restaurant_data.db')

@st.cache_data
def load_data():
    """Load all data from database"""
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM restaurant_transactions", conn)
    return df

@st.cache_data
def get_restaurant_list():
    """Get list of all restaurants"""
    conn = get_db_connection()
    restaurants = pd.read_sql_query("SELECT DISTINCT restaurant_name FROM restaurant_transactions", conn)
    return restaurants['restaurant_name'].tolist()

# Main dashboard
st.title("🍽️ TableCheck Restaurant Analytics Dashboard")
st.markdown("---")

# Load data
df = load_data()
restaurants = get_restaurant_list()

# Sidebar filters
st.sidebar.title("Filters")
selected_restaurant = st.sidebar.selectbox("Select Restaurant", ["All"] + restaurants)

# Filter data based on selection
if selected_restaurant != "All":
    filtered_df = df[df['restaurant_name'] == selected_restaurant]
else:
    filtered_df = df

# Key Metrics Row
st.subheader("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_customers = filtered_df['customer_name'].nunique()
    st.metric("Total Customers", f"{total_customers:,}")

with col2:
    total_revenue = filtered_df['food_cost'].sum()
    st.metric("Total Revenue", f"${total_revenue:,.2f}")

with col3:
    total_transactions = len(filtered_df)
    st.metric("Total Transactions", f"{total_transactions:,}")

with col4:
    avg_order_value = filtered_df['food_cost'].mean()
    st.metric("Average Order Value", f"${avg_order_value:.2f}")

st.markdown("---")

# Business Questions Section
st.subheader("🎯 Business Questions Analysis")

# Question 1: Restaurant at the end of the universe customers
st.markdown("### 1. Restaurant at the End of the Universe Analysis")
universe_df = df[df['restaurant_name'] == 'the-restaurant-at-the-end-of-the-universe']

col1, col2 = st.columns(2)
with col1:
    universe_customers = universe_df['customer_name'].nunique()
    st.metric("Total Customers", universe_customers)
    
with col2:
    universe_revenue = universe_df['food_cost'].sum()
    st.metric("Total Revenue", f"${universe_revenue:,.2f}")

# Question 2: Most popular dish at each restaurant
st.markdown("### 2. Most Popular Dish at Each Restaurant")
popular_dishes = df.groupby(['restaurant_name', 'food_name']).size().reset_index(name='count')
most_popular = popular_dishes.loc[popular_dishes.groupby('restaurant_name')['count'].idxmax()]

st.dataframe(most_popular[['restaurant_name', 'food_name', 'count']], 
             column_config={
                 "restaurant_name": "Restaurant",
                 "food_name": "Most Popular Dish",
                 "count": "Orders"
             })

# Question 3: Most profitable dish at each restaurant
st.markdown("### 3. Most Profitable Dish at Each Restaurant")
profitable_dishes = df.groupby(['restaurant_name', 'food_name'])['food_cost'].sum().reset_index(name='total_revenue')
most_profitable = profitable_dishes.loc[profitable_dishes.groupby('restaurant_name')['total_revenue'].idxmax()]

st.dataframe(most_profitable[['restaurant_name', 'food_name', 'total_revenue']],
             column_config={
                 "restaurant_name": "Restaurant",
                 "food_name": "Most Profitable Dish",
                 "total_revenue": "Total Revenue ($)"
             })

# Question 4: Customer analysis
st.markdown("### 4. Customer Analysis")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Most Frequent Customer per Restaurant")
    customer_counts = df.groupby(['restaurant_name', 'customer_name']).size().reset_index(name='visits')
    top_customers = customer_counts.loc[customer_counts.groupby('restaurant_name')['visits'].idxmax()]
    st.dataframe(top_customers[['restaurant_name', 'customer_name', 'visits']],
                 column_config={
                     "restaurant_name": "Restaurant",
                     "customer_name": "Top Customer",
                     "visits": "Visits"
                 })

with col2:
    st.markdown("#### Customers Who Visited Most Restaurants")
    customer_restaurants = df.groupby('customer_name')['restaurant_name'].nunique().reset_index(name='restaurants_visited')
    top_explorers = customer_restaurants.nlargest(10, 'restaurants_visited')
    st.dataframe(top_explorers,
                 column_config={
                     "customer_name": "Customer",
                     "restaurants_visited": "Restaurants Visited"
                 })

# Visualizations
st.markdown("---")
st.subheader("📈 Visualizations")

# Revenue by Restaurant
st.markdown("### Revenue by Restaurant")
revenue_by_restaurant = df.groupby('restaurant_name')['food_cost'].sum().reset_index()
fig_revenue = px.bar(revenue_by_restaurant, x='restaurant_name', y='food_cost',
                     title="Total Revenue by Restaurant",
                     labels={'food_cost': 'Revenue ($)', 'restaurant_name': 'Restaurant'})
fig_revenue.update_xaxes(tickangle=45)
st.plotly_chart(fig_revenue, use_container_width=True)

# Customer Distribution
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Customer Visits by Restaurant")
    customer_visits = df.groupby('restaurant_name')['customer_name'].nunique().reset_index()
    fig_customers = px.pie(customer_visits, values='customer_name', names='restaurant_name',
                           title="Customer Distribution")
    st.plotly_chart(fig_customers, use_container_width=True)

with col2:
    st.markdown("### Average Order Value by Restaurant")
    avg_order = df.groupby('restaurant_name')['food_cost'].mean().reset_index()
    fig_avg = px.bar(avg_order, x='restaurant_name', y='food_cost',
                     title="Average Order Value by Restaurant",
                     labels={'food_cost': 'Average Order Value ($)', 'restaurant_name': 'Restaurant'})
    fig_avg.update_xaxes(tickangle=45)
    st.plotly_chart(fig_avg, use_container_width=True)

# Top Food Items
st.markdown("### Top Food Items Across All Restaurants")
top_foods = df.groupby('food_name')['food_cost'].sum().nlargest(15).reset_index()
fig_foods = px.bar(top_foods, x='food_cost', y='food_name',
                   title="Top 15 Food Items by Revenue",
                   labels={'food_cost': 'Revenue ($)', 'food_name': 'Food Item'},
                   orientation='h')
st.plotly_chart(fig_foods, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("**Dashboard created for TableCheck Data Operations Take-Home Project**")
