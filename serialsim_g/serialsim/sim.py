#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Programm for simulating a serial sensor.

(C) 2015 x4x georg.la8585@gmx.at

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

Name: main.py
Info:
Thema: serialsim
Date: <2015-01-28 Mittwoch 15:38>
Version:
"""

import serial
import threading
from event import handler

class sereialsim(object):
    """simulates an serial sensor"""

    def __init__(self, sport, boud, answer, question=None):
        """Initalise Sensor simulator.

        Attributes:
         sport     Serial port number. eg.: '/dev/ttyS0' or on win: COM1 = 0
         boud      Boud eg.: 9600, 19200
         answer    String sent form simulator
         question  Question to wate in polld mode. eg.: '?A' 
         mode      operration mode. eg.: 'c1' continous 1sec
                                         'c2' continous 2sec
                                         'p'  polled (wating for question string)
         call  object to call if event (set to self)

         :var data_in: string with entire serial input data
        """
        self.question = question
        self.answer = answer
        self._data = ""
        self.data_in = ""
        self.handler = handler()

        self.serial = serial.Serial(port=sport, baudrate=boud, bytesize=8, parity='N',
                                  stopbits=1, timeout=None, xonxoff=0, rtscts=0)

    def setBoud(self, boud):
        """reset boudrate

        Attributes:
         boud  boud rate
        """
        if(self.serial.isOpen()):
            self.stop()
        self.serial.boudrate= boud

    def start(self):
        """Start simulator."""
        self.serial.open()

    def stop(self):
        """Stop simulator."""
        self.serial.close()

    def __call__(self):
        if(self.serial.isOpen()):
            self.serial.write(self.answer)
            return True
        return False

    def setpoll(self):
        """"starts a thread and wates for the question string.
        If string is detected the object in call is called."""
        def _event():
            while(self.serial.isOpen()):
                self._data = self.serial.read(len(self.question))
                self._data += self.serial.read(self.serial.inWaiting())
                self.data_in += self._data  # append to entire data string
                if(self._data.find(self.question) >= 0):
                    self.handler()
            
        self.poll = threading.Thread(target=_event)
        self.poll.daemon = True  #allow killing of the thread
        self.poll.start()

    
if __name__=="__main__":
    """tests:"""
    #a= sereialsim('/dev/ttyUSB1', 19200, "\x02"+ "A,042,000.00,M,60," +"\x03"+ "0E" +"\r\n", question="?A")
    a= sereialsim('/dev/ttyUSB1', 19200, "\x02"+ "A,275,000.17,M,60," +"\x03"+ "0E" +"\r\n", question="?A")
    print(a)
    #a.start()
    a()
    print " handler test:"
    def printfun(): print(a._data)
    a.handler.append(printfun) # print input
    a.handler.append(a) # return answer
    a.setpoll() #start polled mode
    #a.stop()
    
