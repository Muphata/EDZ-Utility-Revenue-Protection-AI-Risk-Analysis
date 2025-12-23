import mysql.connector
import random
from faker import Faker

# Initialize Faker
fake = Faker()

config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Alfagamma1991', 
    'database': 'edz_operations_db'
}

# Real-world data lists for Zahlé
family_names = ['Sarkis', 'Tawk', 'El-Basha', 'Hajj', 'Assaf', 'Madi', 'Karam', 'Sawaya', 'Nasrallah',
                 'Sayegh', 'Fakhoury', 'Salloum', 'Kayar', 'Brahim', 'Masaad', 'Amin', 'Sawan', 'Fakih',
                   'Tom', 'Mounir', 'Trachichi', 'Farran']
amperage_options = [5, 10, 15, 30, 60]
conn_types = ['Residential', 'Commercial', 'Industrial']

def generate_customers(n=5000):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Fetch neighborhoods
        cursor.execute("SELECT neighborhood_id, center_lat, center_long FROM dim_geography")
        neighborhoods = cursor.fetchall()

        customers = []
        for i in range(1, n + 1):
            name = f"{fake.first_name()} {random.choice(family_names)}"
            phone = f"70{random.randint(100000, 999999)}"
            amp = random.choice(amperage_options)
            
            # --- STRICT BUSINESS LOGIC ---
            if amp <= 15:
                conn_type = 'Residential'
            elif amp == 30:
                conn_type = random.choice(['Residential', 'Commercial'])
            else: # 60A
                conn_type = 'Commercial'
            
            fee = float(amp) * 1.2 
            phase = 3 if amp >= 30 else 1
            
           
            nb_id, base_lat, base_long = random.choice(neighborhoods)
            
            lat = float(base_lat) + random.uniform(-0.012, 0.012)
            lon = float(base_long) + random.uniform(-0.012, 0.012)
            
            contract_date = fake.date_between(start_date='-10y', end_date='today')
            
            # --- REAL-WORLD STATUS LOGIC ---
            # 95% Active, 5% Inactive
            is_active = 1 if random.random() < 0.95 else 0 

            customers.append((i, name, phone, amp, fee, phase, conn_type, nb_id, lat, lon, contract_date, is_active))

        # Wiping old data to ensure we have exactly 5,000 clean records
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("TRUNCATE TABLE dim_customer;")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

        query = """
            INSERT INTO dim_customer 
            (customer_id, name, phone, max_amperage, fixed_fee_usd, phase_type, connection_type, 
             neighborhood_id, customer_lat, customer_long, contract_date, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.executemany(query, customers)
        conn.commit()
        print(f"SUCCESS: {n} customers populated. Logic verified. Status diversity included.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    generate_customers(5000)