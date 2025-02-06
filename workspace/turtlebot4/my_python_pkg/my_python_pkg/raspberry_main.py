import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import csv
import time
import serial
from datetime import datetime
from rclpy.qos import QoSProfile

# Instellen van de UART-poort (vervang '/dev/ttyAMA0' indien nodig)
uart = serial.Serial('/dev/ttyAMA0', baudrate=115200, timeout=1)

def get_valid_response(ping_id):
    """
    Functie om te controleren of een geldige respons ontvangen is.
    """
    try:
        time.sleep(0.2)  # Geef tijd aan de M5Stack om te reageren
        if uart.in_waiting > 0:
            response = uart.readline().decode('utf-8').strip()
            print(f"Received: {response}")

            parts = response.split(',')
            if len(parts) == 5:
                try:
                    received_id = int(parts[0])
                    temperature = float(parts[1])
                    humidity = float(parts[2])
                    co2 = float(parts[3])
                    light = float(parts[4])
                    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    csv_line = [[received_id, temperature, humidity, co2, light, current_time]]
                    print(f"Valid response: ID={received_id}, Temp={temperature}, Humidity={humidity}, CO2={co2}, Light={light}")

                    if str(received_id) == ping_id:
                        return True, csv_line
                    else:
                        print("Mismatched ID in response!")
                except ValueError:
                    print("Error parsing data, skipping malformed response.")
            else:
                print("Malformed response received.")
        else:
            print("No response received.")
    except Exception as e:
        print(f"Error receiving response: {e}")
    return False, None

class CsvSender(Node):
    def __init__(self):
        super().__init__('csv_sender')

        # Subscriber voor toestemming meten
        self.toestemming_subscriber = self.create_subscription(
            String,
            '/toestemming_meten',
            self.toestemming_callback,
            QoSProfile(depth=10)
        )

        # Subscriber om nummer te ontvangen
        self.subscriber = self.create_subscription(
            String,
            'number_received',
            self.csv_callback,
            QoSProfile(depth=10)
        )

        # Publisher om de CSV te versturen
        self.publisher_ = self.create_publisher(String, 'csv_sent', QoSProfile(depth=10))

        # Publisher om toestemming terug te sturen
        self.toestemming_publisher = self.create_publisher(String, '/toestemming_meten', QoSProfile(depth=10))

        # Variabele om toestemming te tracken
        self.toestemming_ontvangen = False
        self.wachtende_ping_id = None

    def toestemming_callback(self, msg):
        """Callback voor toestemming ontvangen"""
        if msg.data == "1":
            self.get_logger().info("Toestemming ontvangen! Metingen worden gestart.")
            self.toestemming_ontvangen = True

            self.get_logger().info("CHECK.")
            self.create_csv("example.csv", self.wachtende_ping_id)
            self.wachtende_ping_id = None  # Reset wachtende ID

    def csv_callback(self, msg):
        """Callback om het ontvangen nummer te verwerken."""
        self.get_logger().info(f'Received number: {msg.data}')

        # Start direct met meten als toestemming al binnen is
        if self.toestemming_ontvangen:
            self.create_csv("example.csv", msg.data)
        else:
            self.get_logger().info("Nog geen toestemming ontvangen, wachtend...")
            self.wachtende_ping_id = msg.data  # Wacht tot toestemming komt

    def send_csv(self, file):
        """Stuur de aangemaakte CSV."""
        try:
            with open("example.csv", "r") as file:
                csv_content = file.read()
                msg = String()
                msg.data = csv_content
                self.publisher_.publish(msg)
                self.get_logger().info("CSV file sent.")
        except FileNotFoundError:
            self.get_logger().error("CSV file not found!")

        # Na het verzenden van de CSV, stuur een 0 terug naar toestemming_meten
        self.send_toestemming_terug()

    def send_toestemming_terug(self):
        """Stuurt een 0 naar /toestemming_meten om toestemming in te trekken."""
        msg = String()
        msg.data = "0"
        self.toestemming_publisher.publish(msg)
        self.get_logger().info("Toestemming ingetrokken (0 verzonden).")

    def create_csv(self, filename, ping_id):
        """Maak een CSV-bestand met sensorgegevens."""
        try:
            while True:
                ping_message = f"ping,{ping_id}"
                uart.write((ping_message + '\n').encode('utf-8'))
                print(f"Sent: {ping_message}")

                pass_value, csv_line = get_valid_response(ping_id)
                if pass_value:
                    data = csv_line
                    break  # Stop als er een geldige respons is ontvangen

                print("Retrying with the same ID...")
                time.sleep(0.2)

        except Exception as e:
            print(f"Error: {e}")

        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data)

        self.get_logger().info(f"CSV file '{filename}' created with data: {data}")

        self.send_csv(file)

def main(args=None):
    rclpy.init(args=args)
    node = CsvSender()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Node interrupted by user.")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
