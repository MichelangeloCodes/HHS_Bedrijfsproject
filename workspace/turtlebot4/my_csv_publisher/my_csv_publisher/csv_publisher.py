
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import csv

class CSVPublisher(Node):
    def __init__(self):
        super().__init__('csv_publisher')
        self.publisher_ = self.create_publisher(String, 'csv_data', 10)
        self.timer = self.create_timer(1.0, self.publish_csv_data)  # Publish every second
        self.csv_file = 'data.csv'  # Update this to your CSV file path
        self.csv_data = self.load_csv_data()
        self.row_index = 0

    def load_csv_data(self):
        try:
            with open(self.csv_file, 'r') as file:
                reader = csv.reader(file)
                return list(reader)
        except FileNotFoundError:
            self.get_logger().error(f"CSV file '{self.csv_file}' not found.")
            return []

    def publish_csv_data(self):
        if self.row_index < len(self.csv_data):
            row = self.csv_data[self.row_index]
            message = String()
            message.data = ','.join(row)  # Convert the row to a comma-separated string
            self.publisher_.publish(message)
            self.get_logger().info(f'Publishing: {message.data}')
            self.row_index += 1
        else:
            self.get_logger().info('All CSV rows have been published.')
            self.destroy_timer(self.timer)

def main(args=None):
    rclpy.init(args=args)
    node = CSVPublisher()
    rclpy.spin(node)
    rclpy.shutdown()
