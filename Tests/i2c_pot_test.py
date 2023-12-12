import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Cria uma instância da interface I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Cria uma instância do objeto ADS1115
ads = ADS.ADS1115(i2c)

# Cria uma instância do canal analógico no pino A0
chan = AnalogIn(ads, ADS.P0)

try:
    while True:
        # Lê o valor do potenciômetro
        pot_value = chan.value 
        scaled_value = int((pot_value/ 32767.0) * 1024)
        print("Valor do Potenciômetro:", scaled_value)
        time.sleep(0.5)

except KeyboardInterrupt:
    pass
