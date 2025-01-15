import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import csv
import random
from datetime import datetime

# Example function to create a CSV file
def create_csv(filename, id):

                    # random.choice([1,2])
                    # random.choice([1, 2, 3, 4])
    point_id = random.choice([1,2,3,4,5,6,7,8])                
    sensor1 =   round(random.uniform(18, 25), 1)
    sensor2 =   round(random.uniform(56, 68), 1)
    sensor3 =   round(random.uniform(3850, 4135), 1)
    sensor4 =   round(random.uniform(34, 45), 1)
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    data = [[point_id, sensor1, sensor2, sensor3, sensor4, formatted_datetime]]

    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

    return file



class CsvPublisher(Node):
    def __init__(self):
        super().__init__("csv_publisher")
        self.publisher_ = self.create_publisher(String, "csv_data", 10)
        self.timer = self.create_timer(10.0, self.publish_csv)
        self.current_number = 1  # Start with 1

    def publish_csv(self):
        try:
            create_csv("example.csv", self.current_number)
            with open("example.csv", "r") as file:
                csv_content = file.read()
                msg = String()
                msg.data = csv_content
                self.publisher_.publish(msg)
                self.get_logger().info("CSV file sent.")
                self.current_number += 1  # Increment the number

        except FileNotFoundError:
            self.get_logger().error("CSV file not found!")

def main(args=None):
    rclpy.init(args=args)
    node = CsvPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
