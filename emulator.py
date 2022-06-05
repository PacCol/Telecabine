# A class to emulate the Raspberry Pi GPIO module

emulator = True

class GPIO:

    BCM = None
    BOARD = None

    OUT = None
    
    def __init__(self):
        pass
    def setwarnings(something):
        pass
    def setmode(something):
        pass
    def setup(something, something1):
        pass
    class PWM:
        def __init__(self, something, something1):
            pass
        def start(self, something):
            pass
    def output(something, something1):
        pass


class gpiozero:

    def __init__(self):
        pass

    def CPUTemperature():
        class cpu:
            temperature = "45"
            def __init__(self):
                pass
        return cpu()

    class RGBLED:
        def __init__(self, something, something1, something2):
            pass

    class PWMLED:
        def __init__(self, something):
            pass
        def pulse(self):
            pass
        def on(self):
            pass
        def off(self):
            pass

    class Button:
        def __init__(self, something):
            pass

    class RotaryEncoder:
        def __init__(self, something, something1, wrap, max_steps):
            pass


class i2c:

    def __init__(self, port, address):
        pass


class sh1106:

    width = 128
    height = 64

    def __init__(self, serial, rotate, width, height):
        pass

    def contrast(self, something):
        pass

    def show(self):
        pass

    def hide(self):
        pass


class canvas(object):

    def __init__(self, something):
        pass

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        pass