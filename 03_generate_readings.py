import mysql.connector
import random
from datetime import datetime

config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Alfagamma1991',
    'database': 'edz_operations_db'
}

def generate_january_readings():
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # 1. Fetching active customers
        cursor.execute("""
            SELECT customer_id, max_amperage, customer_lat, customer_long, neighborhood_id 
            FROM dim_customer WHERE is_active = 1
        """)
        customers = cursor.fetchall()

        # 2. Map neighborhoods to staff (reader_id)
        cursor.execute("SELECT neighborhood_id, assigned_collector_id FROM dim_geography")
        geo_map = dict(cursor.fetchall())

        readings = []
        timestamp_val = '2025-01-31 10:00:00' 
        
        # MANUAL ID COUNTER: This solves Error 1364/1833
        current_id = 1

        for cust in customers:
            c_id, amp, c_lat, c_long, nb_id = cust
            r_id = geo_map.get(nb_id, 1) 

            # Consumption logic
            base_usage = amp * random.uniform(15, 40)
            kwh_val = round(base_usage, 2)

            # Audit GPS Logic
            if random.random() > 0.02:
                cap_lat = float(c_lat) + random.uniform(-0.0001, 0.0001)
                cap_long = float(c_long) + random.uniform(-0.0001, 0.0001)
            else:
                cap_lat = 33.8430 # Reader "stayed at the cafe"
                cap_long = 35.9080

            meter_id = 10000 + c_id 
            is_estimated = 0

            # Adding all columns including the manual reading_id
            readings.append((current_id, meter_id, c_id, r_id, kwh_val, cap_lat, cap_long, is_estimated, timestamp_val))
            current_id += 1

        # 3. Insert query including the reading_id
        query = """
            INSERT INTO fact_readings 
            (reading_id, meter_id, customer_id, reader_id, kwh_value, captured_lat, captured_long, is_estimated, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Clean the table before fresh insert
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("TRUNCATE TABLE fact_readings;")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

        cursor.executemany(query, readings)
        conn.commit()
        print(f"SUCCESS: {len(readings)} readings inserted manually. No MySQL Auto-Increment needed!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    generate_january_readings()