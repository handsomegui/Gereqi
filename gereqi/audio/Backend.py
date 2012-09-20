# -*- coding: utf-8 -*-
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
from PhononBE import PhononBE
from ..storage.Collection import CollectionDb

import time


class AudioBackend:
    recently_played = []
    
    def __init__(self, parent):
        self.ui             = parent        
        self.db             = CollectionDb("backend")
        self.just_finished  = False
        self.__phonon_init()      

        
    def timeval_to_label(self, val):
        """
        Convert the tracks play-length into a format
        suitable for label widget and set
        """
        trk_time    = self.audio_object.totalTime() # FIXME: this is wrong n the transistion period
        trk_time    = QTime(0, (trk_time  / 60000) % 60, (trk_time / 1000) % 60)
        t_now       = QTime(0, (val / 60000) % 60, (val / 1000) % 60)
        self.ui.progress_lbl.setText("%s | %s" % (t_now.toString('mm:ss'), 
                                                  trk_time.toString("mm:ss"))) 
        
    def __phonon_init(self):
        self.audio_object = PhononBE()
        # signal/slots
        self.audio_object.aboutToFinish.connect(self.__about_to_finish)
        self.audio_object.tick.connect(self.__prog_tick)
        self.audio_object.currentSourceChanged.connect(self.__track_changed)
        self.audio_object.finished.connect(self.__finished_playing)
        self.ui.progress_sldr.setMediaObject(self.audio_object)                
        self.ui.stop_bttn.pressed.connect(self.__finished_playing)  
        
    def __about_to_finish(self, pipeline=None):
        """
        Generates a track to go into queue
        before playback stops
        """
        self.recently_played.append(self.audio_object.current_source())
        self.just_finished  = True
        track               = self.ui.playlist_table.next()
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
        
        self.ui.generate_info()
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
        track       = self.ui.playlist_table.previous()
        timestamp   = time.time()
        self.db.inc_count(timestamp, track)
