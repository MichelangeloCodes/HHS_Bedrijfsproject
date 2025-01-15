import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json
import random

class SimplePublisher(Node):
    def __init__(self):
        super().__init__('simple_publisher')
        self.publisher_ = self.create_publisher(String, 'data_topic', 10)
        self.timer = self.create_timer(1, self.timer_callback)
        self.get_logger().info("Publisher is running...")

    def timer_callback(self):
        data = {
            "value": random.uniform(0.0, 100.0),  # Example float32 value
            "description": "This is a float32 example value"
        }
        msg = String()
        msg.data = json.dumps(data)  # Convert to JSON string
        self.publisher_.publish(msg)
        self.get_logger().info(f"Published: {msg.data}")

def main():
    rclpy.init()
    node = SimplePublisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
