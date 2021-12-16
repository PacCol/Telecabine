import tm1637

from time import sleep

tm = tm1637.TM1637(clk=27, dio=17)

def show():
    tm.write([127, 255, 127, 127]) # all LEDS on "88:88"
    sleep(1)
    tm.write([0, 0, 0, 0]) # all LEDS off
    sleep(1)
    tm.write([63, 6, 91, 79]) # show "0123"
    sleep(1)
    tm.write([0b00111001, 0b00111111, 0b00111111, 0b00111000]) # "COOL"
    sleep(1)
    tm.show('help') # show "HELP"
    sleep(1)
    tm.hex(0xdead) # display "dEAd"
    sleep(1)
    tm.hex(0xbeef) # display "bEEF"
    sleep(1)
    tm.numbers(11, 55) # show "11:55"
    sleep(1)
    tm.number(-955) # show "-955"

show()