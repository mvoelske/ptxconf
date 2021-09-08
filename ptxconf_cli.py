#! /usr/bin/python
import json
from ptxconftools import ConfController
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as appindicator
import os


class PTXConfCLI():
    def __init__(self):
        self.my_conf = ConfController()
        self.state_file_name = os.path.join(os.environ['HOME'], '.config', 'ptxconf-cli.json')
        os.makedirs(os.path.dirname(self.state_file_name), exist_ok=True)
        self.pens = list(sorted(self.my_conf.getPenTouchIds().keys()))
        self.monitors = list(sorted(self.my_conf.getMonitorIds()[0].keys()))
        if os.path.isfile(self.state_file_name):
            with open(self.state_file_name) as f:
                self.state = json.load(f)
        else:
            self.state = dict(active_monitor=0, active_pen=0)

    def save_state(self):
        with open(self.state_file_name, 'w') as f:
            json.dump(self.state, f)

    def next_monitor(self):
        if self.state['active_monitor'] < len(self.monitors) - 1:
            self.state['active_monitor'] += 1
        else:
            self.state['active_monitor'] = 0
        self.save_state()
        self.map_tablet()
        os.system(f'notify-send "ptxconf" "pen mapped to {self.monitors[self.state["active_monitor"]]}"')

    def map_tablet(self, callback_data=None):
        pen = self.pens[self.state['active_pen']]
        monitor = self.monitors[self.state['active_monitor']]
        # call API with these settings
        self.my_conf.setPT2Monitor(pen, monitor)


import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)
p = PTXConfCLI()
print(p.monitors)
print(p.pens)
p.next_monitor()