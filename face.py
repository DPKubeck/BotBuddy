import RPi.GPIO as GPIO
import time

LSBFIRST = 1
MSBFIRST = 2
# define the pins connect to 74HC595
dataPinL   = 11      # DS Pin of 74HC595(Pin14)
latchPinL  = 13      # ST_CP Pin of 74HC595(Pin12)
clockPinL = 15       # SH_CP Pin of 74HC595(Pin11)

dataPinR   = 19      # DS Pin of 74HC595(Pin14)
latchPinR  = 21      # ST_CP Pin of 74HC595(Pin12)
clockPinR = 23       # SH_CP Pin of 74HC595(Pin11)

nice = [0x00,0x18,0x24,0x42,0x42,0x42,0x42,0x00]  # data of nice face
aangryR = [0x00,0x0f,0x3f,0x7e,0xfc,0x78,0x30,0x00]
aangryL = [0x00,0xf0,0xfc,0x7e,0x3f,0x1e,0xf3,0x00]
angryR = [0xe, 0x11, 0x21, 0x59, 0x99, 0x81, 0x42, 0x3c]
angryL = [0x70, 0x88, 0x84, 0x9a, 0x99, 0x81, 0x42, 0x3c]
sassyL = [0x00, 0x30, 0x18, 0xe, 0x1c, 0x30, 0x60, 0x00]
sassyR = [0x00, 0xc, 0x18, 0x70, 0x38, 0xc, 0x6, 0x00]
eyeRight = [0x3c, 0x42, 0x81, 0x87, 0x87, 0x81, 0x42, 0x3c]
eyeLeft  = [0x3c, 0x42, 0x81, 0xe1, 0xe1, 0x81, 0x42, 0x3c]
crossEyes = [0x3c, 0x42, 0xa5, 0x99, 0x99, 0xa5, 0x42, 0x3c]
blink1 = [0x3c, 0x42, 0x99, 0x99, 0x99, 0x99, 0x42, 0x3c]
blink2 = [0x3c, 0x42, 0x81, 0x81, 0xbd, 0x81, 0x42, 0x3c]
rollEyes = [[0x3c, 0x42, 0x81, 0x99, 0x99, 0x81, 0x42, 0x3c],
            [0x3c, 0x42, 0x81, 0x81, 0x99, 0x99, 0x42, 0x3c],
            [0x3c, 0x42, 0x81, 0x81, 0x8d, 0x8d, 0x42, 0x3c],
            [0x3c, 0x42, 0x81, 0x8d, 0x8d, 0x81, 0x42, 0x3c],
            [0x3c, 0x42, 0x8d, 0x8d, 0x81, 0x81, 0x42, 0x3c],
            [0x3c, 0x42, 0x99, 0x99, 0x81, 0x81, 0x42, 0x3c],
            [0x3c, 0x42, 0xb1, 0xb1, 0x81, 0x81, 0x42, 0x3c],
            [0x3c, 0x42, 0x81, 0xb1, 0xb1, 0x81, 0x42, 0x3c],
            [0x3c, 0x42, 0x81, 0x81, 0xb1, 0xb1, 0x42, 0x3c],
            [0x3c, 0x42, 0x81, 0x81, 0x99, 0x99, 0x42, 0x3c]]


def setup():
    GPIO.setmode(GPIO.BOARD)    # use PHYSICAL GPIO Numbering
    GPIO.setup(dataPinL, GPIO.OUT)
    GPIO.setup(latchPinL, GPIO.OUT)
    GPIO.setup(clockPinL, GPIO.OUT)
    GPIO.setup(dataPinR, GPIO.OUT)
    GPIO.setup(latchPinR, GPIO.OUT)
    GPIO.setup(clockPinR, GPIO.OUT)



def shiftOut(dPin,cPin,order,val):
    for i in range(0,8):
        GPIO.output(cPin,GPIO.LOW);
        if(order == LSBFIRST):
            GPIO.output(dPin,(0x01&(val>>i)==0x01) and GPIO.HIGH or GPIO.LOW)
        elif(order == MSBFIRST):
            GPIO.output(dPin,(0x80&(val<<i)==0x80) and GPIO.HIGH or GPIO.LOW)
        GPIO.output(cPin,GPIO.HIGH);

# def loop():
#     while True:
#     	for j in range(0,500): # Repeat enough times to display the smiling face a period of time
#             x=0x80
#             for i in range(0,8):
#                 GPIO.output(latchPin,GPIO.LOW)
#                 shiftOut(dataPin,clockPin,pic[i]) #first shift data of line information to first stage 74HC959

#                 shiftOut(dataPin,clockPin,MSBFIRST,~x) #then shift data of column information to second stage 74HC959
#                 GPIO.output(latchPin,GPIO.HIGH) # Output data of two stage 74HC595 at the same time
#                 time.sleep(0.001) # display the next column


def static(eyeL,eyeR):
    while True:
        for j in range(0,100): # Repeat enough times to display the smiling face a period of time
            x=0x80
            for i in range(0,8):
                GPIO.output(latchPinL,GPIO.LOW)
                GPIO.output(latchPinR,GPIO.LOW)
                shiftOut(dataPinL,clockPinL,MSBFIRST,eyeL[i]) #first shift data of line information to first stage 74HC959
                shiftOut(dataPinR,clockPinR,MSBFIRST,eyeR[i])

                shiftOut(dataPinL,clockPinL,MSBFIRST,~x) #then shift data of column information to second stage 74HC959
                shiftOut(dataPinR,clockPinR,MSBFIRST,~x)
                GPIO.output(latchPinL,GPIO.HIGH) # Output data of two stage 74HC595 at the same time
                GPIO.output(latchPinR,GPIO.HIGH)
                time.sleep(0.001) # display the next column
                x>>=1

