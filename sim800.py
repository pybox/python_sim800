#!/usr/bin/python

import serial
import re
import time
class sim(object):
    def __init__(self, port, baudrate=9600, timeout=2):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.sim_serial = serial.Serial(port, baudrate=self.baudrate, timeout=self.timeout)

        #Serial commands
        self.at = b'AT+IPR=9600\n'
        self.s_q = b'AT+CSQ\n'
        self.c_t_m = b'AT+CMGF=1\n'
        self.ctrl_z = b'\x1A'
    def response_handler(self, c):
        try :
            r = ''
            i = 0
            while(i < c):
                r += self.sim_serial.readline().decode()
                i+=1
            return re.findall(r"\r\n(.*)\r\n", r)
        except Exception as e :
            print(e)
            return False

    def isOpen(self):
        self.sim_serial.flushInput()
        self.sim_serial.write(self.at)
        if self.response_handler(2)[0] == "OK" :
            return True
        else :
            return False

    def signal_quality(self):
        self.sim_serial.flushInput()
        self.sim_serial.write(self.s_q)
        r = self.response_handler(4)[0][5:].split(',')[0]
        if r :
            return ("%.2f" % (( int(r)/31 ) * 100))
        else :
            return False
    def send_sms(self, number, text):
        try :
#            import pdb ; pdb.set_trace()
            self.sim_serial.write(self.c_t_m)
            time.sleep(0.1)
            self.sim_serial.write( ('AT+CMGS="%s"\n' % (number)).encode('ascii'))
            time.sleep(0.1)
            self.sim_serial.write(text.encode('ascii'))
            time.sleep(0.1)
            self.sim_serial.flushInput()
            self.sim_serial.write(self.ctrl_z)
            time.sleep(1)
            r = self.response_handler(4)
            if r[-1] == 'OK' :
                return r
            else :
                return False
        except Exception as e :
            print(e)
            return False
    def call(self, number, w):
        data = 'ATD+ '+number+';\n'
        self.sim_serial.flushInput()
        self.sim_serial.write( data.encode('ascii') )
        time.sleep(w)
        self.sim_serial.write(b'ATH\n')
        return True
