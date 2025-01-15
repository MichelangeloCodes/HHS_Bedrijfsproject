import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64, String

class SensorPublisher(Node):
    def __init__(self):
        super().__init__('sensor_publisher')
        
        # Create publishers for the float and string
        self.float_publisher = self.create_publisher(Float64, '/float_data', 10)
        self.string_publisher = self.create_publisher(String, '/string_data', 10)

        # Timer to publish every second
        self.timer = self.create_timer(1.0, self.publish_message)

    def publish_message(self):
        # Publish float message
        float_msg = Float64()
        float_msg.data = 42.123  # Sample float value
        self.float_publisher.publish(float_msg)

        # Publish string message
        string_msg = String()
        string_msg.data = "Sensor 1"  # Sample string value
        self.string_publisher.publish(string_msg)

        self.get_logger().info(f'Publishing: Float = {float_msg.data}, String = {string_msg.data}')

def main(args=None):
    rclpy.init(args=args)
    sensor_publisher = SensorPublisher()

    try:
        rclpy.spin(sensor_publisher)
    except KeyboardInterrupt:
        pass

    finally:
        sensor_publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
