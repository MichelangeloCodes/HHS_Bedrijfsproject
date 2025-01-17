import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import csv
import random
from datetime import datetime
from rclpy.qos import QoSProfile
import serial
import time
from datetime import datetime  # Voor het verkrijgen van de huidige tijd

# Instellen van de UART-poort (vervang '/dev/serial0' indien nodig)
uart = serial.Serial('/dev/serial0', baudrate=115200, timeout=1)

def get_valid_response(ping_id):
    """
    Functie om te controleren of een geldige respons ontvangen is.
    """
    try:
        # Wacht op een antwoord
        time.sleep(0.2)  # Geef tijd aan de M5Stack om te reageren
        if uart.in_waiting > 0:
            response = uart.readline().decode('utf-8').strip()
            print(f"Received: {response}")

            # Verwerk het ontvangen CSV-antwoord
            parts = response.split(',')
            if len(parts) == 5:
                try:
                    # Try to parse the response data
                    received_id = int(parts[0])  # ID
                    temperature = float(parts[1])  # Temperatuur
                    humidity = float(parts[2])  # Luchtvochtigheid
                    co2 = float(parts[3])
                    light = float(parts[4])

                    # Verkrijg huidige tijd
                    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    # Voeg de tijd toe aan de respons
                    csv_line = [[received_id, temperature, humidity, co2, light, current_time]]

                    print(f"Response - ID: {received_id}, Temperature: {temperature}, Humidity: {humidity}, CO2: {co2}, Light: {light}, Tijd van ontvangst: {current_time}")

                    # Controleer of de ontvangen ID overeenkomt
                    if str(received_id) == ping_id:
                        print("Valid response received!")
                        return csv_line
                    else:
                        print("Mismatched ID in response!")
                except ValueError as e:
                    print(f"Error parsing data: {e}. Skipping malformed response.")
            else:
                print(f"Malformed response: {response}")
        else:
            print("No response received.")
    except Exception as e:
        print(f"Error while receiving response: {e}")
    return False

class CsvSender(Node):
    def __init__(self):
        super().__init__('csv_sender')

        # Subscriber to receive the number
        self.subscriber = self.create_subscription(
            String,
            'number_received',  # Topic name where the number will be published
            self.csv_callback,  # Callback function to handle the number
            qos_profile=QoSProfile(depth=10)
        )

        # Publisher to send the CSV content
        self.publisher_ = self.create_publisher(String, 'csv_sent', qos_profile=QoSProfile(depth=10))

        # Variable to track the current number
        self.current_number = 0

    def csv_callback(self, msg):
        """Callback function to handle the incoming number."""
        self.get_logger().info(f'Received number: {msg.data}')
        self.create_csv("example.csv", msg.data)

    def send_csv(self, file):
        """Send the created CSV file."""
        try:
            # Create the CSV file with the current number
            # self.create_csv("example.csv", str(self.current_number))
            with open("example.csv", "r") as file:
                csv_content = file.read()
                msg = String()
                msg.data = csv_content
                self.publisher_.publish(msg)
                self.get_logger().info("CSV file sent.")
                self.current_number += 1  # Increment the number

        except FileNotFoundError:
            self.get_logger().error("CSV file not found!")

    def create_csv(self, filename, ping_id):
        """Create a CSV file with dummy sensor data."""

        try:
            while True:
                # Maak een ping-bericht in CSV-formaat
                ping_message = f"ping,{ping_id}"
                uart.write((ping_message + '\n').encode('utf-8'))
                print(f"Sent: {ping_message}")

                # Controleer of de respons geldig is
                if get_valid_response(ping_id):
                    data = get_valid_response(ping_id)
                    break  # Stop als er een geldige respons is ontvangen

                print("Retrying with the same ID...")
                time.sleep(0.2)  # Wacht voordat opnieuw verzenden

        except Exception as e:
            print(f"Error: {e}")

        # data = get_valid_response(ping_id)
        self.get_logger().info(f"Sensor data is'{data}'")

        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data)

        self.get_logger().info(f"CSV file '{filename}' created with data: {data}")

        self.send_csv(file)


def main(args=None):
    rclpy.init(args=args)
    node = CsvSender()

    # Example of manually sending CSV; in a real application, this might be triggered by an event
    # node.send_csv()

    try:
        rclpy.spin(node)  # Keep the node alive and listening for messages
    except KeyboardInterrupt:
        node.get_logger().info("Node interrupted by user.")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()

