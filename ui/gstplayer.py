#!/usr/bin/env python

import gst, time
from os import path

class Player:
    def __init__(self):
        self.playbin = gst.element_factory_make("playbin","amaroq")
        fakesink = gst.element_factory_make("fakesink","fakesink")
        self.playbin.set_property("video-sink",fakesink)
        bus = self.playbin.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)

    def on_message(self, bus, msg):
        msg_type = msg.type()
        print msg_type, msg

    def load(self, fname):
        if path.isfile(fname):
            file_now = "file://%s" % fname
            print file_now
            self.playbin.set_property("uri",file_now)

    def play(self):
        self.playbin.set_state(gst.STATE_PLAYING)

    def stop(self):
        self.playbin.set_state(gst.STATE_NULL)
    
    def pause(self):
        self.playbin.set_state(gst.STATE_READY)
        self.playbin.set_state(gst.STATE_PAUSED)
        
