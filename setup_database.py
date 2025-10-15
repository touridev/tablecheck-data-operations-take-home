import sqlite3
import pandas as pd
import os

def create_database():
    """Create SQLite database and ingest CSV data"""
    
    # Create database connection
    conn = sqlite3.connect('restaurant_data.db')
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS restaurant_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_name TEXT NOT NULL,
            food_name TEXT NOT NULL,
            customer_name TEXT NOT NULL,
            food_cost REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Read CSV data
    print("Reading CSV data...")
    df = pd.read_csv('data/data.csv')
    
    # Clean column names to match our table schema
    df.columns = ['restaurant_name', 'food_name', 'customer_name', 'food_cost']
    
    # Insert data into database
    print("Inserting data into database...")
    df.to_sql('restaurant_transactions', conn, if_exists='replace', index=False)
    
    # Create indexes for better query performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_restaurant ON restaurant_transactions(restaurant_name)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_food ON restaurant_transactions(food_name)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_customer ON restaurant_transactions(customer_name)')
    
    # Verify data
    cursor.execute('SELECT COUNT(*) FROM restaurant_transactions')
    count = cursor.fetchone()[0]
    print(f"Successfully inserted {count} records")
    
    # Show sample data
    cursor.execute('SELECT * FROM restaurant_transactions LIMIT 5')
    sample = cursor.fetchall()
    print("Sample data:")
    for row in sample:
        print(row)
    
    conn.commit()
    conn.close()
    print("Database setup complete!")

if __name__ == "__main__":
    create_database()
