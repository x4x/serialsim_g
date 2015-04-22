#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
enhanced assotative event handler

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

Name: events2.py
Info:
Thema: serialsim
Date:
Version:
"""

class Handler(list):
    """minamal event hendler baste on a list

    Usage:
        def b(x):
            print(x*2)
        a= handler()
        a.append(b)
        # call:
        a(3)
    """

    def __call__(self, *args, **kwargs):
        for i in self:
            i(*args, **kwargs)

    def __repr__(self):
        return "Event(%s)" % list.__repr__(self)


class AssoziativHandler(dict):
    """Advanced assotative eventhandler
    Usage:
        a = AssoziativHandler()
        a.add_event("test1")
        a("test1") # call
        print(a) # debug

        def c(num):
            print("test num*2= " + str(num*2))

        a.add_calleble("test1", c)
        a("test1", 2) # call (slow)
        a.calleble("test1")(2) # call (fast)

        # kivy ex.:
        ....
        b_a = Button(text='A')
        self.add_widget(b_a)
        b_start.bind(on_press=handler.calleble("b_a"))
        ...
    """

    def add_event(self, name):
        """add events to the handler.
        Arguments:
        name  text for event
        """
        if not name in self:
            self[name] = Handler()

    def bind(self, name, calleble):
        """add calleble object to the handler.
        Arguments:
        name  name of event to hook the caleble
        calleble   calleble object
        """
        if name in self:
            self[name].append(calleble)
        else:
            self[name] = Handler([calleble])

    def calleble(self, name):
        """returns a pointer for a callback.
        Arguments:
        name  pointer to event"""
        if not name in self:
            self[name] = Handler()
        return self[name]

    def __call__(self, name, *args, **kwargs):
        """manuel call of event
        Arguments:
        name   name of event"""
        if name in self:
            self[name](*args, **kwargs)

    def __repr__(self):
        ret = ""
        for i in self:
            ret += "{0} Handels {1}\r\n".format( i, self[i] )
        return ret


if __name__ == "__main__":
    """Test:"""
    a = AssoziativHandler()
    a.add_event("test1")
    a("test1") # call
    print(a)

    def c(num):
        print("test num*2= " + str(num*2))

    a.bind("test1", c)
    a("test1", 2)

    def c2(num):
        print("test num*3= " + str(num*4))

    a.bind("test2", c2)
    a.bind("test1", c2)

    print(a)

    a("test1", 2)
    a("test2", 5)