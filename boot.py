from adafruit_ht16k33.segments import Seg7x4
import time
import digitalio
import board
import time
import busio

#usb detection
usb = digitalio.DigitalInOut(board.GP24)
usb.switch_to_input(pull=digitalio.Pull.DOWN)


# PICO LED
led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT


#input pins
pinB = digitalio.DigitalInOut(board.GP22)
pinB.switch_to_input(pull=digitalio.Pull.DOWN)
pinGW = digitalio.DigitalInOut(board.GP21)
pinGW.switch_to_input(pull=digitalio.Pull.DOWN)
pinOW = digitalio.DigitalInOut(board.GP20)
pinOW.switch_to_input(pull=digitalio.Pull.DOWN)
pinO = digitalio.DigitalInOut(board.GP19)
pinO.switch_to_input(pull=digitalio.Pull.DOWN)
reset = digitalio.DigitalInOut(board.GP18)
reset.switch_to_input(pull=digitalio.Pull.DOWN)
pinG = digitalio.DigitalInOut(board.GP17)
pinG.switch_to_input(pull=digitalio.Pull.DOWN)


# Clear and update display
def UpdateF(val):
    display.fill(0)
    display.print(val)
    
    
    
#if True:            #if powered by usb
if not usb.value:   #if powered by pins and usb not used
    try:
    # i2c = busio.I2C(board.SCL1, board.SDA1)  # QT Py RP2040 STEMMA connector
        i2c = busio.I2C(board.GP27, board.GP26)    # Pi Pico RP2040
        display = Seg7x4(i2c)
        display.brightness = 0.1
        display.blink_rate = 0

    #turn on led for 3 seconds to show pico turns on
        led.value = True
        time.sleep(3)
        led.value = False

        val=0
        UpdateF(val)

        while True:
        #    display.set_digit_raw(0, 0b01000000)
            if (pinB.value):
                #blinks led and raise counter by one
                val=val+1
                led.value = True
                time.sleep(.1)
                while (pinB.value):
                    print("on")
                led.value = False
                UpdateF(val)
            elif reset.value or pinGW.value:
                #resets counter
                val=0
                UpdateF(val)
            elif pinG.value:
                #Prints heat
                display.fill(0)
                display.set_digit_raw(0,0b01110110)
                display.set_digit_raw(1,0b01111001)
                display.set_digit_raw(2,0b01110111)
                display.set_digit_raw(3,0b00110001)
                
                time.sleep(.1)
            elif pinO.value:
                #Prints done
                display.fill(0)
                display.set_digit_raw(0,0b01011110)
                display.set_digit_raw(1,0b01011100)
                display.set_digit_raw(2,0b01010100)
                display.set_digit_raw(3,0b01111001)
                
                time.sleep(.1)
                
            time.sleep(.1)
        
    except KeyboardInterrupt:
        display.fill(0)
        display.set_digit_raw(0,0b01111001)
        display.set_digit_raw(1,0b01000000)
        display.set_digit_raw(2,0b00111001)
        display.set_digit_raw(3,0b00000110)
    except:
        while not reset.value:
            led.value = True
            time.sleep(.1)
            led.value = False
            time.sleep(.1)
else:
    
    led.value = True
    time.sleep(.5)
    led.value = False
    time.sleep(.5)
    led.value = True
    time.sleep(.5)
    led.value = False
    print('usb')



