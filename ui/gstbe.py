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
        return self.pipe_line.get_state(1)[1]

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
        if self.state() == gst.STATE_PLAYING:
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
            self.pipe_line.set_property('uri', fname)
            self.pipe_line.set_state(gst.STATE_PAUSED) 
            self.pipe_source = fname
        else:
            print("Error: %s not loaded" % fname)
            
    def play(self):
        """
        If a file is loaded play  or unpause it
        """
        #TODO: check for state. i.e paused
        now = self.state()
        if self.queue:
            if now == gst.STATE_READY:
                print("PLAY")
                self.pipe_line.set_state(gst.STATE_PLAYING)
                self.play_thread_id = thread.start_new_thread(self.whilst_playing, ())
                self.queue = None
            else:
                # This is not gapless
                self.load(self.queue)
                self.pipe_line.set_state(gst.STATE_PLAYING)
                self.play_thread_id = thread.start_new_thread(self.whilst_playing, ())
                self.emit(SIGNAL("autoqueued()"))
                self.queue = None
                print("AUTOQUEUE")
                
        elif now == gst.STATE_PAUSED:
            print("UNPAUSE")
            self.pipe_line.set_state(gst.STATE_PLAYING)
        else:
            self.emit(SIGNAL("finished()"))
        
    def pause(self):
        print("PAUSE")
        self.pipe_line.set_state(gst.STATE_PAUSED)
        
    def stop(self):
        print("STOP")
        if self.play_thread_id:
            self.play_thread_id = None
            self.pipe_line.set_state(gst.STATE_NULL)
   
#TODO: Find a cleaner seek method. This has a nasty sounding 'blip'
    def seek(self, val):
        """
        Seek to a time-position(in nS) of playing file
        """
        pos = val * 1000000        
        event = gst.event_new_seek(1.0, gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH,
                gst.SEEK_TYPE_SET, pos, gst.SEEK_TYPE_NONE, 0)
        self.pipe_line.send_event(event)
        
    def set_volume(self, val):
        if 0 <= val <= 1:
            self.pipe_line.set_property('volume', val)
        else:
            print("Incorrect volume value. 0 -> 1")

#FIXME: do not do this
    def enqueue(self, fname):
        print(fname)
        self.pipe_line.set_property('uri', fname)
        self.pipe_source = fname


#TODO: may need a queueBin for gapless playback
#FIXME: in order for this to me signal/slot compatible
# this needs to be a QObject
class Player(Actions, Queries, QObject):
    def __init__(self):
        super(Player, self).__init__()
        gobject.threads_init() # V.Important
        
        device, sinkname = self.gstreamer_sink("gconfaudiosink")
        self.pipe_line = gst.element_factory_make('playbin2')
        self.pipe_line.connect('about-to-finish',  self.__about_to_finish)
        bufbin = gst.Bin()
        queue = gst.element_factory_make('queue')
        queue.set_property('max-size-time', 1000 * gst.MSECOND)
        bufbin.add(queue, device)
        queue.link(device)
        gpad = gst.GhostPad('sink', queue.get_pad('sink'))
        bufbin.add_pad(gpad)
        
        self.pipe_line.set_property('audio-sink', bufbin)
        self.pipe_line.set_property('video-sink', None)
        
        bus = self.pipe_line.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.__on_message)

        # A crude method if what is currently loaded
        # into the pipeline. Could possibly use a Gstreamer
        # implementation instead.
        self.pipe_source = None
        
        # A crude queue method that's currently not used.
        # Should really be replaced with a queueBin
        self.queue = None
        self.play_thread_id = None
        
    def gstreamer_sink(self, pipeline):
        """
        Try to create a GStreamer pipeline:
        * Try making the pipeline (defaulting to gconfaudiosink).
        * If it fails, fall back to autoaudiosink.
        * If that fails, complain loudly.
        Savagely copied from quod-libet
        """
        if pipeline == "gconf": 
            pipeline = "gconfaudiosink"
        try: 
            pipe = gst.parse_launch(pipeline)
        except gobject.GError, err:
            if pipeline != "autoaudiosink":
                try: 
                    pipe = gst.parse_launch("autoaudiosink")
                except gobject.GError: 
                    pipe = None
                else: 
                    pipeline = "autoaudiosink"
            else: 
                pipe = None
        if pipe: 
            return pipe, pipeline
        else:
            print("Error: Unable to create audio output")
            
    def __about_to_finish(self, pipeline):
        self.emit(SIGNAL("about_to_finish()"))  

#FIXME: the message type output is not as expected
    def __on_message(self, bus, msg):
        """
        Messages from pipe_line object
        """
        if msg.type == gst.MESSAGE_EOS:
            print("EOS")
            self.play_thread_id = None            
            self.pipe_line.set_state(gst.STATE_NULL)
            self.emit(SIGNAL("finished()"))
        
        elif msg.type == gst.MESSAGE_ERROR:
            print("ERROR")
            self.pipe_line.set_state(gst.STATE_NULL)
            err, debug = msg.parse_error()
            print("Error: %s" % err, debug)
        
        
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
        # Stay here until we have a current_source
        # total_time duration
        while not dur:
            dur = self.total_time()            
            sleep(0.1)
        
        dur = self.to_milli(dur)

        while play_thread_id == self.play_thread_id:
            try:
                pos_int = self.pipe_line.query_position(gst.FORMAT_TIME)[0]
                val = self.to_milli(pos_int)
                self.emit(SIGNAL("tick ( int )"), val)
            except:
                pass
            sleep(1)
