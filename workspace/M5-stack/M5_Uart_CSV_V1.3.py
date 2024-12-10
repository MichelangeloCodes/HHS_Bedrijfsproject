import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import CO2LUnit
from unit import DLightUnit
from unit import PAHUBUnit
from machine import UART
import time

i2c0 = None
pahub_0 = None
dlight_0 = None
co2l_0 = None

def setup():
    global i2c0, pahub_0, dlight_0, co2l_0, uart2
    M5.begin()
    uart2 = UART(2, baudrate=9600, tx=17, rx=18)
    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    co2l_0 = CO2LUnit(PAHUBUnit(i2c=i2c0, channel=0))
    dlight_0 = DLightUnit(PAHUBUnit(i2c=i2c0, channel=1))
    co2l_0.set_stop_periodic_measurement()
    co2l_0.set_start_periodic_measurement()
    # Stel UART in op TX=17 en RX=18

def sensor(ping_id):
  global i2c0, pahub_0, dlight_0, co2l_0
  M5.update()
  if co2l_0.is_data_ready() == True:
    temperature = co2l_0.temperature
    humidity = co2l_0.humidity
    co2 = co2l_0.co2
    light = dlight_0.get_lux()
    return(f"{ping_id},{temperature},{humidity}, {co2}, {light}")

def uart():
    global i2c0, pahub_0, dlight_0, co2l_0
    if uart2.any():  # Controleer of er data beschikbaar is
        try:
            # Lees en decodeer ontvangen data
            data = uart2.read().decode('utf-8').strip()
            print(f"Received: {data}")
            
            # Splits CSV-gegevens
            parts = data.split(',')
            if len(parts) == 2 and parts[0] == 'ping':
                # Extract ID
                ping_id = parts[1]
                
                # Maak een CSV-antwoord (ID, temperatuur, luchtvochtigheid)
                response = sensor(ping_id)
                
                # Stuur antwoord terug
                uart2.write(response + '\n')
                print(f"Sent: {response}")
        except Exception as e:
            print(f"Error: {e}")
    time.sleep(1)

if __name__ == '__main__':
    try:
        setup()
        while True:
            uart()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg
            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")

