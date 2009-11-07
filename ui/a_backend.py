#!/usr/bin/env python

import pygst
pygst.require("0.10")
import gst, thread, gobject
from os import path
from time import sleep
from PyQt4.QtCore import QObject, SIGNAL


#TODO: may need a queueBin for gapless playback
#FIXME: in order for this to me signal/slot compatible
# this needs to be a QObject
class Player(QObject):
    def __init__(self):
        super(Player, self).__init__()
        gobject.threads_init() # V.Important
        
        # Where everything goes
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

        self.time_format = gst.Format(gst.FORMAT_TIME)
        self.pipe_source = None
        self.queue = None
        
        # get_clock()?
        bus = self.pipe_line.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)

    def on_message(self, bus, msg):
        """
        Messages from pipe_line object
        """
        msg_type = msg.type
        print(msg)
        if msg_type == gst.MESSAGE_EOS:
            self.play_thread_id = None
            self.pipe_line.set_state(gst.STATE_NULL)
        
        elif msg_type == gst.MESSAGE_ERROR:
            self.pipe_line.set_state(gst.STATE_NULL)
            err, debug = msg.parse_error()
            print("Error: %s" % err, debug)

    def on_dynamic_pad(self, dbin, pad, islast):
        """
        File-src has manypads due to multiple formats.
        Have to be connected to the converter
        """
        pad.link(self.converter.get_pad("sink"))
        
    def to_milli(self, val):
        milli = int(round(val / 1000000.0))
        return milli
        
    def whilst_playing(self):
        """
        Whilst a track is playing create a new thread to
        emit the playing-file's position
        """
        play_thread_id = self.play_thread_id
        dur = 0
        
        while dur == 0:
            try:
                dur = self.total_time()
            except:
                pass
            sleep(0.1)

        print dur

        while play_thread_id == self.play_thread_id:
            try:
                pos_int = self.pipe_line.query_position(self.time_format)[0]
                val = self.to_milli(pos_int)
                self.emit(SIGNAL("tick ( int )"), val)
                if dur - val < 2000:
                    print("SPAM!")
                    self.emit(SIGNAL("aboutToFinish()"))                    
            except:
                pass
            sleep(1)

    def state(self):
        """
        To find out pipe_line's current state
        """
        return self.pipe_line.get_state()
        
    def current_source(self):
        return self.pipe_source
        
    def total_time(self):
        """
        Thiswon't do anything until the pipe_line
        is in a PLAYING_STATE
        """
        dur = self.pipe_line.query_duration(self.time_format)[0]
        return self.to_milli(dur)
        
    def load(self, fname):
        """
        This is for file-src so file:// doesn't seem to be necessary.
        CD and url sources   may be tricky later on. I hope not.
        """
        #FIXME:  Changing the `location' property on filesink when a file is open is not supported.
        if path.isfile(fname):            
            self.pipe_line.get_by_name("file-source").set_property(\
                "location", fname)
            self.pipe_source = fname
            self.queue = fname
            self.pipe_line.set_state(gst.STATE_READY)
        else:
            print("Error: %s not loaded" % fname)
            
    def play(self):
        #TODO: check for state. i.e paused
        if self.queue:
            self.pipe_line.set_state(gst.STATE_PLAYING)
            self.play_thread_id = thread.start_new_thread(self.whilst_playing, ())
            self.queue = None
        else:
            pass
#            self.emit(SIGNAL, ("finished()"))
        
    def pause(self):
        self.pipe_line.set_state(gst.STATE_PAUSED)
        
    def stop(self):
        self.play_thread_id = None
        self.pipe_line.set_state(gst.STATE_NULL)
        
    def seek(self, val):
        """
        Seek to a time-position(in nS) of playing file
        """
        pos = val * 1000000        
        self.pipe_line.seek_simple(self.time_format, gst.SEEK_FLAG_SEGMENT, pos)
        
    def set_volume(self, val):
        if 0 <= val <= 1:
            self.pipe_line.get_by_name("volume").set_property('volume', val)

    def enqueue(self, fname):
        self.queue = fname
