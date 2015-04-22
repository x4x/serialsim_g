#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
timer

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

Name: timer.py
Info:
Thema: serialsim
Date: <2015-02-13 Freitag 14:03>
Version:
"""
from threading import Timer

class timer(object):
    """repedetive timer"""

    def __init__(self, interval, call):
        """
        Atrebutts:
         interval  interval of timer in seconds
         call      event to call (eg.: event.handler)
        """
        self.interval= interval
        self.call= call
        self.thread= Timer(self.interval, self._recall)
        self.thread.daemon= True

    def _recall(self):
        self.call()
        #print self.call
        #print "recall"
        self.thread= Timer(self.interval, self._recall)
        self.thread.daemon= True
        self.thread.start()
        #print self.thread

    def start(self):
        """start timer"""
        self.thread.start()

    def cancel(self):
        self.thread.cancel()


if __name__=="__main__":
    """tests:"""
    def test():
        print("tik")
    a= timer(1,test)
    a.start()
