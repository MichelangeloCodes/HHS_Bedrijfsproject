import serial
import time
from datetime import datetime

# Instellen van de UART-poort (vervang '/dev/serial0' indien nodig)
uart = serial.Serial('/dev/serial0', baudrate=115200, timeout=1)

def get_valid_response(ping_id, start_time):
    """
    Functie om een geldig antwoord te ontvangen en de vertraging te meten.
    """
    try:
        if uart.in_waiting > 0:
            response = uart.readline().decode('utf-8').strip()
            print(f"Received: {response}")

            # Verwerk het ontvangen CSV-antwoord
            parts = response.split(',')
            if len(parts) == 5:
                received_id = int(parts[0])  # ID
                temperature = float(parts[1])  # Temperatuur
                humidity = float(parts[2])  # Luchtvochtigheid
                co2 = float(parts[3])
                light = float(parts[4])

                # Controleer of de ontvangen ID overeenkomt
                if str(received_id) == ping_id:
                    print("Valid response received!")
                    end_time = time.time()
                    delay = end_time - start_time
                    print(f"Delay: {delay:.4f} seconds")
                    return delay
                else:
                    print("Mismatched ID in response!")
        return None
    except Exception as e:
        print(f"Error while receiving response: {e}")
        return None

def measure_ping_times():
    """
Meet de vertraging tussen het verzenden en ontvangen van pings.
    """
    results = []

    for i in range(100):  # Meet 100 keer
        try:
            while True:  # Blijf proberen met dezelfde ping totdat een geldige respons wordt ontvangen
                # Verzenden van ping met tijdstip
                ping_id = str(i + 1)  # Uniek ID per ping
                ping_message = f"ping,{ping_id}"
                start_time = time.time()
                uart.write((ping_message + '\n').encode('utf-8'))
                print(f"Sent: {ping_message} at {datetime.now().strftime('%H:%M:%S')}")

                # Probeer een geldige respons te krijgen
                delay = get_valid_response(ping_id, start_time)
                if delay is not None:
                    results.append(delay)
                    break  # Stop de poging en ga naar de volgende ping
                else:
                    print("No response, retrying immediately...")
                    time.sleep(0.3)  # Korte wachttijd voordat opnieuw geprobeerd wordt

            # Wacht 3 seconden voordat de volgende ping wordt verzonden
            time.sleep(3)

        except Exception as e:
            print(f"Error during ping: {e}")
            results.append(None)

    # Schrijf resultaten naar bestand
    with open("ping_times.csv", "w") as file:
        file.write("Ping ID,Delay (seconds)\n")
        for idx, delay in enumerate(results):
            file.write(f"{idx + 1},{delay if delay is not None else 'Error'}\n")
    print("Ping times saved to ping_times.csv")

if __name__ == "__main__":
    try:
        measure_ping_times()
    except KeyboardInterrupt:
        print("Programma beëindigd door gebruiker.")