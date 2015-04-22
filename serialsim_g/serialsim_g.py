#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Grafical frontend for serialsim a serail sensors simulator.

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

Name: serialsim_g.py
Info:
Thema: serialsim
Date: <2015-04-09 Donnerstag 11:57>
Version:
"""
from __future__ import print_function

appname= "serialsim_g 0.0.1alfa"

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton

from serialsim import sensor as seri
from events2 import AssoziativHandler


class SerialConfig(GridLayout):
    """Panel with sensor config options."""

    def __init__(self, **kwargs):
        super(SerialConfig, self).__init__(**kwargs)
        self.cols = 2

        self.add_widget(Label(text='Com', size_hint_x=0.5))
        self.com = TextInput(multiline=False, text='/dev/ttyUSB0')
        self.com.bind(text=handler.calleble("f_com"))
        self.add_widget(self.com)

        self.add_widget(Label(text='Boud', size_hint_x=0.5))
        self.boud = TextInput(multiline=False, text='9600')
        self.boud.bind(text= handler.calleble("f_boud"))
        self.add_widget(self.boud)

        self.add_widget(Label(text='Cont. Intervall', size_hint_x=0.5))
        self.intervall = TextInput(multiline=False, text='1')
        self.intervall.bind(text= handler.calleble("f_intervall"))
        self.add_widget(self.intervall)

        self.add_widget(Label(text='Answer', size_hint_x=0.5))
        self.answer = TextInput(multiline=False, text=r'\x02A,275,000.17,M,60,\x030E\r\n')
        self.answer.bind(text= handler.calleble("f_Answer"))
        self.add_widget(self.answer)

        self.add_widget(Label(text='Question', size_hint_x=0.5))
        self.question = TextInput(multiline=False, text='?A')
        self.question.bind(text= handler.calleble("f_Question"))
        self.add_widget(self.question)

        self.add_widget(Label(text='Mode', size_hint_x=0.5))
        self.mode = Button(text='poll', background_normal='', background_color=[1, 0.5, 0, 1])
        self.mode.bind(on_press= handler.calleble("f_mode"))
        self.add_widget(self.mode)
        def toggle_mode_button(opt=None):
            if self.mode.text == "poll":
                self.mode.text= "cont"
                self.mode.background_color= [1, 0, 0.5, 1]
            else:
                self.mode.text= "poll"
                self.mode.background_color= [1, 0.5, 0, 1]
        handler.bind("f_mode", toggle_mode_button)


class ControlPanel(GridLayout):
    """Panel with main controls. eg.: start/stop, set config"""

    def __init__(self, **kwargs):
        super(ControlPanel, self).__init__(**kwargs)
        self.cols = 3
        self.rows = 1
        b_startstop = ToggleButton(text='Start/Stop', stat="normal",
                                   size_hint_x=1,
                                   background_normal='', background_color=[0.8, 0, 0, 1],
                                   background_down='')
        b_config = Button(text='Config', size_hint_x=0.5)
        self.add_widget(b_startstop)
        self.add_widget(b_config)
        b_config.bind(on_press=handler.calleble("b_conf"))
        # logic for toggelButton events:
        b_startstop.bind(
            state=lambda i, s: handler.calleble("b_stop")() if s == "normal" else handler.calleble("b_start")())
        # set b_startstop Button color acording to status:
        def startstop_off(*args):
            b_startstop.background_color = [0.8, 0, 0, 1]
        handler.bind("b_stop", startstop_off)
        def startstop_on(*args):
            b_startstop.background_color = [0, 0.8, 0, 1]
        handler.bind("b_start", startstop_on)

        # set indicators of config Button:
        def config_not_set(*args , **kwargs):
            """set the config button to jello, to indicate config not set."""
            b_config.background_normal = ''
            b_config.background_color = [1, 0.8, 0, 1]
        handler.bind("l_config", config_not_set)
        def reset_config_button(*args, **kwargs):
            """set the config button to defoult agen."""
            b_config.background_normal = 'atlas://data/images/defaulttheme/button'
            b_config.background_color = [1, 1, 1, 1]
        handler.bind("b_conf", reset_config_button)


class MyApp(App):

    def build(self):
        # controll pennel:
        controlslayout = GridLayout(cols=1, rows=2)
        controlslayout.add_widget(SerialConfig())
        controlslayout.add_widget(ControlPanel())
        # data pennel:

        # master layout:
        layout = GridLayout(cols=2, rows=1)
        layout.add_widget(Label(text='serial output'))
        layout.add_widget(controlslayout)

        # function bindings for Buttons and Felds:
        handler.bind("b_start", io.s_stat)
        handler.bind("b_stop", io.s_stop)
        handler.bind("b_conf", io.s_conf)
        # config Felds:
        handler.bind("f_com", io.s_com)
        handler.bind("f_boud", io.s_boud)
        handler.bind("f_intervall", io.s_intervall)
        handler.bind("f_Answer", io.s_answer)
        handler.bind("f_Question", io.s_question)
        handler.bind("f_mode", io.s_mode)
        # call wen something in SerialConfig changes:
        handler.bind("f_com", handler.calleble("l_config"))
        handler.bind("f_boud", handler.calleble("l_config"))
        handler.bind("f_intervall", handler.calleble("l_config"))
        handler.bind("f_Answer", handler.calleble("l_config"))
        handler.bind("f_Question", handler.calleble("l_config"))
        handler.bind("f_mode", handler.calleble("l_config"))

        return layout

    def on_stop(self):
        """exiting app"""
        io.s_stop()

    def get_application_name(self):
        """name of the app"""
        return appname


class extern(object):
    """interfaces to the non GUI stuff."""
    def __init__(self):
        self.sensor = seri.sensor(com=None)
        self.toconfig = seri.sensor(com=None)


    def s_stat(self, opt=None):
        if not self.sensor.isRuning:
            print("Start Button")
            self.sensor._config()
            self.sensor.start()

    def s_stop(self, opt=None):
        if self.sensor.isRuning:
            print("Stop Button")
            self.sensor.stop()
            self.sensor._terminate()

    def s_conf(self, opt=None):
        """take config from toconfig and initialise it."""
        if not self.sensor.isRuning:
            print("Config Button")
            self.sensor = self.toconfig

    def s_com(self, opt=None, val=None):
        """set com in toconfig."""
        self.toconfig.com = val

    def s_boud(self, opt=None, val=None):
        """set boud in toconfig."""
        self.toconfig.boud = int(val)

    def s_intervall(self, opt=None, val=None):
        """set intervall in toconfig."""
        self.toconfig.interval = int(val)

    def s_answer(self, opt=None, val=None):
        """set answer in toconfig."""
        self.toconfig.answer = val

    def s_question(self, opt=None, val=None):
        """set question in toconfig."""
        self.toconfig.question = val

    def s_mode(self, opt=None):
        """toggel mode in toconfig."""
        if self.toconfig.mode == "poll":
            self.toconfig.mode = "cont"
        else:
            self.toconfig.mode = "poll"

handler = AssoziativHandler()
io = extern()
if __name__ == '__main__':
    MyApp().run()
