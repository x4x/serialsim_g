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
import sys

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.event import EventDispatcher
from kivy.clock import Clock

from datetime import datetime
import xmltodict

from serialsim import sensor as seri
from events2 import AssoziativHandler
from serial import SerialException


appname = "serialsim_g 0.0.2beta"
loghader = """Log file: {0}\n""".format(str(datetime.now()))

class LogWindow(GridLayout):
    """event and serial log"""

    def __init__(self, *args, **kwargs):
        """ """
        super(LogWindow, self).__init__(*args, **kwargs)
        self.cols = 1

        log = TextInput(text= loghader,
                        markup=True,
                        multiline=True, halign="left", valign="top",
                        size_hint_y=1)
        self.b_clear = Button(text="Log clear", size_hint_y=0.1)
        def clear_log(*args):
            log.text = loghader
        self.b_clear.bind(on_press=clear_log)
        self.add_widget(self.b_clear)
        self.add_widget(log)
        self.b_export = Button(text="Export Log", size_hint_y=0.2)
        self.b_export.textout = log.text
        self.add_widget(self.b_export)
        self.b_export.bind(on_press=handler.calleble("b_w-log"))

        # put serial input in log.text:
        def append_text(*args):
            try: log.text += io.get_data_in()
            except: pass
        clock = Clock.schedule_interval(append_text, 1)

        # TODO: make serial in and output append to log.text with different markup colors according to source.

class StringPreMadeText(GridLayout):
    """insert a pre made sensor sting from list"""

    def __init__(self, insert=Label(), *args, **kwargs):
        """
        :param insert: string in witch chosen char gets appended
        """
        super(StringPreMadeText, self).__init__(*args, **kwargs)
        self.cols = 2
        self.insert = insert

        def insert(instance):
            """append chosen char to string in Label."""
            self.insert.text = instance.text
            handler.calleble("l_helpDismiss")()

        self.sensor_strs = []
        for each in xml["conf"]["sensor"]:
            self.add_widget(Label(text=each["name"], size_hint_x=0.3))
            #self.add_widget(Label(text="Wind Sonic", size_hint_x=0.3))
            #self.windsonic = Button(text=r"\x02A,275,040.17,M,60,\x030E\r\n").bind(on_press=insert)
            #self.windsonic.bind(on_press=insert)
            #self.add_widget(self.windsonic)
            self.sensor_strs.append(Button(text=each["str"]))
            self.sensor_strs[-1].bind(on_press=insert)
            self.add_widget(self.sensor_strs[-1])

        self.freestring = TextInput(multiline=False, text='')
        self.setclose = Button(text='Close')
        self.setclose.bind(on_press=lambda i=None: handler.calleble("l_helpDismiss")())
        self.freestring.bind(on_text_validate=insert)
        self.add_widget(self.setclose)
        self.add_widget(self.freestring)


