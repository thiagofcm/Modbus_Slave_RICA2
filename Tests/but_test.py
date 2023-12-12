import RPi.GPIO as GPIO
import time

#Define the GPIO pin
#pot_pin = 17
but_pin = 11

#GPIO Configuration
GPIO.setmode(GPIO.BOARD)
GPIO.setup(but_pin, GPIO.IN)

try:
    while True:
        val_but = GPIO.input(but_pin)
        print(f"Valor do botao: {val_but}")
        #if  val_but == True:
        #    print(f"Valor do botao: 1")
        #else:
        #    print(f"Valor do botao: 0")
        #time.sleep(0.1)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()

