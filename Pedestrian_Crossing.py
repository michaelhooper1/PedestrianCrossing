import time, random
import RPi.GPIO as io

LEDcontrol = [23,24,25,4,17,9]
#GPIO for Traffic Red, amber, Green and noCross corss sounder

crossRequest = 7
trafficSensor = 18
nextSequenceTime = time.time()

def main():
    global lastTraffic, state, bleep
    print("Pedestrian crossing simulator Ctrl C to quit")
    initGPIO()
    io.output(green,1) #Green light on to start
    state = 0
    bleepTime = time.time()
    bleep = False
    lastTraffic = time.time()
    while 1:
        checkTraffic()
        if checkRequest() and state == 0:
            io.output(noCross, 1) #turn on the no cross light
            if time.time() - lastTraffic > 10.0: #Cross now
                state = 1
            else:
                time.sleep(10.0) #let traffic flow for a bit
                state = 1
        crossSequenceFunction()
        if bleep and time.time() > bleepTime:
            bleepTime = time.time() + 0.3
            io.output(sounder, not(io.input(sounder)))

def checkTraffic():
    global lastTraffic
    if io.input(trafficSensor) == 0:
        lastTraffic = time.time()

def checkRequest():
    request = False
    if io.input(crossRequest) == 0:
        request = True
    return request

def crossSequenceFunction():
    global nextSequenceTime, countFlash, state, bleep
    if state == 0:
        nextSequenceTime = time.time() + 2.0
        return
    if time.time() > nextSequenceTime:
        if state == 1: #show amber light
            #print("doing state", state)
            io.output(green, 0)
            io.output(amber, 1)
            state = 2
            nextSequenceTime = time.time() + 2.0 #show amber time
        elif state == 2: #show red
            #print("doing state", state)
            io.output(amber, 0)
            io.output(red,1)
            state = 3
            nextSequenceTime = time.time() + 2.0 # show red time
        elif state == 3: #show cross light
            #print("doing state",state)
            io.output(noCross,0 )
            io.output(cross,1)
            bleep = True
            state = 4
            nextSequenceTime = time.time() + 5.0 #crossing time
        elif state == 4: #change to amber clear crossing
            #print("doing state", state)
            io.output(amber,1)
            io.output(red, 0)
            bleep = False
            io.output(sounder,0) # turn off sounder
            state = 5
            nextSequenceTime = time.time() + 1.0
        elif state == 5: #flash amber and cross
            #print("doing state", state)
            io.output(amber, not(io.input(amber)))
            io.output(cross, not(io.input(cross)))
            nextSequenceTime = time.time() + 0.2 #flashing speed
            countFlash +=1
            if countFlash > 20: #clear crossing time 20 * flash speed
                countFlash = 0
                state = 6
        elif state == 6: # hold amber
            io.output(cross,0)
            io.output(noCross,1)
            io.output(amber,1)
            state = 7
            nextSequenceTime = time.time() + 2.0 #hold amber time
        elif state == 7: #put on red light
            # print("doing state", state)
            io.output(amber,0)
            io.output(green,1)
            io.output(noCross,0)
            state = 0
            nextSequenceTime = time.time() + 1.0

def initGPIO():
    global red, amber, green, noCross, cross, countFlash, sounder
    io.setmode(io.BCM)
    io.setwarnings(False)
    for pin in range(0, len(LEDcontrol)):
        io.setup(LEDcontrol[pin], io.OUT) #make pin into an output
        io.output(LEDcontrol[pin], 0) #set to zero
    io.setup(crossRequest,io.IN, pull_up_down= io.PUD_UP) # make pin into an input
    red = LEDcontrol[0]
    amber = LEDcontrol[1]
    green = LEDcontrol[2]
    noCross = LEDcontrol[3]
    cross = LEDcontrol[4]
    sounder = LEDcontrol[5]
    countFlash = 0

#main program logic:
if __name__ == "__main__":
    main()