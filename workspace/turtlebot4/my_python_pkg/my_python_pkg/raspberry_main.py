class CsvSender(Node):
    def __init__(self):
        super().__init__('csv_sender')

        self.toestemming_subscriber = self.create_subscription(
            String,
            '/toestemming_meten',
            self.toestemming_callback,
            QoSProfile(depth=10)
        )

        self.subscriber = self.create_subscription(
            String,
            'number_received',
            self.csv_callback,
            QoSProfile(depth=10)
        )

        self.publisher_ = self.create_publisher(String, 'csv_sent', QoSProfile(depth=10))
        self.toestemming_publisher = self.create_publisher(String, '/toestemming_meten', QoSProfile(depth=10))

        self.toestemming_ontvangen = False
        self.wachtende_ping_id = None

    def toestemming_callback(self, msg):
        """Callback voor toestemming ontvangen"""
        if msg.data == "1":
            self.get_logger().info("Toestemming ontvangen! Metingen worden gestart.")
            self.toestemming_ontvangen = True

            if self.wachtende_ping_id is not None:
                self.get_logger().info(f"Verzenden met wachtende ID: {self.wachtende_ping_id}")
                self.create_csv("example.csv", self.wachtende_ping_id)
            else:
                self.get_logger().info("Geen ping ID ontvangen, wachten op een nummer.")

            self.wachtende_ping_id = None  # Reset wachtende ID

    def csv_callback(self, msg):
        """Callback om het ontvangen nummer te verwerken."""
        self.get_logger().info(f'Received number: {msg.data}')

        if self.toestemming_ontvangen:
            self.create_csv("example.csv", msg.data)
        else:
            self.get_logger().info("Nog geen toestemming ontvangen, wachtend...")
            self.wachtende_ping_id = msg.data  # Wacht tot toestemming komt

    def create_csv(self, filename, ping_id):
        """Maak een CSV-bestand met sensorgegevens."""
        if ping_id is None:
            self.get_logger().error("Ping ID is None, kan geen CSV aanmaken!")
            return

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

