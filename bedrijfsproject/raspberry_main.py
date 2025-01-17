import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
from std_msgs.msg import String
import csv
import serial
import time
from datetime import datetime

# Setup UART for M5Stack communication
uart = serial.Serial('/dev/serial0', baudrate=115200, timeout=1)

class SensorDataReceiver(Node):
    def __init__(self):
        super().__init__('sensor_data_receiver')
        
        # Publisher for sending back sensor data
        self.publisher_ = self.create_publisher(String, "csv_data", 10)
        
        # Setup UART for M5Stack communication (should use self.uart)
        self.uart = serial.Serial('/dev/serial0', baudrate=115200, timeout=1)
        
        # Subscriber to wait for the number between 1 and 8
        self.subscription = self.create_subscription(
            Int32,
            'number_received',  # Topic name where the number will be published
            self.m5_stack,
            10
        )
        self.subscription  # Prevent unused variable warning
        

    def get_valid_response(self, ping_id):

        """
        Function to check if a valid response is received from the M5Stack.
        """
        try:
            # Wait for response
            time.sleep(0.2)  # Give time for the M5Stack to respond
            if self.uart.in_waiting > 0:
                response = self.uart.readline().decode('utf-8').strip()
                self.get_logger().info(f"Received: {response}")

                # Process the received CSV response
                parts = response.split(',')
                if len(parts) == 5:
                    received_id = int(parts[0])  # ID
                    temperature = float(parts[1])  # Temperature
                    humidity = float(parts[2])  # Humidity
                    co2 = float(parts[3])
                    light = float(parts[4])

                    # Get current time
                    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    self.get_logger().info(f"Response - ID: {received_id}, Temperature: {temperature}, Humidity: {humidity}, CO2: {co2}, Light: {light}, Time: {current_time}")

                    data = [[received_id, temperature, humidity, co2, light, current_time]]

                    # Correct file handling - opening for writing
                    filename = "sensor_data.csv"
                    with open(filename, mode="w", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerows(data)
                        self.get_logger().info(f"CSV data written to {filename}")

                    # Read back the content of the CSV file
                    with open(filename, "r") as file:
                        csv_content = file.read()

                    msg = String()
                    msg.data = csv_content
                    self.publisher_.publish(msg)
                    self.get_logger().info("CSV file sent.")
                    
                    # Check if the received ID matches
                    if str(received_id) == ping_id:
                        self.get_logger().info("Valid response received!")
                        return True
                    else:
                        self.get_logger().warn("Mismatched ID in response!")
                else:
                    self.get_logger().warn("Invalid response format.")
            else:
                self.get_logger().warn("No response received.")
        except Exception as e:
            self.get_logger().error(f"Error while receiving response: {e}")
        return False
    
    def m5_stack(self, msg):
        while True:
            try:
    
                ping_id = msg.data
                self.get_logger().info(f"Received number: {ping_id}")

                if ping_id.lower() == 'exit':
                    self.get_logger().warn("Programma beëindigd.")
                    break

                while True:
                    # Maak een ping-bericht in CSV-formaat
                    ping_message = f"ping,{ping_id}"
                    uart.write((ping_message + '\n').encode('utf-8'))
                    self.get_logger().info(f"Sent: {ping_message}")

                    # Controleer of de respons geldig is
                    if self.get_valid_response(ping_id):
                        break  # Stop als er een geldige respons is ontvangen

                    self.get_logger().warnnt("Retrying with the same ID...")
                    time.sleep(0.2)  # Wacht voordat opnieuw verzenden

            except Exception as e:
                self.get_logger().error(f"Error: {e}")

def main(args=None):
    rclpy.init(args=args)
    
    # Create the node
    node = SensorDataReceiver()
    
    # Spin to keep the node alive and listen for messages
    rclpy.spin(node)
    
    # Clean up
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()


