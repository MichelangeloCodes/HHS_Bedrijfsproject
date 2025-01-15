import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import websockets
import asyncio
import json

class SimpleSubscriber(Node):
    def __init__(self):
        super().__init__('simple_subscriber')
        self.subscription = self.create_subscription(
            String,
            'data_topic',
            self.listener_callback,
            10
        )
        self.get_logger().info("Subscriber is running...")

    def listener_callback(self, msg):
        self.get_logger().info(f"Received: {msg.data}")
        # Deserialize JSON data
        data = json.loads(msg.data)
        asyncio.run(self.send_data_to_websocket(data))

    async def send_data_to_websocket(self, data):
        uri = "ws://localhost:8080"  # WebSocket server URL
        async with websockets.connect(uri) as websocket:
            await websocket.send(json.dumps(data))  # Send as JSON

def main():
    rclpy.init()
    node = SimpleSubscriber()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
