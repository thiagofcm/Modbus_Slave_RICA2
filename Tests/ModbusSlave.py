#!/bin/python

import board
import busio
import digitalio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO
from pyModbusTCP.server import ModbusServer
from time import sleep
from random import uniform

#GPIO Definitions
#Switch Button:
PIN = board.D17
but_pin = digitalio.DigitalInOut(PIN)
but_pin.direction = digitalio.Direction.INPUT

#Level Sensor Button:
PIN_LEVEL = board.D18
but_level = digitalio.DigitalInOut(PIN_LEVEL)
but_level.direction = digitalio.Direction.INPUT

#GREEN LED
PIN_GREEN_LED = board.D27
green_led_value = digitalio.DigitalInOut(PIN_GREEN_LED)
green_led_value.direction = digitalio.Direction.OUTPUT

#YELLOW LED
PIN_YELLOW_LED = board.D22
yellow_led_value = digitalio.DigitalInOut(PIN_YELLOW_LED)
yellow_led_value.direction = digitalio.Direction.OUTPUT

#RED LED
PIN_RED_LED = board.D23
red_led_value = digitalio.DigitalInOut(PIN_RED_LED)
red_led_value.direction = digitalio.Direction.OUTPUT

#I2C Configurations:
#Cria uma instância da interface I2C
i2c = busio.I2C(board.SCL, board.SDA)
#Cria uma instância do objeto ADS1115
ads = ADS.ADS1115(i2c)
#Cria uma instância do canal analógico no pino A0
chan = AnalogIn(ads, ADS.P0)

#Auxiliar Variables:
aux = True
aux_switch = True
holding_value = 0
aux_level = True
led_warning_aux = True
led_status_message_aux = False

#Create an instance of ModbusServer
server = ModbusServer("169.254.113.124",502, no_block=True) #(Master IP Adress)
try:
    print("Start server...")
    server.start()
    print("Server is online")
    server.data_bank.set_holding_registers(0,[holding_value])
    
    while True:

        #Variable Definitions
        temp_value = round(chan.voltage/0.010,2)
        switch_state = but_pin.value
        level_state = but_level.value

        #Holding Registers Function (Valve Value - ADDRES: 40001 - AO):
        current_holding = server.data_bank.get_holding_registers(0,1)
        if(current_holding != holding_value):
            print(f"[VALVE] Register number 40001 of Holding Registers Function has changed from {holding_value} to {current_holding}")
            holding_value = current_holding

        #Input Status Function (Switch - ADDRES: 10001 - DI  /  Level_Sensor - ADDRES: 10002 - DI):
        server.data_bank.set_discrete_inputs(0,[switch_state])
        if switch_state != aux_switch:
            print(f"[SWITCH] Register number 10001 of Input Status Function has changed from {aux_switch} to {switch_state}")
            aux_switch = switch_state
        
        server.data_bank.set_discrete_inputs(1,[level_state])
        print(level_state)
        if level_state != aux_level:
            print(f"[LEVEL SENSOR] Register number 10002 of Input Status Function has changed from {aux_level} to {level_state}")
            aux_level = level_state

        #Coil Status Function (LED ON - ADDRES: 00001 - DO / LED WARNING - ADDRES: 00002 - DO / LED STATUS MESSAGE - ADDRES: 00003 - DO):
        coil = server.data_bank.get_coils(0,1)
        if coil == [True]:
            green_led_value.value = True
        else:
            green_led_value.value = False
        if coil != aux:
            print(f"[GREEN LED] Register number 00001 of Coil Status Function has changed from {aux} to {coil}")
            aux = coil

        led_warning_state = server.data_bank.get_coils(1,1)
        if led_warning_state == [True]:
            yellow_led_value.value = True
        else:
            yellow_led_value.value = False

        if led_warning_state != led_warning_aux:
            print(f"[YELLOW LED] Register number 00002 of Coil Status Function has changed from {led_warning_aux} to {led_warning_state}")
            led_warning_aux = led_warning_state

        led_status_message = server.data_bank.get_coils(2,1)
        if led_status_message == [True]:
            red_led_value.value = True
        else:
            red_led_value.value = False

        if led_status_message != led_status_message_aux:
            print(f"[RED LED] Register number 00003 of Coil Status Function has changed from {led_status_message_aux} to {led_status_message}")
            led_status_message_aux = led_status_message

        #Input Registers Function (Temperature Sensor - ADDRES: 30001 - AI):
        server.data_bank.set_input_registers(0,[temp_value])
        if(switch_state == True):
            print(f"[TEMP] Temperature Value: {temp_value} °C")

        sleep(0.5)

except:
    green_led_value.value = False
    yellow_led_value.value = False
    red_led_value.value = False
    print("Shutdown server...")
    server.stop()
    print("Server is offline")
        
