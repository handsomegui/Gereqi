#!/usr/bin/env python
import pygst
pygst.require("0.10")

import gst#, gobject
from os import path

class Player:
    pipe_source = None
    
    def __init__(self):
        #gobject.threads_init()
        self.pipe_line = gst.Pipeline("mypipeline")
        
        # Negates the need for 'file://' May prove awkward later on
        self.filesrc = gst.element_factory_make("filesrc", "file-source")
        self.pipe_line.add(self.filesrc)
        
        # Automatic decoder. As it deals with many formats it has multiple
        # pads that have to be dynamically linked to the converter
        self.decoder = gst.element_factory_make("decodebin", "decoder")
        self.decoder.connect("new-decoded-pad", self.on_dynamic_pad)
        self.pipe_line.add(self.decoder)
        self.filesrc.link(self.decoder)
        
        self.converter = gst.element_factory_make("audioconvert", "converter")
        self.pipe_line.add(self.converter)
        
        # Range is long 0 -> 1
        self.vol = gst.element_factory_make("volume", "volume")
        self.pipe_line.add(self.vol)        
        self.converter.link(self.vol)
        
        # Don't care for Pulseaudio
        self.sink = gst.element_factory_make("alsasink", "sink")
        self.pipe_line.add(self.sink)
        self.vol.link(self.sink)
        
        self.pipe_line.get_by_name("volume").set_property('volume', 1)
        
        bus = self.pipe_line.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)

    def on_message(self, bus, msg):
        """
        Messages from pipe_line object
        """
        msg_type = msg.type
        
        if msg_type == gst.MESSAGE_ERROR:
            self.pipe_line.set_state(gst.STATE_NULL)
            err, debug = msg.parse_error()
            print("Error: %s" % err, debug)

    def on_dynamic_pad(self, dbin, pad, islast):
        """
        File-src has manypads due to multiple formats.
        Have to be connected to the converter
        """
        pad.link(self.converter.get_pad("sink"))
        
    def get_state(self):
        """
        To find out pipe_line's current state
        """
        
    def current_source(self):
        return self.pipe_source

    def load(self, fname):
        """
        This is for file-src so file:// doesn't
        seem to be necessary. CD and url sources
        may be tricky later on. I hope not.
        """
        #FIXME:  Changing the `location' property on filesink when a file is open is not supported.
        if path.isfile(fname):            
            self.pipe_line.get_by_name("file-source").set_property(\
                "location", fname)
            self.pipe_source = fname
            self.pipe_line.set_state(gst.STATE_READY)
        else:
            print("Error: %s not loaded" % fname)
            
    def play(self):
        #TODO: check for state. i.e paused
        self.pipe_line.set_state(gst.STATE_PLAYING)
        
    def pause(self):
        self.pipe_line.set_state(gst.STATE_PAUSED)
        
    def stop(self):
        self.pipe_line.set_state(gst.STATE_NULL)
        
    def set_volume(self, val):
        if 0 <= val <= 1:
            self.pipe_line.get_by_name("volume").set_property('volume', val)

