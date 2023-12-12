import time
import board
import digitalio

PIN = board.D18

print("hello blinky!")

led = digitalio.DigitalInOut(PIN)
led.direction = digitalio.Direction.INPUT

while True:
    print("valor do botao: ", led.value)
