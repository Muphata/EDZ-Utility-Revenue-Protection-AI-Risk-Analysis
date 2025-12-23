import mysql.connector
import random
from datetime import datetime

config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Alfagamma1991',
    'database': 'edz_operations_db'
}

def generate_january_expenses():
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # 1. Get staff and neighborhood IDs for realistic mapping
        cursor.execute("SELECT staff_id FROM dim_staff")
        staff_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT neighborhood_id FROM dim_geography")
        neighborhood_ids = [row[0] for row in cursor.fetchall()]

        expenses = []
        expense_id_counter = 1
        january_date = '2025-01-31'

        # --- A. GENERATE SALARIES (Fixed Expense) ---
        for s_id in staff_ids:
            expenses.append((
                expense_id_counter, 'Salaries', 800.00, january_date, s_id, None
            ))
            expense_id_counter += 1

        # --- B. GENERATE FUEL COSTS (Per Neighborhood) ---
        # Fuel is neighborhood-specific because of the generators located there
        for n_id in neighborhood_ids:
            fuel_cost = random.uniform(5000, 12000) # Realistic monthly diesel cost per area
            expenses.append((
                expense_id_counter, 'Fuel/Diesel', round(fuel_cost, 2), january_date, None, n_id
            ))
            expense_id_counter += 1

        # --- C. GENERATE MAINTENANCE (Random Anomalies) ---
        for _ in range(5):
            maint_cost = random.uniform(200, 1500)
            expenses.append((
                expense_id_counter, 'Maintenance', round(maint_cost, 2), january_date, 
                random.choice(staff_ids), random.choice(neighborhood_ids)
            ))
            expense_id_counter += 1

        # 2. Insert into dim_expenses table
        query = """
            INSERT INTO dim_expenses 
            (expense_id, category, amount_usd, date, staff_id, neighborhood_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("TRUNCATE TABLE dim_expenses;")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

        cursor.executemany(query, expenses)
        conn.commit()
        print(f"SUCCESS: {len(expenses)} operational expenses recorded for January.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    generate_january_expenses()