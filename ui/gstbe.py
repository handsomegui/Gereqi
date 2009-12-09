#!/usr/bin/env python

import pygst
pygst.require("0.10")
import gst, thread, gobject
from os import path
from time import sleep
from PyQt4.QtCore import QObject, SIGNAL

class Extraneous:
    def to_milli(self, val):
        """
        Pointless really
        """
        milli = int(round(val / 1000000.0))
        return milli

    def can_play_source(self, source):
        """
        Gstreamer finds out if it would be able 
        to play the media source
        """
        return gst.element_make_from_uri(gst.URI_SRC, source, "") is not None
        
    def source_checks(self, source, type):
        fnow= None
        if type == "file" and path.isfile(source):
            fnow = "file://%s" % source
        elif type == "cd":
            fnow = "cdda://%s" % source
            
        if fnow and self.can_play_source(fnow): 
            return fnow
            
            
class Gstbe(QObject):
    def __init__(self):
        QObject.__init__(self)
        gobject.threads_init() # V.Important
        self.extra = Extraneous()

        self.pipe_line = gst.element_factory_make("playbin2", "player")
        self.pipe_line.connect("audio-changed",  self.__audio_changed)
        self.pipe_line.set_property('video-sink', None)
        self.set_volume(1)
        bus = self.pipe_line.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.__on_message)
        
        self.pipe_source = self.play_thread_id = None

    def __audio_changed(self, pipeline):
        print("AUDIO CHANGED", pipeline)
        self.emit(SIGNAL("track_changed()"))

    def __on_message(self, bus, msg):
        """
        Messages from pipe_line object
        """
        mtype = msg.type
        if mtype == gst.MESSAGE_EOS:
            print("EOS")
            Gstbe.play_thread_id = None            
            self.pipe_line.set_state(gst.STATE_NULL)
            self.emit(SIGNAL("finished()"))
        
        elif mtype == gst.MESSAGE_ERROR:
            print("ERROR")
            self.pipe_line.set_state(gst.STATE_NULL)
            err, debug = msg.parse_error()
            print("Error: %s" % err, debug)
            
        elif mtype == gst.MESSAGE_BUFFERING:
            print(msg)            
        
        
    def __whilst_playing(self):
        """
        Whilst a track is playing create a new thread to
        emit the playing-file's position
        """
        play_thread = self.play_thread_id
        
        while play_thread== self.play_thread_id:
            try:
                pos_int = self.pipe_line.query_position(gst.FORMAT_TIME)[0]
                val = int(round(pos_int / 1000000))
                self.emit(SIGNAL("tick ( int )"), val)
            except:
                pass
            sleep(1)

    def load(self, fname, type="file"):
        """
        A dynamic way of loading of media. Files, urls, cds 
        (last 2 are TODO) can be used. As we are using playbin2 
        we are actually queuing a track if one is already playing
        """
        # cdda://4   <-- cd track#4
        fnow = self.extra.source_checks(fname, type)
        if fnow:
            self.pipe_line.set_state(gst.STATE_NULL)
            self.pipe_line.set_property("uri", fnow)  
            self.pipe_line.set_state(gst.STATE_READY)
            self.pipe_source = fname
            return True
        else:
            print("ERROR: %s not loaded" % fname)
            return False
            
    def play(self):
        """
        If a file is loaded play  or unpause it
        """
        now = self.state()
        if (now == gst.STATE_READY) or (now == gst.STATE_NULL):
            print("PLAY")
            self.pipe_line.set_state(gst.STATE_PLAYING)
            Gstbe.play_thread_id = thread.start_new_thread(self.__whilst_playing, ())
        elif now == gst.STATE_PAUSED:
            print("UNPAUSE")
            self.pipe_line.set_state(gst.STATE_PLAYING)
            Gstbe.play_thread_id = thread.start_new_thread(self.__whilst_playing, ())
        else:
            print("FINISHED")
            self.emit(SIGNAL("finished()"))
        
    def pause(self):
        print("PAUSE")
        self.pipe_line.set_state(gst.STATE_PAUSED)
        self.play_thread_id = None
        
    def stop(self):
        print("STOP")
        if self.play_thread_id:
            self.play_thread_id = None
            self.pipe_line.set_state(gst.STATE_NULL)
   
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

    def enqueue(self, fname, type="file"):
        fnow  = self.extra.source_checks(fname, type)
        if fnow:
            print("ENQUEUE")
            self.pipe_line.set_property("uri", fnow)
            self.pipe_source = fname
            return True
        else:
            print("ERROR: %s not loaded" % fname)
            return False

    def mute(self, set):
        self.pipe_line.set_property("mute", set)

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
        return self.pipe_source
        
    def total_time(self):
        """
        This won't do anything until the pipe_line
        is in a PLAYING_STATE
        """
        dur = self.pipe_line.query_duration(gst.FORMAT_TIME)[0]
        return int(round(dur/ 1000000))
        
    def is_playing(self):
        return self.state() == gst.STATE_PLAYING
            
