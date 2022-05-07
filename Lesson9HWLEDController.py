import RPi.GPIO as GPIO
from time import sleep

DutyCycle = 1.0
DutyCycleUpperLimit = 100.0/1.0
DutyCycleLowerLimit = 0.0/1.0
Frequency = 100
Increment = 100.0/8.0
Delay = .1

LEDPin = 37
BrighterPin = 38
DimmerPin = 40

BrighterState = 0
BrighterStateOld = 0
DimmerState = 0
DimmerStateOld = 0
LEDDutyCycle = 0

GPIO.setmode(GPIO.BOARD)
GPIO.setup(LEDPin, GPIO.OUT)
GPIO.setup(BrighterPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DimmerPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

LEDPWM = GPIO.PWM(LEDPin, Frequency)

try:
    while True:
        BrighterState = GPIO.input(BrighterPin)
        print("BrighterState = ", BrighterState)
        if BrighterState == 1 and BrighterStateOld == 0:
            DutyCycle = DutyCycle + Increment
            if DutyCycle > DutyCycleUpperLimit:
                DutyCycle = DutyCycleUpperLimit
        BrighterStateOld = BrighterState
        DimmerState = GPIO.input(DimmerPin)
        print("DimmerState = ", DimmerState)
        if DimmerState == 1 and DimmerStateOld == 0:
            DutyCycle = DutyCycle - Increment
            if DutyCycle < DutyCycleLowerLimit:
                DutyCycle = DutyCycleLowerLimit
        print("DutyCycle = ", DutyCycle)
        LEDPWM.start(DutyCycle)
        DimmerStateOld = DimmerState
        sleep(Delay)
except KeyboardInterrupt:
    print("\nThat's all folks")
    LEDPWM.stop()
    GPIO.cleanup()