class StringTextInsertHelp(GridLayout):
    """Contant for the string special chars help."""

    def __init__(self, insert=Label(), *args, **kwargs):
        """
        :param insert: string in witch chosen char gets appended
        """
        super(StringTextInsertHelp, self).__init__(*args, **kwargs)
        self.cols = 2
        self.insert = insert

        def insert_append(instance):
            """append chosen char to string in Label."""
            self.insert.text += instance.text
            handler.calleble("l_helpDismiss")()

        self.add_widget(Label(text=r"Backslash (\)", size_hint_x=1.6))
        self.backslash = Button(text=r"\\")
        self.backslash.bind(on_press=insert_append)
        self.add_widget(self.backslash)

        self.add_widget(Label(text=r"Single quote (')", size_hint_x=1))
        self.singlequoute = Button(text=r"\'")
        self.singlequoute.bind(on_press=insert_append)
        self.add_widget(self.singlequoute)

        self.add_widget(Label(text="Double quote (\")", size_hint_x=1))
        self.dublequoute = Button(text=r"\'")
        self.dublequoute.bind(on_press=insert_append)
        self.add_widget(self.dublequoute)

        self.add_widget(Label(text="ASCII Bell (BEL)", size_hint_x=1))
        self.bell = Button(text=r"\a")
        self.bell.bind(on_press=insert_append)
        self.add_widget(self.bell)

        self.add_widget(Label(text="ASCII Backspace (BS)", size_hint_x=1))
        self.backspace = Button(text=r"\b")
        self.backspace.bind(on_press=insert_append)
        self.add_widget(self.backspace)

        self.add_widget(Label(text="ASCII Formfeed (FF)", size_hint_x=1))
        self.formfeed = Button(text=r"\f")
        self.formfeed.bind(on_press=insert_append)
        self.add_widget(self.formfeed)

        self.add_widget(Label(text="ASCII Linefeed (LF)", size_hint_x=1))
        self.linefeed = Button(text=r"\n")
        self.linefeed.bind(on_press=insert_append)
        self.add_widget(self.linefeed)

        self.add_widget(Label(text="ASCII Carriage Return (CR)", size_hint_x=1))
        self.carriagereturn = Button(text=r"\r")
        self.carriagereturn.bind(on_press=insert_append)
        self.add_widget(self.carriagereturn)

        self.add_widget(Label(text="ASCII Horizontal Tab (TAB)", size_hint_x=1))
        self.tab = Button(text=r"\t")
        self.tab.bind(on_press=insert_append)
        self.add_widget(self.tab)

        self.add_widget(Label(text="ASCII char with hex value hh", size_hint_x=1))
        self.add_widget(Label(text=r"\xhh"))

        self.freestring = TextInput(multiline=False, text='')
        self.add_widget(self.freestring)
        self.setclose = Button(text='Close', size_hint_x=0.5)
        self.setclose.bind(on_press=lambda i=None: handler.calleble("l_helpDismiss")())
        self.freestring.bind(on_text_validate=insert_append)
        self.add_widget(self.setclose)


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

        # Popup for string special caracters help:
        self.answer = TextInput(multiline=False, text=r'\x02A,275,000.17,M,60,\x030E\r\n')
        self.premadestings_popup = Popup(title="Pre made sensor strings:",
                                         content=StringPreMadeText(insert=self.answer),
                                         size_hint=(None, None), size=(500, 400))
        self.answer.bind(on_triple_tap=self.premadestings_popup.open)
        self.stringhelp_popup = Popup(title="String Help\nTap 3 times in answer field for premade strings!",
                           content=StringTextInsertHelp(insert=self.answer),
                           size_hint=(None, None), size=(500, 400))
        self.stringhelp = Button(text='Answer (Help)', size_hint_x=0.5)
        self.stringhelp.bind(on_press=self.stringhelp_popup.open)
        self.add_widget(self.stringhelp)
        # close string help:
        handler.bind("l_helpDismiss", self.stringhelp_popup.dismiss)
        handler.bind("l_helpDismiss", self.premadestings_popup.dismiss)
        self.answer.bind(text= handler.calleble("f_Answer"))
        self.add_widget(self.answer)

        self.add_widget(Label(text='Question', size_hint_x=0.5))
        self.question = TextInput(multiline=False, text='?A')
        self.question.bind(text= handler.calleble("f_Question"))
        self.add_widget(self.question)

        self.add_widget(Label(text='Mode', size_hint_x=0.5))
        self.mode = Button(text='poll', font_size='20sp', background_normal='', background_color=[1, 0.5, 0, 1])
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
        b_startstop = ToggleButton(text='[size=28][b]Start[/b][/size]/Stop', stat="normal",
                                   markup=True, font_size='20sp',
                                   size_hint_x=1,
                                   background_normal='', background_color=[0.8, 0, 0, 1],
                                   background_down='')
        b_config = Button(text='Config', size_hint_x=0.5, font_size='20sp')
        self.add_widget(b_startstop)
        self.add_widget(b_config)
        b_config.bind(on_press=handler.calleble("b_conf"))
        # logic for toggelButton events:
        b_startstop.bind(
            state=lambda i, s: handler.calleble("b_stop")() if s == "normal" else handler.calleble("b_start")())
        def b_startstop_textstart():
            b_startstop.text= '[size=28][b]Start[/b][/size]/Stop'
        handler.bind("b_stop", b_startstop_textstart)
        def b_startstop_textstop():
            b_startstop.text= 'Start/[size=28][b]Stop[/b][/size]'
        handler.bind("b_start", b_startstop_textstop)
        # set b_startstop Button color acording to status:
        def startstop_off(*args):
            b_startstop.background_color = [0.8, 0, 0, 1]
        handler.bind("b_stop", startstop_off)
        def startstop_on(*args):
            b_startstop.background_color = [0, 0.5, 0, 1]
        handler.bind("b_start", startstop_on)
        def serial_acht(*args):
            """let start/stop button blink once if serial activity"""
            b_startstop.background_color = [0, 1, 0, 1]
            def setback(*args): b_startstop.background_color = [0, 0.5, 0, 1]
            Clock.schedule_once(setback, 0.2)
        handler.bind("serial_out", serial_acht)

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

