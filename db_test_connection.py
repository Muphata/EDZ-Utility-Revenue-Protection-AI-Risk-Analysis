import mysql.connector

try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',         # username 
        password='Alfagamma1991', # ENTER YOUR MYSQL PASSWORD HERE
        database='edz_operations_db'
    )

    if connection.is_connected():
        print("Success! Python is now connected to the EDZ Database.")
        connection.close()

except Exception as e:
    print(f"Error: {e}")