#Volg de volgende stappen op de raspberry pi anders werkt het niet!
#1. sudo nano /boot/firmware/config.txt
#2. en enable Uart door enable_uart=1 te maken en save het bestand
#3. sudo nano /boot/firmware/cmdline.txt
#4. en haal de volgende lijn weg console=serial0,115200 en save het bestand

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
                received_id = int(parts[0])  # ID
                temperature = float(parts[1])  # Temperatuur
                humidity = float(parts[2])  # Luchtvochtigheid
                co2 = float(parts[3])
                light = float(parts[4])
                
                # Verkrijg huidige tijd
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Voeg de tijd toe aan de respons
                csv_line = f"{received_id},{temperature},{humidity},{co2},{light},{current_time}"

                print(f"Response - ID: {received_id}, Temperature: {temperature}, Humidity: {humidity}, co2: {co2}, Light: {light}, Tijd van ontvangst: {current_time}")
                
                # Controleer of de ontvangen ID overeenkomt
                if str(received_id) == ping_id:
                    print("Valid response received!")
                    return True
                else:
                    print("Mismatched ID in response!")
        else:
            print("No response received.")
    except Exception as e:
        print(f"Error while receiving response: {e}")
    return False

while True:
    try:
        # Vraag de gebruiker om een ID in te voeren
        ping_id = input("Voer een ping-ID in (of type 'exit' om te stoppen): ")
        if ping_id.lower() == 'exit':
            print("Programma beëindigd.")
            break

        while True:
            # Maak een ping-bericht in CSV-formaat
            ping_message = f"ping,{ping_id}"
            uart.write((ping_message + '\n').encode('utf-8'))
            print(f"Sent: {ping_message}")
            
            # Controleer of de respons geldig is
            if get_valid_response(ping_id):
                break  # Stop als er een geldige respons is ontvangen
            
            print("Retrying with the same ID...")
            time.sleep(0.2)  # Wacht voordat opnieuw verzenden

    except Exception as e:
        print(f"Error: {e}")

