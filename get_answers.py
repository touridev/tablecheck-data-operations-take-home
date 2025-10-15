import sqlite3

def get_business_answers():
    conn = sqlite3.connect('restaurant_data.db')
    cursor = conn.cursor()
    
    print("=== BUSINESS QUESTIONS ANSWERS ===\n")
    
    # Question 1: Restaurant at the end of the universe customers
    cursor.execute('SELECT COUNT(DISTINCT customer_name) FROM restaurant_transactions WHERE restaurant_name = "the-restaurant-at-the-end-of-the-universe"')
    customers = cursor.fetchone()[0]
    print(f"1. How many customers visited the 'Restaurant at the end of the universe'?")
    print(f"   Answer: {customers:,} customers\n")
    
    # Question 2: Revenue for Restaurant at the end of the universe
    cursor.execute('SELECT SUM(food_cost) FROM restaurant_transactions WHERE restaurant_name = "the-restaurant-at-the-end-of-the-universe"')
    revenue = cursor.fetchone()[0]
    print(f"2. How much money did the 'Restaurant at the end of the universe' make?")
    print(f"   Answer: ${revenue:,.2f}\n")
    
    # Question 3: Most popular dish at each restaurant
    print("3. What was the most popular dish at each restaurant?")
    cursor.execute('''
        SELECT restaurant_name, food_name, COUNT(*) as order_count
        FROM restaurant_transactions
        GROUP BY restaurant_name, food_name
        HAVING COUNT(*) = (
            SELECT MAX(cnt) FROM (
                SELECT COUNT(*) as cnt 
                FROM restaurant_transactions rt2 
                WHERE rt2.restaurant_name = restaurant_transactions.restaurant_name
                GROUP BY rt2.food_name
            )
        )
        ORDER BY restaurant_name
    ''')
    popular_dishes = cursor.fetchall()
    for restaurant, dish, count in popular_dishes:
        print(f"   {restaurant}: {dish} ({count} orders)")
    print()
    
    # Question 4: Most profitable dish at each restaurant
    print("4. What was the most profitable dish at each restaurant?")
    cursor.execute('''
        SELECT restaurant_name, food_name, SUM(food_cost) as total_revenue
        FROM restaurant_transactions
        GROUP BY restaurant_name, food_name
        HAVING SUM(food_cost) = (
            SELECT MAX(revenue) FROM (
                SELECT SUM(food_cost) as revenue 
                FROM restaurant_transactions rt2 
                WHERE rt2.restaurant_name = restaurant_transactions.restaurant_name
                GROUP BY rt2.food_name
            )
        )
        ORDER BY restaurant_name
    ''')
    profitable_dishes = cursor.fetchall()
    for restaurant, dish, revenue in profitable_dishes:
        print(f"   {restaurant}: {dish} (${revenue:.2f})")
    print()
    
    # Question 5: Customer analysis
    print("5. Who visited each store the most, and who visited the most stores?")
    
    # Most frequent customer per restaurant
    print("   Most frequent customer per restaurant:")
    cursor.execute('''
        SELECT restaurant_name, customer_name, COUNT(*) as visits
        FROM restaurant_transactions
        GROUP BY restaurant_name, customer_name
        HAVING COUNT(*) = (
            SELECT MAX(cnt) FROM (
                SELECT COUNT(*) as cnt 
                FROM restaurant_transactions rt2 
                WHERE rt2.restaurant_name = restaurant_transactions.restaurant_name
                GROUP BY rt2.customer_name
            )
        )
        ORDER BY restaurant_name
    ''')
    top_customers = cursor.fetchall()
    for restaurant, customer, visits in top_customers:
        print(f"     {restaurant}: {customer} ({visits} visits)")
    
    # Customer who visited most stores
    print("\n   Customer who visited the most stores:")
    cursor.execute('''
        SELECT customer_name, COUNT(DISTINCT restaurant_name) as restaurants_visited
        FROM restaurant_transactions
        GROUP BY customer_name
        ORDER BY restaurants_visited DESC
        LIMIT 5
    ''')
    top_explorers = cursor.fetchall()
    for customer, restaurants_count in top_explorers:
        print(f"     {customer}: {restaurants_count} restaurants")
    
    conn.close()

if __name__ == "__main__":
    get_business_answers()
