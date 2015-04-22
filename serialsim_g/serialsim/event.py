#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Event handler

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

Name: event.py
Info:
Thema: serialsim
Date: <2015-02-13 Freitag 13:08>
Version:
"""

class handler(list):
    """event hendler"""
    def __call__(self, *args, **kwargs):
        for i in self:
            i(*args, **kwargs)

    def __repr__(self):
        return "Event(%s)" % list.__repr__(self)
