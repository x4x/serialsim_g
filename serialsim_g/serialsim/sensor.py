#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Programm for simulating serail sensors.

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

Name: sensor.py
Info:
Thema: serialsim
Date: <2015-02-24 Dienstag 00:31>
Version:
"""

from event import handler
from timer import timer
from sim import sereialsim

class sensor(object):
    """simulates an serial sensor"""
    def __init__(self,
                 mode=     "poll",
                 boud=     9600,
                 com=      "/dev/ttyUSB0",
                 interval= 1,
                 answer=   "\x02A,275,000.17,M,60,\x030E\r\n",
                 question= "?A"):
        self.mode =     mode
        self.boud =     boud
        self.com =      com
        self.interval = interval
        self.answer =   answer
        self.question = question
        self.isRuning = False

        self.sim = sereialsim(sport=None, boud=self.boud, answer=self.answer, question=self.question)
        self.data_in_ptr = 0
        #self._config()
    
    def _config(self):
        """configure the mode"""
        self.handler = handler()  # create event handler
        self.sim = sereialsim(sport=self.com, boud=self.boud, answer=self.answer, question=self.question)
        self.handler.append(self.sim) # hook output to eventhandler
        self.isRuning = False

    def _terminate(self):
        """Terminate internels."""
        if(self.isRuning): self.stop()
        #del self.handler
        self.sim = sereialsim(sport=None, boud=self.boud, answer=self.answer, question=self.question)
        del self.sim
        self.data_in_ptr = 0
        self.isRuning= False
        
    def start(self):
        """start the simulation"""
        if(not self.isRuning):
            if(self.mode == "cont"): # continous
                self.timer= timer(self.interval, self.handler )
                self.timer.start()
            elif(self.mode=="poll"): # polled
                self.sim.handler.append(self.handler)
                self.sim.setpoll()
            self.isRuning= True
        
    def stop(self):
        """stop(hold) the simulation"""
        if(self.isRuning):
            if(self.mode == "cont"): # continous
                self.timer.cancel()
            elif(self.mode=="poll"): # polled
                self.sim.handler.remove(self.handler)
            self.isRuning= False

    def get_in(self):
        """get the serial input.
        :return entire input."""
        r = self.sim.data_in[self.data_in_ptr:]
        self.data_in_ptr = len(self.sim.data_in)
        return r

    def bind(self, on_question):
        """call if question is sent."""
        self.handler.append(on_question)
    
def main():
    """test cases:"""
    """
    # continous:
    print("starting ...")
    a= sensor(   mode=     "cont",
                 boud=     9600,
                 com=      "/dev/ttyUSB1",
                 interval= 1,
                 answer=   "\x02A,275,000.17,M,60,\x030E\r\n",
                 question= "?A")
    print("config")
    a._config()
    print("started")
    a.start()
    while(True):
        pass
    """
    # polled:
    print("starting ...")
    a= sensor(   mode=     "poll",
                 boud=     9600,
                 com=      "/dev/ttyUSB1",
                 interval= 1,
                 answer=   "\x02A,275,000.17,M,60,\x030E\r\n",
                 question= "?A")
    print("config")
    a._config()
    print("started")
    a.start()
    while(True):
        pass
    
if __name__ == "__main__":
    main()
