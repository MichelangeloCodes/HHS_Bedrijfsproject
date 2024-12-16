import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from csv_subscriber.csv_writer import write_csv

class Subscriber(Node):
    def __init__(self):
        super().__init__('remote_csv_subscriber')
        self.subscription = self.create_subscription(String, '/csv_data', self.listener_callback, 10)
        self.subscription
        self.csv_data = []

    def listener_callback(self, msg):
        self.get_logger().info(f'Received message: "{msg.data}"')

        parsed_data = self.parse_message(msg.data)
        if parsed_data:
            self.csv_data.append(parsed_data)  # Add the parsed data to the list
            write_csv(self.csv_data)  # Write data to CSV file

    def parse_message(self, data):
        try:
            name, age = data.split(',')
            return {'name': name.strip(), 'age': age.strip()}
        except ValueError:
            self.get_logger().error('Invalid message format. Expected "name,age".')
            return None



def main(args=None):
    rclpy.init(args=args)
    subscriber = Subscriber()
    rclpy.spin(subscriber)

    subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

