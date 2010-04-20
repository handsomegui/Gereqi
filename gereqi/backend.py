#Copyright 2009 Jonathan.W.Noble <jonnobleuk@gmail.com>

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
from PyQt4.QtCore import QObject, QTime, SIGNAL, QString


from database import Media
from gstbe import Gstbe

class AudioBackend:
    def __init__(self, parent):
        self.ui = parent
        self.media_db = Media()
        self.just_finished = False
        self.__gstreamer_init()
            
    def __gstreamer_init(self):
        """
        Sets up the environment/signals on
        backend initialisation
        """
        self.audio_object = Gstbe()
        QObject.connect(self.audio_object, SIGNAL("tick ( int )"), self.__prog_tick)
        self.audio_object.pipe_line.connect("about-to-finish", self.__about_to_finish)
        QObject.connect(self.audio_object, SIGNAL("track_changed()"), self.__track_changed)
        QObject.connect(self.audio_object, SIGNAL("finished()"), self.__finished_playing)
        QObject.connect(self.ui.stopBttn, SIGNAL("pressed()"), self.__finished_playing)
        
    def __about_to_finish(self, pipeline):
        """
        Generates a track to go into queue
        before playback stops
        """
        self.just_finished = True
        track = self.ui.tracking.generate_track("next")
        #Not at end of  playlist
        if track is not None:
            self.audio_object.enqueue(track)

    def __prog_tick(self, time):
        """
        Every second update time labels and progress slider
        """
        t_now = QTime(0, (time / 60000) % 60, (time / 1000) % 60)
        now = t_now.toString('mm:ss')
        max_time = self.ui.t_length.toString('mm:ss')
        self.ui.progLbl.setText("%s | %s" % (now, max_time))            
        # Allows normal playback whilst slider still grabbed
        if self.ui.progSldr.value() == self.ui.old_pos: 
            self.ui.progSldr.setValue(time)
        self.ui.old_pos = time
        
    def __track_changed(self):
        """
        When the playing track changes certain
        Ui features may need to be updated.
        """
        # Cannot do it in "about_to_finish" as it's in another thread
        if self.just_finished is True:
            self.just_finished = False
            self.__inc_playcount()
        
        self.ui.tracking.generate_info()
        self.ui.set_info()
        self.ui.set_prog_sldr()
        self.ui.old_pos = 0
        self.ui.progSldr.setValue(0)
        
    def __finished_playing(self):
        """
        Things to be performed when the playback finishes
        """
        self.just_finished = False
        self.ui.horizontal_tabs.setTabEnabled(1, False)
        self.ui.horizontal_tabs.setTabEnabled(2, False)
        self.ui.playBttn.setChecked(False)
        self.ui.stopBttn.setEnabled(False)
        self.ui.progSldr.setValue(0)
        self.ui.old_pos = 0
        self.ui.xtrawdgt.stat_lbl.setText("Stopped")
        self.ui.progLbl.setText("00:00 | 00:00")
        # clear things like wiki and reset cover art to default        
        self.ui.wiki_view.setHtml(QString(""))
        self.ui.cover_view.setPixmap(QPixmap(":/Icons/music.png"))
        self.ui.trkNowBox.setTitle(QString("No Track Playing"))
        self.ui.art_alb["oldart"] = self.ui.art_alb["oldalb"] = None
        self.ui.xtrawdgt.tray_icon.setToolTip("Stopped")
        
    def __inc_playcount(self):
        """
        Probably better to do this within the database.
        """
        now = self.ui.tracking.generate_track("back")
        playcount = int(self.media_db.get_info(unicode(now))[5])
        playcount += 1
        self.media_db.inc_count(playcount, unicode(now))
        
