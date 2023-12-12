import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from time import sleep

#Initialize the I2C interface
i2c = busio.I2C(board.SCL, board.SDA)

#Create an ADS1115 object
ads = ADS.ADS1115(i2c)
 
#Define the analog input channel
channel = AnalogIn(ads, ADS.P0)
  
#Loop to read the analog input continuously
while True:
    #print("Analog Value: ",channel.value, "Voltage: ", channel.voltage)
    #temp = channel.voltage
    temp = round(channel.voltage/0.010, 3)
    print("Temperatura: ", temp, "°C")
    sleep(1)
