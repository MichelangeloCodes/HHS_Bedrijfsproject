import rclpy
from rclpy.node import Node
from my_interfaces.msg import Custom  # Import the custom message

class SubscriberNode(Node):
    def __init__(self):
        super().__init__('subscriber_node')
        self.subscription = self.create_subscription(
            Custom,  # Message type
            'float_data_topic',  # Topic name
            self.listener_callback,  # Callback function
            10  # Queue size
        )

    def listener_callback(self, msg):
        self.get_logger().info(f'Received: {msg.description}, {msg.data}')  # Print received value


def main(args=None):
    rclpy.init(args=args)
    node = SubscriberNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
