import sys
import serial
import glob
import time

def scan():
    """scan for available ports. return a list of tuples (num, name)"""
    if sys.platform == 'linux2':
        return list(glob.glob('/dev/ttyUSB*'))
    else:
        available = []
        for i in range(256):
            try:
                s = serial.Serial("COM" + str(i))
                available.append( s.portstr)
                s.close() # explicit close 'cause of delayed GC in java
            except serial.SerialException:
                pass
        return available

if __name__ == "__main__":
    print "Available ports: "
    s = scan()
    for x, y in enumerate(s):
        print "[%d] %s" % (x, y)

    if len(s) == 0:
        print "No ports available"
        return

    port = s[input("Select port id: ")]

    dev = serial.Serial(port, 115200, timeout=1)
    time.sleep(2)

    print "Name:     ", dev.write('AT+CGMI\r')
    time.sleep(0.5)
    print "Pin:      ", dev.write('AT+CPIN?\r')
    time.sleep(0.5)
    print "Baudrate: ", dev.write('AT+IPR?\r')

    print "Would you like to set name, pin and baudrate? y/n"
    
    if (raw_input() == 'y'):
        pass
