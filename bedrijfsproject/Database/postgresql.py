import psycopg2
import random

# Database connection parameters
db_params = {
    "dbname": "bedrijfsprojectdb",
    "user": "postgres",
    "password": "Tennis28",
    "host": "localhost",  # or the server's IP address
    "port": "5432"        # default PostgreSQL port
}

# def insert_data():

def insert_point(measurement_id, point_id, timestamp, sensor1, sensor2, sensor3, sensor4):
        
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        # Insert query
        query = """
        INSERT INTO datapoints (measurement_id, point_id, timestamp, sensor1, sensor2, sensor3, sensor4)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        data = (measurement_id, point_id, timestamp, sensor1, sensor2, sensor3, sensor4)
        cursor.execute(query, data)

        # Commit the changes
        connection.commit()
        print("Data inserted successfully.")


def next_measurement_id():
    # SQL to find the next id
    next_measuement_id_query = """
    SELECT COALESCE(MAX(measurement_id), 0) + 1 FROM datapoints;
    """

    # Get the next room_id
    cursor.execute(next_measuement_id_query)
    next_id = cursor.fetchone()[0]

    return next_id


try:
    # Connect to the database
    connection = psycopg2.connect(**db_params)

    # Create a cursor object
    cursor = connection.cursor()

    # Execute a simple query
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables
        WHERE table_schema = 'public';
    """)

    

    # Fetch the result
    db_version = cursor.fetchone()
    print("Connected to:", db_version)


    # Example usage
    for i in range(1, 60):
        i += 120
        insert_point(next_measurement_id(),
                    random.choice([1,2,3,4,5,6,7,8]),
                    f'2024-12-11 17:{i-120}:00',
                    round(random.uniform(18, 25), 1),
                    round(random.uniform(56, 68), 1),
                    round(random.uniform(3850, 4135), 1),
                    round(random.uniform(34, 45), 1))

        


except Exception as error:
    print("Error connecting to the database:", error)



finally:
    # Ensure the connection is closed
    if connection:
        cursor.close()
        connection.close()
        print("Database connection closed.")


