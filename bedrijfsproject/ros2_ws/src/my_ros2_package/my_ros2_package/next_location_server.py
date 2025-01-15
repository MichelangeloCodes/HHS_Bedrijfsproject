import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import psycopg2
from datetime import datetime

class LaptopNode(Node):
    def __init__(self):
        super().__init__("laptop_node")
        self.subscriber_ = self.create_subscription(String, "time_topic", self.time_callback, 10)
        self.publisher_ = self.create_publisher(String, "location_topic", 10)

    def time_callback(self, msg):
        current_time = msg.data
        self.get_logger().info(f"Received time: {current_time}")
        
        # Get the next point_id from the database
        next_point_id = self.get_next_point_id(current_time)
        
        # Publish the location (point_id) back to the Raspberry Pi
        location_msg = String()
        if next_point_id:
            location_msg.data = f"Next point_id: {next_point_id}"
        else:
            location_msg.data = "No next point_id found."
        
        self.publisher_.publish(location_msg)
        self.get_logger().info(f"Sent location: {location_msg.data}")

    def get_next_point_id(self, current_time):
        try:
            # Database connection parameters
            db_params = {
                "dbname": "bedrijfsprojectdb",
                "user": "postgres",
                "password": "Tennis28",
                "host": "localhost",  # or the database server's IP address
                "port": "5432"
            }
            conn = psycopg2.connect(**db_params)
            cursor = conn.cursor()

            # Format the current time
            current_time_dt = datetime.strptime(current_time, "%H:%M").time()

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
            conn.close()

            return result[0] if result else None

        except Exception as e:
            self.get_logger().error(f"Database error: {e}")
            return None

def main(args=None):
    rclpy.init(args=args)
    node = LaptopNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
