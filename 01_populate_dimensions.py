import mysql.connector

config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Alfagamma1991',
    'database': 'edz_operations_db'
}

def populate_dims():
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # 1. Balanced & Diverse Staff (10 People)
        staff_data = [
            (1, 'Ahmad Hamdan', 'Reader/Collector', '70111222', 1),
            (2, 'Jean Khoury', 'Reader/Collector', '03222333', 1),
            (3, 'Mustafa Khalifeh', 'Admin', '71333444', 1),
            (4, 'Elias Abu Faisal', 'Reader/Collector', '76444555', 1),
            (5, 'Hassan Jaber', 'Technician', '03555666', 1),
            (6, 'Michel Haddad', 'Reader/Collector', '70666777', 1),
            (7, 'Omar Dandach', 'Reader/Collector', '71777888', 1),
            (8, 'Rita Maalouf', 'Reader/Collector', '76888999', 1), 
            (9, 'Bilal Zein', 'Technician', '03999000', 1),
            (10, 'George Scaff', 'Reader/Collector', '70000111', 1)
        ]
        
        cursor.executemany("""
            INSERT IGNORE INTO dim_staff (staff_id, staff_name, role, phone_number, active_status) 
            VALUES (%s, %s, %s, %s, %s)
        """, staff_data)

        # 2. Neighborhoods (6 Zones)
        geo_data = [
            (1, 'Houch El Omara', 33.8463, 35.9020, 1), 
            (2, 'Maallaqa', 33.8490, 35.8950, 2),      
            (3, 'Midane', 33.8430, 35.9080, 4),        
            (4, 'Barbara', 33.8510, 35.8910, 6),
            (5, 'Ksara', 33.8290, 35.8940, 10),     
            (6, 'Saadnayel', 33.8120, 35.8920, 7)   
        ]
        
        cursor.executemany("""
            INSERT IGNORE INTO dim_geography (neighborhood_id, neighborhood_name, center_lat, center_long, assigned_collector_id) 
            VALUES (%s, %s, %s, %s, %s)
        """, geo_data)

        conn.commit()
        print(f"Successfully populated dimensions! Staff: 10, Neighborhoods: 6")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    populate_dims()