""" # kivys internel event handler
class ErrorEvent(EventDispatcher):
    def __init__(self, **kwargs):
        self.register_event_type('on_error')
        super(ErrorEvent, self).__init__(**kwargs)

    def do_callerror(self, error):
        # when do_something is called, the 'on_test' event will be
        # dispatched with the value
        self.dispatch('on_error')

    def on_error(self, *args):
        print("event")
"""

class ErrorPopup(Popup):
    """Error message popup."""

    def __init__(self, error=SerialException, *args, **kwargs):
        """
        :argument error: error element
        """
        super(ErrorPopup, self).__init__(**kwargs)
        self.title = "Error"
        self.content = Label(text="Serial Error {0}:\n{1}".format( str(error.errno), str(error.message)))
        self.size_hint=(0.9, 0.25)
        #self.size=(400, 400)


class MyApp(App):

    def build(self):
        # controll pennel:
        controlslayout = GridLayout(cols=1, rows=2)
        controlslayout.add_widget(SerialConfig())
        controlslayout.add_widget(ControlPanel())
        # data pennel:

        # master layout:
        layout = GridLayout(rows=1)
        layout.add_widget(LogWindow())  # TODO: add log window and log
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
        # log file output:
        handler.bind("b_w-log", io.to_file)

        # error popup
        #erevents = ErrorEvent()
        def error(error):
            errpopup = ErrorPopup(error)
            errpopup.open()
        handler.bind("p_error", error)

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
        """"""
        self.sensor = seri.sensor(mode=     "poll",
                                  boud=     9600,
                                  com=      "/dev/ttyUSB0",
                                  interval= 1,
                                  answer=   "\x02A,275,000.17,M,60,\x030E\r\n",
                                  question= "?A")
        self.toconfig = seri.sensor(mode=     "poll",
                                  boud=     9600,
                                  com=      "/dev/ttyUSB0",
                                  interval= 1,
                                  answer=   "\x02A,275,000.17,M,60,\x030E\r\n",
                                  question= "?A")


    def s_stat(self, *args):
        if not self.sensor.isRuning:
            #print("Start Button")
            try: self.sensor._config()
            except SerialException as e:
                print("Serial Error {0}:  {1}".format(e.errno, e.message))
                handler.calleble("p_error")(error=e)
            else:
                self.sensor.start()
                # add data out put event
                self.sensor.bind(handler.calleble("serial_out"))

    def s_stop(self, *args):
        if self.sensor.isRuning:
            #print("Stop Button")
            self.sensor.stop()
            self.sensor._terminate()

    def s_conf(self, *args):
        """take config from toconfig and initialise it."""
        if not self.sensor.isRuning:
            #print("Config Button")
            self.sensor = self.toconfig
        else:
            handler.calleble("l_config")()

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
        self.toconfig.answer = str(val).decode('string-escape')

    def s_question(self, opt=None, val=None):
        """set question in toconfig."""
        self.toconfig.question = str(val).decode('string-escape')

    def s_mode(self, opt=None):
        """toggel mode in toconfig."""
        if self.toconfig.mode == "poll":
            self.toconfig.mode = "cont"
        else:
            self.toconfig.mode = "poll"

    def to_file(self, instance):
        """write text to file
        writes text in the 'textout' variable of the calling instance"""
        time = datetime.now()
        f = open("log"+str(time.now().date())+'_'+str(time.time())[:8].replace(':', '-')+".txt", mode='w')
        f.write(instance.textout)
        f.close()

    def get_data_in(self):
        """:return : input data from interface"""
        return self.sensor.get_in()


# --- Global stuff: ----

def load_string_samples():
    """load the xml config with the Pre made sting samples.
    :return dict: with xml config"""
    # read xml file and convert it do a dict.
    with open('stringsamples.xml') as fd:
         xml = xmltodict.parse(fd.read())
    return xml

handler = AssoziativHandler()
io = extern()
xml = load_string_samples()
if __name__ == '__main__':
    MyApp().run()
