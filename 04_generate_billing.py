import mysql.connector
from datetime import datetime

config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Alfagamma1991',
    'database': 'edz_operations_db'
}

def generate_january_billing():
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # 1. Fetch readings and join with customers
        cursor.execute("""
            SELECT r.reading_id, r.customer_id, r.kwh_value, c.fixed_fee_usd 
            FROM fact_readings r
            JOIN dim_customer c ON r.customer_id = c.customer_id
            WHERE r.timestamp LIKE '2025-01-31%'
        """)
        reading_data = cursor.fetchall()

        bills = []
        tariff_usd = 0.12  
        exchange_rate = 89500  
        issue_date = '2025-02-01'
        due_date = '2025-02-15'
        
        bill_id_counter = 1

        for row in reading_data:
            r_id, c_id, kwh, fixed_charge_usd = row
            
            consumption_charge_usd = float(kwh) * tariff_usd
            total_amount_usd = round(float(fixed_charge_usd) + consumption_charge_usd, 2)
            total_amount_lbp = round(total_amount_usd * exchange_rate, -3) 
            
            status = 'Unpaid'

            bills.append((
                bill_id_counter, r_id, c_id, float(fixed_charge_usd), 
                round(consumption_charge_usd, 2), total_amount_lbp, total_amount_usd, 
                issue_date, due_date, status
            ))
            bill_id_counter += 1

        # 2. Precise Query matching your image_162bef.png columns
        query = """
            INSERT INTO fact_billing 
            (bill_id, reading_id, customer_id, fixed_charge_amount, consumption_charge_amount, 
             amount_lbp, amount_usd, issue_date, due_date, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Using explicit table references to avoid syntax errors
        print("Cleaning old billing data...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("TRUNCATE TABLE `edz_operations_db`.`fact_billing`;") # Backticks for safety
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

        print(f"Inserting {len(bills)} new bills...")
        cursor.executemany(query, bills)
        conn.commit()
        print("SUCCESS: Billing table populated perfectly.")

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    generate_january_billing()