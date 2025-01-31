import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from datetime import datetime
import psycopg2
from psycopg2 import sql
from rclpy.qos import QoSProfile

class CsvReceiver(Node):
    def __init__(self):
        super().__init__('csv_receiver')

        # Publisher to send the number_received to the Raspberry Pi
        self.publisher = self.create_publisher(String, 'number_received', qos_profile=QoSProfile(depth=10))
        self.timer = self.create_timer(900.0, self.send_number)

        # Subscriber to receive the CSV data back from the Raspberry Pi
        self.subscriber = self.create_subscription(
            String, 'csv_sent', self.csv_callback, qos_profile=QoSProfile(depth=10)
        )

    def send_number(self):
        # Call the method using the instance (`self`)
        number_sent = self.get_next_point_id(datetime.now())
        
        if number_sent is not None:
            # Publish the result
            msg = String()
            msg.data = str(number_sent)  # Ensure the data is a string
            self.publisher.publish(msg)
            self.get_logger().info(f'Sent number: {msg.data}')
        else:
            self.get_logger().warn("No point_id found to send.")

    def get_next_point_id(self, current_time):
        try:
            # Database connection parameters
            db_params = {
                "dbname": "postgres",
                "user": "postgres",
                "password": "Password",
                "host": "localhost",  # or the server's IP address
                "port": "5432"
            }

            # Use a context manager to ensure the connection is properly closed
            with psycopg2.connect(**db_params) as conn:
                with conn.cursor() as cursor:
                    # Format the current time to only HH:MM (ignores seconds)
                    current_time_dt = current_time.strftime("%H:%M")  # Fix this to match your DB time format

                    # Query to fetch the next point_id
                    query = """
                    SELECT point_id
                    FROM time_slots
                    WHERE time_slot > %s
                    ORDER BY time_slot ASC
                    LIMIT 1;
                    """
                    cursor.execute(query, (current_time_dt,))
                    result = cursor.fetchone()

                    # Return the point_id or None if not found
                    return result[0] if result else None

        except Exception as e:
            self.get_logger().error(f"Database error: {e}")
            return None

    def csv_callback(self, msg):
        # Callback function to handle the incoming CSV data
        self.get_logger().info(f'Received CSV data: {msg.data}')

        try:
            # Split the CSV string
            point_id, sensor_1, sensor_2, sensor_3, sensor_4, timestamp = msg.data.strip().split(',')

            data_str = [None] * 6
            # Convert fields to appropriate types
            data_str[0] = int(point_id)
            data_str[1]  = float(sensor_1)
            data_str[2]  = float(sensor_2)
            data_str[3]  = float(sensor_3)
            data_str[4]  = float(sensor_4)
            data_str[5]  = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

            #Uploads data to database
            self.store_data(data_str)
            
            #Display data in the log
            parsed_row = {
                "point_id": data_str[0],
                "sensor_1": data_str[1],
                "sensor_2": data_str[2],
                "sensor_3": data_str[3],
                "sensor_4": data_str[4],
                "timestamp": data_str[5]
            }

            # Log the parsed data
            self.get_logger().info(f"Parsed data: {parsed_row}")
        except Exception as e:
            self.get_logger().error(f"Failed to process message: {e}")

    def store_data(self, data_str):
        db_params = {
            "dbname": "postgres",
            "user": "postgres",
            "password": "Password",
            "host": "localhost",  # or the server's IP address
            "port": "5432"        # default PostgreSQL port
        }

        try:
            # Connect to the database
            connection = psycopg2.connect(**db_params)

            # Create a cursor object
            cursor = connection.cursor()

            next_measuement_id_query = """
            SELECT COALESCE(MAX(mmeasurement_id), 0) + 1 FROM datapoints;
            """

            # Get the next room_id
            cursor.execute(next_measuement_id_query)
            next_id = cursor.fetchone()[0]

            # Insert query
            query = """
            INSERT INTO datapoints (mmeasurement_id, point_id, timestamp, temperature, humidity, co2, light_intensity)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
            #       mesurement, point_id, time, sensor1, sensor2, sensor3, sensor4
            data = (next_id, data_str[0], data_str[5], data_str[1], data_str[2], data_str[3], data_str[4])
            cursor.execute(query, data)

            # Commit the changes
            connection.commit()

        except Exception as error:
            print("Error connecting to the database:", error)

        finally:
            # Ensure the connection is closed
            if connection:
                cursor.close()
                connection.close()
                print("Database connection closed.")


def main(args=None):
    rclpy.init(args=args)
    node = CsvReceiver()

    try:
        rclpy.spin(node)  # Keep the node alive and listening for messages
    except KeyboardInterrupt:
        node.get_logger().info("Node interrupted by user.")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()




