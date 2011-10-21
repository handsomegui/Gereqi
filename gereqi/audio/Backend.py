# This file is part of Gereqi.
#
# Gereqi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Gereqi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gereqi.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4.QtGui import QPixmap
from PyQt4.QtCore import QObject, QTime

import time

from Gstreamer import Gstbe
from PhononBE import PhononBE

class AudioBackend:
    recently_played = []
    
    def __init__(self, parent, mode=0):
        """
        Mode: 0 = phonon; 1 = gstreamer
        """
        self.ui = parent
        self.just_finished = False
        self.mode = mode
        if mode == 0:
            self.__phonon_init()
        elif mode == 1:
            self.__gstreamer_init()
        else:
            raise Exception("No such audio mode")
        
        self.ui.stop_bttn.pressed.connect(self.__finished_playing) 
            
    def __gstreamer_init(self):
        """
        Sets up the environment/signals on
        backend initialisation
        """
        self.audio_object = Gstbe()        
        # signal/slots
        self.audio_object.tick.connect(self.__prog_tick)
        self.audio_object.track_changed.connect(self.__track_changed)
        self.audio_object.finished.connect(self.__finished_playing)              
        self.audio_object.pipe_line.connect("about-to-finish", self.__about_to_finish)
        
    def __phonon_init(self):
        self.audio_object = PhononBE()
        # signal/slots
        self.audio_object.aboutToFinish.connect(self.__about_to_finish)
        self.audio_object.tick.connect(self.__prog_tick)
        self.audio_object.currentSourceChanged.connect(self.__track_changed)
        self.audio_object.finished.connect(self.__finished_playing)
        self.ui.progress_sldr.setMediaObject(self.audio_object)
        
    def __about_to_finish(self, pipeline=None):
        """
        Generates a track to go into queue
        before playback stops
        """
        self.recently_played.append(self.audio_object.current_source())
        self.just_finished = True
        track = self.ui.tracking.next()
        # Not at end of playlist
        if track:
            self.audio_object.load(track)

    def __prog_tick(self, time):
        """
        Every second update time labels and progress slider
        Time is millis
        """      
        self.timeval_to_label(time)
        
    def __track_changed(self):
        """
        When the playing track changes certain
        Ui features may need to be updated.
        """
        # Cannot do it in "about_to_finish" as it's in another thread
        if self.just_finished:
            self.just_finished = False
            self.__inc_playcount()
        
        self.ui.tracking.generate_info()
        self.ui.set_info()
        self.ui.set_prog_sldr()
        self.ui.tray_tooltip()
        
    def __finished_playing(self):
        """
        Things to be performed when the playback finishes
        """
        self.just_finished = False
        self.recently_played = []
        self.ui.horizontal_tabs.setTabEnabled(1, False)
        self.ui.horizontal_tabs.setTabEnabled(2, False)
        self.ui.play_bttn.setChecked(False)
        self.ui.stop_bttn.setEnabled(False)
        self.ui.stat_lbl.setText("Stopped")
        self.ui.progress_lbl.setText("00:00 | 00:00")
        # clear things like wiki and reset cover art to default        
        self.ui.wiki_view.setHtml("")
        self.ui.art_alb["oldart"] = self.ui.art_alb["oldalb"] = None
        self.ui.tray_icon.setToolTip("Stopped")
        
    def __inc_playcount(self):
        """
        Doesn't actually change count. Adds notification
        of full-play into the historyDB table
        """
        track = self.ui.tracking.previous()
        timestamp = time.time()
        self.ui.media_db.inc_count(timestamp, track)
        
    def timeval_to_label(self, val):
        """
        Convert the tracks play-length into a format
        suitable for label widget and set
        """
        t_now = QTime(0, (val / 60000) % 60, (val / 1000) % 60)
        now = t_now.toString('mm:ss')
#        max_time = self.ui.t_length.toString('mm:ss')
        self.ui.progress_lbl.setText("%s | %s" % (now, "")) 
        
