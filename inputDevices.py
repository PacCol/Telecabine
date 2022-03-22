import gpiozero
from subprocess import check_call
from time import sleep
import status
from lift import lights, motors
import display.display as display


class illuminatedPushButton():

    def __init__(self):
        self.button = gpiozero.Button(24)
        self.led = gpiozero.PWMLED(23)
        self.led.pulse()

        def toggleStatus():
            if lights.getStatus():
                status.setStatus(None, False)
            else:
                status.setStatus(None, True)
            sleep(0.4)

        def shutdown():
            display.displayOFF()
            check_call(['sudo', 'poweroff'])

        self.button.when_released = toggleStatus
        self.button.when_held = shutdown

    def showLightsEnabled(self, enabled):
        if enabled:
            led.off()
            led.on()
        else:
            led.off()
            led.pulse()


class rotaryEncoder():

    def __init__(self):
        self.rotor = gpiozero.RotaryEncoder(15, 18, wrap=False, max_steps=10)
        self.rotor.steps = motors.getSpeed()
        self.rotaryButton = gpiozero.Button(14)
        self.rotor.when_rotated = self.setMotorsSpeed
        self.rotaryButton.when_released = self.stopMotors

    def setMotorsSpeed(self):
        if self.rotor.steps < 0 and not motors.isBackwardAllowed():
            self.rotor.steps = 0
        else:
            status.setStatus(self.rotor.steps, None)
        sleep(0.05)

    def stopMotors(self):
        status.setStatus(0, None)


illuminatedButton = illuminatedPushButton()
rotary = rotaryEncoder()