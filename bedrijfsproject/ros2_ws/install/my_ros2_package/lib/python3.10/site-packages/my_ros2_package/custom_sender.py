import rclpy
from rclpy.node import Node
from my_interfaces.msg import Custom  # Import the custom message
import random

class PublisherNode(Node):
    def __init__(self):
        super().__init__('publisher_node')
        self.publisher_ = self.create_publisher(Custom, 'float_data_topic', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)  # Publish every second

    def timer_callback(self):
        msg = Custom()
        msg.data = random.uniform(0.0, 100.0)  # Set the float data value
        msg.description = 'Sensor 1'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: data={msg.data}, description={msg.description}')


def main(args=None):
    rclpy.init(args=args)
    node = PublisherNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
