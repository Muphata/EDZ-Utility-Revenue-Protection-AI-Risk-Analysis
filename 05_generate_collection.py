import mysql.connector
import random
from datetime import datetime, timedelta

config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Alfagamma1991',
    'database': 'edz_operations_db'
}

def generate_january_collection():
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # 1. Fetch bill details
        cursor.execute("SELECT bill_id, amount_usd, issue_date FROM fact_billing")
        bills = cursor.fetchall()

        # 2. Fetch staff IDs with the specific role 'Reader/Collector'
        cursor.execute("SELECT staff_id FROM dim_staff WHERE role = 'Reader/Collector'")
        collectors = [row[0] for row in cursor.fetchall()]
        
        if not collectors:
            print("Error: No staff found with role 'Reader/Collector'. Please check your dim_staff table.")
            return

        collections = []
        updated_bills = []
        coll_id_counter = 1

        for bill in bills:
            b_id, amt_usd, issue_date = bill
            
            # Probability: 92% of customers pay their January bill
            if random.random() < 0.92:
                days_to_pay = random.randint(1, 14)
                pay_date = issue_date + timedelta(days=days_to_pay)
                
                c_staff = random.choice(collectors)
                
                # FIXED: method must be a string 'Cash', not a list ['Cash']
                method = 'Cash' 
                
                collections.append((
                    coll_id_counter, b_id, c_staff, float(amt_usd), pay_date, method
                ))
                
                updated_bills.append(('Paid', b_id))
                coll_id_counter += 1

        # 3. Insert into fact_collection
        query = """
            INSERT INTO fact_collection 
            (collection_id, bill_id, collector_id, amount_paid, collection_date, payment_method)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        print("Updating collection and billing status...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("TRUNCATE TABLE fact_collection;")

        cursor.executemany(query, collections)

        # 4. Update the Billing table status
        update_query = "UPDATE fact_billing SET status = %s WHERE bill_id = %s"
        cursor.executemany(update_query, updated_bills)

        conn.commit()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        
        print(f"SUCCESS: {len(collections)} payments recorded (All Cash).")
        print(f"MANAGEMENT NOTE: {len(bills) - len(collections)} bills remain 'Unpaid'.")

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    generate_january_collection()