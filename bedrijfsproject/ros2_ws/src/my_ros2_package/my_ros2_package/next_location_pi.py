import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from datetime import datetime

class PiNode(Node):
    def __init__(self):
        super().__init__("pi_node")
        self.publisher_ = self.create_publisher(String, "time_topic", 10)
        self.subscriber_ = self.create_subscription(String, "location_topic", self.location_callback, 10)
        self.timer = self.create_timer(10.0, self.publish_time)

    def publish_time(self):
        current_time = datetime.now().strftime("%H:%M")
        msg = String()
        msg.data = current_time
        self.publisher_.publish(msg)
        self.get_logger().info(f"Sent time: {current_time}")

    def location_callback(self, msg):
        self.get_logger().info(f"Received location: {msg.data}")

def main(args=None):
    rclpy.init(args=args)
    node = PiNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
