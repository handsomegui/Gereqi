#!/usr/bin/env python

import pygst
pygst.require("0.10")
import gst, thread, gobject
from os import path
from time import sleep
from PyQt4.QtCore import QObject, SIGNAL

class Queries:
    """
    All methods that query the playbin and
    its elements
    """
#TODO: parsing of stat
    def state(self):
        """
        To find out pipe_line's current state
        """
        return self.pipe_line.get_state(1)

# TODO: replace with GSreamer implementation
    def current_source(self):
        """
        The pipe-line's current loaded track
        """
        return self.pipe_source
        
    def total_time(self):
        """
        This won't do anything until the pipe_line
        is in a PLAYING_STATE
        """
        try:
            dur = self.pipe_line.query_duration(self.time_format)[0]
        except:
            dur = None
        return dur
        
# TODO: replace with GStreamer implementation
    def is_playing(self):
        if self.play_thread_id:
            return True
        else:
            return False


class Actions:
    """
    All methods that require playbin or
    its elements to do something
    """
    
    def load(self, fname, how="now"):
        """
        This is for file-src so file:// doesn't seem to be necessary.
        CD and url sources   may be tricky later on. I hope not.
        """
        #FIXME:  Changing the `location' property on filesink when a file is open is not supported.
        if path.isfile(fname):  
            self.pipe_line.set_state(gst.STATE_NULL)
            self.pipe_line.get_by_name("file-source").set_property(\
                "location", fname)
            self.pipe_source = fname
            self.queue = fname
            self.pipe_line.set_state(gst.STATE_READY)
        else:
            print("Error: %s not loaded" % fname)
            
    def play(self):
        """
        If a file is loaded play  or unpause it
        """
        #TODO: check for state. i.e paused
        now = self.state()[1]
        if self.queue:
            if (now == gst.STATE_READY):
                self.pipe_line.set_state(gst.STATE_PLAYING)
                self.play_thread_id = thread.start_new_thread(self.whilst_playing, ())
                self.queue = None
            else:
                # This is not gapless
                print("AUTOQUEUE")
                self.load(self.queue)
                self.pipe_line.set_state(gst.STATE_PLAYING)
                self.play_thread_id = thread.start_new_thread(self.whilst_playing, ())
                self.queue = None
                
        elif now == gst.STATE_PAUSED:
            print("UNPAUSE")
            self.pipe_line.set_state(gst.STATE_PLAYING)
        else:
            pass
#            self.emit(SIGNAL, ("finished()"))
        
    def pause(self):
        self.pipe_line.set_state(gst.STATE_PAUSED)
        
    def stop(self):
        if self.play_thread_id:
            self.play_thread_id = None
            self.pipe_line.set_state(gst.STATE_NULL)
   
#TODO: Find a cleaner seek method. This has a nasty sounding 'blip'
    def seek(self, val):
        """
        Seek to a time-position(in nS) of playing file
        """
        pos = val * 1000000        
        self.pipe_line.seek_simple(self.time_format, gst.SEEK_FLAG_FLUSH, pos)
        
    def set_volume(self, val):
        if 0 <= val <= 1:
            self.pipe_line.get_by_name("volume").set_property('volume', val)
        else:
            print("Incorrect volume value. 0 -> 1")

#FIXME: do not do this
    def enqueue(self, fname):
        print(fname)
#        self.load(fname,"queue")
        self.queue = fname

    def clear_queue(self):
        pass

#TODO: may need a queueBin for gapless playback
#FIXME: in order for this to me signal/slot compatible
# this needs to be a QObject
class Player(Actions, Queries, QObject):
    def __init__(self):
        super(Player, self).__init__()
        gobject.threads_init() # V.Important
        
        # Where everything goes
        # filesrc ! decodebin ! audioconvert ! volume ! alsasink
        self.pipe_line = gst.Pipeline("mypipeline")         
        # Negates the need for 'file://' May prove awkward later on
        self.filesrc = gst.element_factory_make("filesrc", "file-source")
        self.pipe_line.add(self.filesrc)
        
        
        self.queuer = gst.element_factory_make("queue", "queuer")
        self.pipe_line.add(self.queuer)
        self.filesrc.link(self.queuer)

        # Automatic decoder. As it deals with many formats it has multiple
        # pads that have to be dynamically linked to the converter
        self.decoder = gst.element_factory_make("decodebin", "decoder")
        self.decoder.connect("new-decoded-pad", self.__on_dynamic_pad)
        self.pipe_line.add(self.decoder)
        self.queuer.link(self.decoder)
        
        # Has to be dynamically linked to
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

        # gst.FORMAT_TIME is in nanoSeconds
        # TODO: try and find a millisecond time format
        self.time_format = gst.Format(gst.FORMAT_TIME)
        
        # A crude method if what is currently loaded
        # into the pipeline. Could possibly use a Gstreamer
        # implementation instead.
        self.pipe_source = None
        
        # A crude queue method that's currently not used.
        # Should really be replaced with a queueBin
        self.queue = None
        self.play_thread_id = None
        
        # get_clock()?
        bus = self.pipe_line.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.__on_message)

#FIXME: the message type output is not as expected
    def __on_message(self, bus, msg):
        """
        Messages from pipe_line object
        """
        msg_type = msg.type
        if msg_type == gst.MESSAGE_EOS:
            print("EOS")
            if self.queue:
                self.play()
            else:
                self.play_thread_id = None            
                self.pipe_line.set_state(gst.STATE_NULL)
        
        elif msg_type == gst.MESSAGE_ERROR:
            print("ERROR")
            self.pipe_line.set_state(gst.STATE_NULL)
            err, debug = msg.parse_error()
            print("Error: %s" % err, debug)

    def __on_dynamic_pad(self, dbin, pad, islast):
        """
        File-src has manypads due to multiple formats.
        Have to be connected to the converter
        """
        pad.link(self.converter.get_pad("sink"))
        
    def to_milli(self, val):
        """
        Pointless really
        """
        milli = int(round(val / 1000000.0))
        return milli
        
    def whilst_playing(self):
        """
        Whilst a track is playing create a new thread to
        emit the playing-file's position
        """
        play_thread_id = self.play_thread_id
        dur = None
        ab2finish = False
        
        # Stay here until we have a current_source
        # total_time duration
        while not dur:
            dur = self.total_time()            
            sleep(0.1)
        
        dur = self.to_milli(dur)
        print dur

        while play_thread_id == self.play_thread_id:
            try:
                pos_int = self.pipe_line.query_position(self.time_format)[0]
                val = self.to_milli(pos_int)
                self.emit(SIGNAL("tick ( int )"), val)
                if dur - val < 2000 and not ab2finish:
                    print("SPAM!")
                    ab2finish = True
                    #TODO: find if a similar message  is output via
                    # pipe-line's bus
                    self.emit(SIGNAL("aboutToFinish()"))                    
            except:
                pass
            sleep(1)
