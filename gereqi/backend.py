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
        self.ui_main = parent
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
        QObject.connect(self.ui_main.stop_bttn, SIGNAL("pressed()"), self.__finished_playing)
        
    def __about_to_finish(self, pipeline):
        """
        Generates a track to go into queue
        before playback stops
        """
        self.just_finished = True
        track = self.ui_main.tracking.generate_track("next")
        #Not at end of  playlist
        if track is not None:
            self.audio_object.enqueue(track)

    def __prog_tick(self, time):
        """
        Every second update time labels and progress slider
        """
        t_now = QTime(0, (time / 60000) % 60, (time / 1000) % 60)
        now = t_now.toString('mm:ss')
        max_time = self.ui_main.t_length.toString('mm:ss')
        self.ui_main.progress_lbl.setText("%s | %s" % (now, max_time))            
        # Allows normal playback whilst slider still grabbed
        if self.ui_main.progress_sldr.value() == self.ui_main.old_pos: 
            self.ui_main.progress_sldr.setValue(time)
        self.ui_main.old_pos = time
        
    def __track_changed(self):
        """
        When the playing track changes certain
        Ui features may need to be updated.
        """
        # Cannot do it in "about_to_finish" as it's in another thread
        if self.just_finished is True:
            self.just_finished = False
            self.__inc_playcount()
        
        self.ui_main.tracking.generate_info()
        self.ui_main.set_info()
        self.ui_main.set_prog_sldr()
        self.ui_main.old_pos = 0
        self.ui_main.progress_sldr.setValue(0)
        
    def __finished_playing(self):
        """
        Things to be performed when the playback finishes
        """
        self.just_finished = False
        self.ui_main.horizontal_tabs.setTabEnabled(1, False)
        self.ui_main.horizontal_tabs.setTabEnabled(2, False)
        self.ui_main.play_bttn.setChecked(False)
        self.ui_main.stop_bttn.setEnabled(False)
        self.ui_main.progress_sldr.setValue(0)
        self.ui_main.old_pos = 0
        self.ui_main.xtrawdgt.stat_lbl.setText("Stopped")
        self.ui_main.progress_lbl.setText("00:00 | 00:00")
        # clear things like wiki and reset cover art to default        
        self.ui_main.wiki_view.setHtml(QString(""))
        self.ui_main.cover_view.setPixmap(QPixmap(":/Icons/music.png"))
        self.ui_main.trkNowBox.setTitle(QString("No Track Playing"))
        self.ui_main.art_alb["oldart"] = self.ui_main.art_alb["oldalb"] = None
        self.ui_main.xtrawdgt.tray_icon.setToolTip("Stopped")
        
    def __inc_playcount(self):
        """
        Probably better to do this within the database.
        """
        now = self.ui_main.tracking.generate_track("back")
        playcount = int(self.media_db.get_info(unicode(now))[5])
        playcount += 1
        self.media_db.inc_count(playcount, unicode(now))
        
