import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from datetime import datetime
import psycopg2

class CSVSubscriber(Node):
    def __init__(self):
        super().__init__('csv_subscriber')
        self.subscription = self.create_subscription(
            String,
            'csv_data',  # Topic name
            self.listener_callback,
            10
        )

    def listener_callback(self, msg):
        # Log the received data
        self.get_logger().info(f"Received row: {msg.data}")

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
            "dbname": "bedrijfsprojectdb",
            "user": "postgres",
            "password": "Tennis28",
            "host": "localhost",  # or the server's IP address
            "port": "5432"        # default PostgreSQL port
        }

        try:
            # Connect to the database
            connection = psycopg2.connect(**db_params)

            # Create a cursor object
            cursor = connection.cursor()

            next_measuement_id_query = """
            SELECT COALESCE(MAX(measurement_id), 0) + 1 FROM datapoints;
            """

            # Get the next room_id
            cursor.execute(next_measuement_id_query)
            next_id = cursor.fetchone()[0]

            # Insert query
            query = """
            INSERT INTO datapoints (measurement_id, point_id, timestamp, sensor1, sensor2, sensor3, sensor4)
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
    node = CSVSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
