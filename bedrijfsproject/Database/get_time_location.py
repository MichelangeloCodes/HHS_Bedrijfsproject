import psycopg2
from datetime import datetime, timedelta

def get_next_point_id(current_time: str):
    """
    Fetch the next point_id for the given current time.
    
    Parameters:
        current_time (str): Current time in HH:MM format.
        
    Returns:
        int: The point_id of the next quarter-hour time slot, or None if not found.
    """
    try:
        # Connect to the PostgreSQL database
        db_params = {
            "dbname": "bedrijfsprojectdb",
            "user": "postgres",
            "password": "Tennis28",
            "host": "localhost",  # or the server's IP address
            "port": "5432"        # default PostgreSQL port
        }
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Format the current time
        current_time_dt = datetime.strptime(current_time, "%H:%M").time()

        # Query to fetch the next point_id based on the current time
        query = """
        SELECT point_id
        FROM time_slots
        WHERE time_slot > %s
        ORDER BY time_slot ASC
        LIMIT 1;
        """
        
        cursor.execute(query, (current_time_dt,))
        result = cursor.fetchone()
        
        # Return the point_id if found
        if result:
            return result[0]
        else:
            return None  # No next point_id found

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        # Close the database connection
        if 'conn' in locals() and conn:
            conn.close()

# Example usage
if __name__ == "__main__":
    current_time = input("Enter the current time (HH:MM): ")
    next_point_id = get_next_point_id(current_time)
    if next_point_id:
        print(f"The next point_id is: {next_point_id}")
    else:
        print("No next point_id found.")
