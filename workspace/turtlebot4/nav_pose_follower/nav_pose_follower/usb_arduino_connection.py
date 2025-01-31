import serial
import time

def setup_serial(port='/dev/ttyUSB0', baudrate=9600, timeout=1):
    """Initialize and return a serial connection."""
    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(2)  # Allow time for the connection to establish
        if ser.is_open:
            print(f"Connected to {port} successfully.")
        else:
            print(f"Failed to open {port}.")
        return ser
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        return None

def send_data(ser, x, y, w):
    """Send formatted data over serial."""
    if ser and ser.is_open:
        data = f"{x},{y},{w}\n"
        ser.write(data.encode())
        print(f"Sent: {data.strip()}")
    else:
        print("Serial connection is not open.")

def receive_ack(ser):
    """Wait for an acknowledgment from the Arduino (expects '1')."""
    if ser and ser.is_open:
        while True:
            if ser.in_waiting > 0:  # Check if data is available to read
                response = ser.readline().decode().strip()  # Read and decode response
                print(f"Received: {response}")
                if response == "1":
                    return True
                else:
                    print("Invalid response, resending data...")
                    return False
    return False

if __name__ == "__main__":
    ser = setup_serial()

    if ser:
        try:
            while True:
                X_coor = 2.01
                Y_coor = -5.92
                W_orien = 1.00

                send_data(ser, X_coor, Y_coor, W_orien)

                # Wait for acknowledgment before proceeding
                if receive_ack(ser):
                    print("Acknowledgment received, continuing...")
                else:
                    print("No valid acknowledgment, retrying...")

                time.sleep(1)

        except KeyboardInterrupt:
            print("\nStopping transmission.")

        finally:
            ser.close()
            print("Serial connection closed.")
