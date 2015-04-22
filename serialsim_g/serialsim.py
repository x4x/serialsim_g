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

Name: serialsim.py
Info:
Thema: serialsim
Date: <2015-04-09 Donnerstag 09:06>
Version:
"""

from cmd2 import Cmd #, make_option, options
from serialsim.sensor import sensor
from docopt import docopt
import sys

__doc__="""Programm for simulating serail sensors.

Usage:
 main.py [ -b <boude> | --boud <boude> ][ -c <com> | --com <com> ][ -m <mode> | --mode <mode> ][ -i <interval> | --interval <interval> ][ --answer <answer> ][ --question <question> ]
 main.py shell <commands>

Options:
 -h --help      Show this screen.
 -b --boud=boud      set boudrate [default: 9600].
 -c --com=com       set serail interface[default: /dev/pts/14].
 -m --mode=mode      selecte mode (eg.: <poll|cont>) [default: poll].
 -i --interval=interval  interfale for continouse mode in sec [default: 1].
 --answer=answer       answer of the sensor [default: Q, a,b,c].
 --question=question     question string for polled mode [default: ?A].
"""

class App(Cmd):
    """Comandline app for serial simulator"""
    """
    @options([make_option('-b', '--boud', type="int", help=""),
              make_option('-c', '--com', type="str", help=""),
              make_option('-m', '--mode', type="str", help=""),
              make_option('-i', '--interval', type="int", help=""),
              make_option('--answer', type="str", help=""),
              make_option('--question', type="str", help=""),
              ])
    """
    def __init__(self):
        #super(App, self).__init__()
        Cmd.__init__(self) # old overlode! super not working.
        if 'arguments'in vars():
            self.mode=     arguments['--mode']
            self.boud=     int(arguments['--boud'])
            self.com=      arguments['--com']
            self.interval= int(arguments['--interval'])
            self.answer=   arguments['--answer']
            self.question= arguments['--question']
        else:
            self.mode=     "poll"
            self.boud=     9600
            self.com=      "/dev/ttyUSB0"
            self.interval= 1
            self.answer=   "\x02A,275,000.17,M,60,\x030E\r\n"
            self.question= "?A"
        self.sensor=None
        self.do_init()

    def do_init(self, opts=None):
        if(self.sensor==None):
            self.sensor= sensor(   mode=     self.mode,
                                   boud=     self.boud,
                                   com=      self.com,
                                   interval= self.interval,
                                   answer=   self.answer,
                                   question= self.question)
        else:
            print("alredy initaliesed!")
        
    def do_start(self, opts=None):
        """start the simulation"""
        self.sensor._config()
        self.sensor.start()
        
    def do_stop(self, opts=None):
        """stop the simulation"""
        self.sensor.stop()

    def do_terminate(self, opts=None):
        """Terminate internal simulator"""
        self.sensor._terminate()
        
    def do_setanswerhex(self, arg, opts=None):
        """set the answer in hex.
        Usage:
         setanswerhex 7061756c -> 'paul'"""
        if(self.sensor.isRuning): self.do_terminate()
        s= ''.join(arg)
        self.sensor.answer= s.decode('hex')        

    def do_setboud(self, arg, opts=None):
        """set the boudrate of the serial interface (e.g.: 9600, 19200)"""
        if(self.sensor.isRuning): self.do_terminate()
        self.sensor.boud= int(''.join(arg))
        
    def do_setinterval(self, arg, opts=None):
        """set the interfal for continous mode"""
        if(self.sensor.isRuning): self.do_terminate()
        self.sensor.interval= int(''.join(arg))
    
    def do_setmode(self, arg, opts=None):
        """set the mode of operratione and stop"""
        if(self.sensor.isRuning): self.do_terminate()
        mode= str(''.join(arg))
        if(mode=="poll"):
            self.sensor.mode= mode
        elif(mode=="cont"):
            self.sensor.mode= mode
        else: print("either 'poll' or 'cont'")
            
    def do_getmode(self, arg, opts=None):
        """get the mode of operatione"""
        print(self.sensor.mode)

    def do_getboud(self, arg, opts=None):
        """get the boudrade"""
        print(self.sensor.boud)

    def do_setcom(self, arg, opts=None):
        """set teh serial interface"""
        if(self.sensor.isRuning): self.do_terminate()
        self.sensor.com= ''.join(arg)

    def do_getcom(self, arg, opts=None):
        print(self.sensor.com)

    """
    def postloop(self):
        print "jes"
    """               
    
if __name__ == "__main__":
    arguments = docopt(__doc__, version='Calculator with docopt') # read in parameters
    # del arguments, becouse arguments are alos interpreted by cmd2.
    if(arguments['shell']):
        sys.argv= arguments['commands']
    else:
        del sys.argv[1:]
    
    appm= App()
    appm.cmdloop()
    