def rowEyes():  # rolling the eyes once which last one second.
    
    for k in range(0,10):
        for j in range(0,10): # Repeat enough times to display the smiling face a period of time
            x=0x80
            for i in range(0,8):
                GPIO.output(latchPinL,GPIO.LOW)
                GPIO.output(latchPinR,GPIO.LOW)
                shiftOut(dataPinL,clockPinL,MSBFIRST,rollEyes1[k][i]) #first shift data of line information to first stage 74HC959
                shiftOut(dataPinR,clockPinR,MSBFIRST,rollEyes1[k][i])

                shiftOut(dataPinL,clockPinL,MSBFIRST,~x) #then shift data of column information to second stage 74HC959
                shiftOut(dataPinR,clockPinR,MSBFIRST,~x)
                GPIO.output(latchPinL,GPIO.HIGH) # Output data of two stage 74HC595 at the same time
                GPIO.output(latchPinR,GPIO.HIGH)
                time.sleep(0.001) # display the next column
                x>>=1


def lookAside(t,direction): # t is the seconds for how long you would like the eye to look left or right
    #direction takes : eyeRight or eyeLeft
    for j in range(0,100): # Repeat enough times to display the smiling face a period of time
            x=0x80
            for i in range(0,8):
                GPIO.output(latchPinL,GPIO.LOW)
                GPIO.output(latchPinR,GPIO.LOW)
                shiftOut(dataPinL,clockPinL,MSBFIRST,blink1[i]) #first shift data of line information to first stage 74HC959
                shiftOut(dataPinR,clockPinR,MSBFIRST,blink1[i])

                shiftOut(dataPinL,clockPinL,MSBFIRST,~x) #then shift data of column information to second stage 74HC959
                shiftOut(dataPinR,clockPinR,MSBFIRST,~x)
                GPIO.output(latchPinL,GPIO.HIGH) # Output data of two stage 74HC595 at the same time
                GPIO.output(latchPinR,GPIO.HIGH)
                time.sleep(0.001) # display the next column
                x>>=1
    for j in range(0,t*100): # Repeat enough times to display the smiling face a period of time
            x=0x80
            for i in range(0,8):
                GPIO.output(latchPinL,GPIO.LOW)
                GPIO.output(latchPinR,GPIO.LOW)
                shiftOut(dataPinL,clockPinL,MSBFIRST,direction[i]) #first shift data of line information to first stage 74HC959
                shiftOut(dataPinR,clockPinR,MSBFIRST,direction[i])

                shiftOut(dataPinL,clockPinL,MSBFIRST,~x) #then shift data of column information to second stage 74HC959
                shiftOut(dataPinR,clockPinR,MSBFIRST,~x)
                GPIO.output(latchPinL,GPIO.HIGH) # Output data of two stage 74HC595 at the same time
                GPIO.output(latchPinR,GPIO.HIGH)
                time.sleep(0.001) # display the next column
                x>>=1

def loop(eyeL,eyeR):
    while True:
        for j in range(0,100): # Repeat enough times to display the smiling face a period of time
            x=0x80
            for i in range(0,8):
                GPIO.output(latchPinL,GPIO.LOW)
                GPIO.output(latchPinR,GPIO.LOW)
                shiftOut(dataPinL,clockPinL,MSBFIRST,eyeL[i]) #first shift data of line information to first stage 74HC959
                shiftOut(dataPinR,clockPinR,MSBFIRST,eyeR[i])

                shiftOut(dataPinL,clockPinL,MSBFIRST,~x) #then shift data of column information to second stage 74HC959
                shiftOut(dataPinR,clockPinR,MSBFIRST,~x)
                GPIO.output(latchPinL,GPIO.HIGH) # Output data of two stage 74HC595 at the same time
                GPIO.output(latchPinR,GPIO.HIGH)
                time.sleep(0.001) # display the next column
                x>>=1
        for k in range(0,100): # Repeat enough times to display the smiling face a period of time
            x=0x80
            for i in range(0,8):
                GPIO.output(latchPinL,GPIO.LOW)
                GPIO.output(latchPinR,GPIO.LOW)
                shiftOut(dataPinL,clockPinL,MSBFIRST,nice[i]) #first shift data of line information to first stage 74HC959
                shiftOut(dataPinR,clockPinR,MSBFIRST,nice[i])

                shiftOut(dataPinL,clockPinL,MSBFIRST,~x) #then shift data of column information to second stage 74HC959
                shiftOut(dataPinR,clockPinR,MSBFIRST,~x)
                GPIO.output(latchPinL,GPIO.HIGH) # Output data of two stage 74HC595 at the same time
                GPIO.output(latchPinR,GPIO.HIGH)
                time.sleep(0.001) # display the next column
                x>>=1

def destroy():  
    GPIO.cleanup()
if __name__ == '__main__':  # Program entrance
    print ('Program is starting...' )
    setup() 
    try:
        loop(angryL,angryR)  
    except KeyboardInterrupt:   # Press ctrl-c to end the program.
        destroy()  
