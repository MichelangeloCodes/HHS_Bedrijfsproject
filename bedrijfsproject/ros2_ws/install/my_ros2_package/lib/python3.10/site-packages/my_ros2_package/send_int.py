import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class IntPublisher(Node):
    def __init__(self):
        super().__init__('int_publisher')
        self.publisher_ = self.create_publisher(Int32, '/int_topic', 10)
        self.timer = self.create_timer(1.0, self.publish_int)  # Publish every 1 second
        self.count = 0

    def publish_int(self):
        msg = Int32()
        msg.data = self.count
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published: {msg.data}')
        self.count += 1

def main(args=None):
    rclpy.init(args=args)
    node = IntPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()