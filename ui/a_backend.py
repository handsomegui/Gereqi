#!/usr/bin/env python
import pygst
pygst.require("0.10")

import gst
from os import path

class Player:
    def __init__(self):
        self.pipe_line = gst.Pipeline("mypipeline")
        
        self.filesrc = gst.element_factory_make("filesrc", "file-source")
        self.pipe_line.add(self.filesrc)
        
        self.decoder = gst.element_factory_make("decodebin", "decoder")
        self.decoder.connect("new-decoded-pad", self.OnDynamicPad)
        self.pipe_line.add(self.decoder)
        self.filesrc.link(self.decoder)
        
        self.converter = gst.element_factory_make("audioconvert", "converter")
        self.pipe_line.add(self.converter)
        
        self.vol = gst.element_factory_make("volume", "volume")
        self.pipeline.add(self.vol)		
        self.converter.link(self.vol)
        
        self.sink = gst.element_factory_make("alsasink", "sink")
        self.pipe_line.add(self.sink)
        self.vol.link(self.sink)
        
        self.pipeline.get_by_name("volume").set_property('volume', 1)
        self.pipe_line.set_state(gst.STATE_READY)
        
        bus = self.pipe_line.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.On_Message)

    def On_Message(self, bus, msg):
        print(msg.type, msg)

    def OnDynamicPad(self, dbin, pad, islast):
        print "OnDynamicPad called!"
        pad.link(self.converter.get_pad("sink"))
            
    def load(self, fname):
        """
        This is for file-src so file:// doesn't
        seem to be necessary. CD and url sources
        may be tricky later on. I hope not.
        """
        if path.isfile(fname):
            self.pipe_line.get_by_name("file-source").set_property("location", filename)
            
    def play(self):
        self.pipe_line.set_state(gst.STATE_PLAYING)
        
    def stop(self):
        self.pipe_line.set_state(gst.STATE_NULL)
        
    def set_volume(self, val):
        if 0 <= val <= 1:
            self.pipeline.get_by_name("volume").set_property('volume', val)

