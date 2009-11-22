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


    def current_source(self):
        """
        The pipe-line's current loaded track
        """
        # TODO: replace with GSreamer implementation
#        print self.pipe_line.get_property("uri")
        return self.pipe_source
        
    def total_time(self):
        """
        This won't do anything until the pipe_line
        is in a PLAYING_STATE
        """
        try:
            dur = self.pipe_line.query_duration(gst.FORMAT_TIME)[0]
        except:
            dur = None
        return dur
        
    def is_playing(self):
        return self.state() == gst.STATE_PLAYING
            
    def can_play_source(self, source):
        return gst.element_make_from_uri(gst.URI_SRC, source, "") is not None
        
    def source_checks(self, source, type):
        if type == "file":
            if path.isfile(source): 
                fnow = "file://%s" % source
        elif type == "cd":
            fnow = "cdda://%s" % source
            
        if self.can_play_source(fnow):
            return fnow


class Actions:
    """
    All methods that require playbin or
    its elements to do something
    """
    def load(self, fname, type="file"):
        """
        A dynamic way of loading of media. Files, urls, cds 
        (last 2 are TODO) can be used. As we are using playbin2 
        we are actually queuing a track if one is already playing
        """
        # cdda://4   <-- cd track#4
        fnow = self.source_checks(fname, type)
        if fnow:
            self.pipe_line.set_state(gst.STATE_NULL)
            self.pipe_line.set_property("uri", fnow)  
            self.pipe_line.set_state(gst.STATE_READY)
            print(fnow)          
            self.pipe_source = fname                
        else:
            print("ERROR: %s not loaded" % fname)
            
    def play(self):
        """
        If a file is loaded play  or unpause it
        """
        now = self.state()
        if (now == gst.STATE_READY) or (now == gst.STATE_NULL):
            print("PLAY")
            self.pipe_line.set_state(gst.STATE_PLAYING)
            self.play_thread_id = thread.start_new_thread(self.whilst_playing, ())
        elif now == gst.STATE_PAUSED:
            print("UNPAUSE")
            self.pipe_line.set_state(gst.STATE_PLAYING)
        else:
            print("FINISHED")
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
        
# TODO: convert the range into decibels
# interface.py is sort of doing this already with
# a sqrt function
    def set_volume(self, val):        
        if 0 <= val <= 1:
            self.pipe_line.set_property('volume', val)
        else:
            print("Incorrect volume value. 0 -> 1")

# FIXME: technically this should work much like in quod-libet.
# It doesn't. Get this error:
# CRITICAL **: deactivate_group: assertion `group->active' failed
    def enqueue(self, fname, type="file"):
        fnow  = self.source_checks(fname, type)
        if fnow:
            print("ENQUEUE")
            self.pipe_line.set_property("uri", fnow)
            self.pipe_source = fname

    def mute(self, set):
        self.pipe_line.set_property("mute", set)


class Player(Actions, Queries, QObject):
    def __init__(self):
        super(Player, self).__init__()
        gobject.threads_init() # V.Important

        self.pipe_line = gst.element_factory_make("playbin2", "player")
        self.pipe_line.connect("about-to-finish",  self.__about_to_finish)
        self.pipe_line.connect("audio-changed",  self.__audio_changed)

        self.pipe_line.set_property('video-sink', None)
        self.set_volume(1)
        
        bus = self.pipe_line.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.__on_message)

        # A crude method if what is currently loaded
        # into the pipeline. Could possibly use a Gstreamer
        # implementation instead.
        self.pipe_source = None        
        self.play_thread_id = None
            
    def __about_to_finish(self, pipeline):
        """
        Emit a signal implying a track is needed 
        for gapless playback
        """
        print("ABOUT TO FINISH", pipeline)
        self.emit(SIGNAL("about_to_finish()"))  
    
    def __audio_changed(self, pipeline):
        print("AUDIO CHANGED", pipeline)
        self.emit(SIGNAL("track_changed()"))

#FIXME: the message type output is not as expected
    def __on_message(self, bus, msg):
        """
        Messages from pipe_line object
        """
        mtype = msg.type
        if mtype == gst.MESSAGE_EOS:
            print("EOS")
            self.play_thread_id = None            
            self.pipe_line.set_state(gst.STATE_NULL)
            self.emit(SIGNAL("finished()"))
        
        elif mtype == gst.MESSAGE_ERROR:
            print("ERROR")
            self.pipe_line.set_state(gst.STATE_NULL)
            err, debug = msg.parse_error()
            print("Error: %s" % err, debug)
            
        elif mtype == gst.MESSAGE_BUFFERING:
            print(msg)            
        
        
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


