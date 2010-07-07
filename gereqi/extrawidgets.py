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


from PyQt4.QtGui import *
from PyQt4.QtCore import *

import time

from settings import Settings


class SetupExtraWidgets:
    def __init__(self, parent):
        self.ui_main = parent
        set_db = Settings()
        
        self.__setup_filesystem_tree()
        tray = set_db.get_interface_setting("trayicon")
        if tray == "True":
            self.__create_tray_menu(show=True)
        else:
            self.__create_tray_menu()

        self.__setup_misc()
        self.__key_shortcuts()
        
    def __setup_filesystem_tree(self):
        """
        A filesystem_tree browser where tracks can be (eventually)
        added to the playlist
        """
        self.ui_main.dir_model = QDirModel()
        filters = QDir.Files|QDir.AllDirs|QDir.Readable|QDir.NoDotAndDotDot
        self.ui_main.dir_model.setFilter(filters)
        self.ui_main.dir_model.setReadOnly(True)
        self.ui_main.dir_model.setNameFilters(["*.ogg", "*.flac", "*.mp3",  "*.m4a"])
        self.ui_main.filesystem_tree.setModel(self.ui_main.dir_model) 
        self.ui_main.filesystem_tree.setColumnHidden(1, True)
        self.ui_main.filesystem_tree.setColumnHidden(2, True)
        self.ui_main.filesystem_tree.setColumnHidden(3, True)
        self.ui_main.filesystem_tree.expandToDepth(0)
        
    def __create_tray_menu(self, show=False):
        """
        The tray menu contains shortcuts to features
        in the main UI
        """
        quit_action = QAction(QString("&Quit"), self.ui_main)
        self.ui_main.play_action = QAction(QString("&Play"), self.ui_main)
        next_action = QAction(QString("&Next"), self.ui_main)
        prev_action = QAction(QString("&Previous"), self.ui_main)
        stop_action = QAction(QString("&Stop"), self.ui_main)
        self.ui_main.play_action.setCheckable(True)
        self.ui_main.view_action = QAction(QString("&Visible"), self.ui_main)
        self.ui_main.view_action.setCheckable(True)
        self.ui_main.view_action.setChecked(True)
        tray_icon_menu = QMenu(self.ui_main)
        icon_normal = QIcon(QPixmap(":/Icons/app.png"))
        tray_icon_menu.addAction(icon_normal, QString("Gereqi"))
        tray_icon_menu.addSeparator()
        tray_icon_menu.addAction(prev_action)
        tray_icon_menu.addAction(self.ui_main.play_action)
        tray_icon_menu.addAction(stop_action)
        tray_icon_menu.addAction(next_action)
        tray_icon_menu.addSeparator()
        tray_icon_menu.addAction(self.ui_main.view_action)
        tray_icon_menu.addAction(quit_action)
        self.ui_main.tray_icon = QSystemTrayIcon(self.ui_main)
        icon_stopped = QIcon(QPixmap(":/Icons/app-paused.png"))
        self.ui_main.tray_icon.setIcon(icon_stopped)
        self.ui_main.tray_icon.setContextMenu(tray_icon_menu)
        if show is True:
            self.ui_main.tray_icon.show()
        self.ui_main.tray_icon.setToolTip("Stopped")    
        
        self.ui_main.play_action.toggled.connect(self.ui_main.play_bttn.setChecked)
        self.ui_main.view_action.toggled.connect(self.ui_main.minimise_to_tray)
        self.ui_main.tray_icon.activated.connect(self.ui_main.tray_event)
        next_action.triggered.connect(self.ui_main.next_bttn.click)
        prev_action.triggered.connect(self.ui_main.prev_bttn.click)
        stop_action.triggered.connect(self.ui_main.stop_bttn.click)
        quit_action.triggered.connect(qApp.quit)     
       
    def __setup_misc(self):
        """
        Extra __init__ things to add to the UI
        """        
        self.ui_main.progress_sldr.setPageStep(0)
        self.ui_main.progress_sldr.setSingleStep(0)
        self.ui_main.stat_lbl = QLabel("Finished")
        self.ui_main.stat_prog= QProgressBar()
        self.ui_main.stat_bttn = QToolButton()
        self.ui_main.play_type_bttn = QToolButton()
        icon = QIcon(QPixmap(":/Icons/application-exit.png"))
        self.ui_main.stat_prog.setRange(0, 100)
        self.ui_main.stat_prog.setValue(100)
        self.ui_main.stat_prog.setMaximumSize(QSize(100, 18))
        self.ui_main.stat_bttn.setIcon(icon)
        self.ui_main.stat_bttn.setAutoRaise(True)
        self.ui_main.stat_bttn.setEnabled(False)
        self.ui_main.play_type_bttn.setText("N")
        self.ui_main.play_type_bttn.setCheckable(True)
        self.ui_main.play_type_bttn.setAutoRaise(True)
        self.ui_main.statusBar.addPermanentWidget(self.ui_main.stat_lbl)
        self.ui_main.statusBar.addPermanentWidget(self.ui_main.stat_prog)
        self.ui_main.statusBar.addPermanentWidget(self.ui_main.stat_bttn)
        self.ui_main.statusBar.addPermanentWidget(self.ui_main.play_type_bttn)
        # Headers for the Playlist widget
        headers = [QString("Track"), QString("Title"), QString("Artist"), \
                   QString("Album"), QString("Year"), QString("Genre"),   \
                   QString("Length"), QString("Bitrate"), QString("FileName")]
        for val in range(len(headers)):
            self.ui_main.track_tbl.insertColumn(val)
        self.ui_main.track_tbl.setHorizontalHeaderLabels(headers)
        
        self.ui_main.collect_tree_hdr = self.ui_main.collect_tree.header()
        self.ui_main.collect_tree_hdr.setClickable(True)
        
        # Disables the webView link-clicks as we want to manually handle them
        self.ui_main.info_view.page().setLinkDelegationPolicy(2)
        self.ui_main.wiki_view.page().setLinkDelegationPolicy(2)
        # The images are scaled smoothly using billinear interp and antialias edges of primitives(?)
        self.ui_main.info_view.setRenderHint(1|4)

    def __key_shortcuts(self):
        delete = QShortcut(QKeySequence(QString("Del")), self.ui_main)
        delete.activated.connect(self.ui_main.playlisting.del_track)
        
        
class WidgetManips:
    def __init__(self, parent):
        self.ui_main = parent
        
    def __time_filt_now(self):
        """
        Based on the combobox selection, the collection
        browser is filtered by addition date
        """
        index = self.ui_main.collect_time_box.currentIndex()
        calc = lambda val: int(round(time.time() - val))
        now = time.localtime()
        filts = [(now[3] * now[4]) + now[5], 604800, 2419200, 7257600, 31557600]   
        if index > 0:
            return calc(filts[index - 1])
        
    def setup_db_tree(self):
        """
        viewing the media database in the QTreeView
        """
        media_db = self.ui_main.media_db
        self.ui_main.collect_tree.clear()
        # This gives multiples of the same thing i.e albums
        filt = unicode(self.ui_main.search_collect_edit.text())
        time_filt = self.__time_filt_now()
        
        text_now = unicode(self.ui_main.collect_tree.headerItem().text(0))
        if text_now == "Artist/Album":
            mode = "artist"
        else:
            mode = "album"
                
        if time_filt is None:
            if mode == "artist":
                things = media_db.get_artists()
            elif mode == "album":
                things = media_db.get_albums_all()
        else:
            if mode == "artist":
                things = media_db.get_artists_timed(time_filt)
            elif mode == "album":
                things = media_db.get_albums_all_timed(time_filt)
                
        if things is not None:
            things = sorted(things)
            old_char = None
            char = None
            font = QFont()
            font.setBold(True)
            for cnt in range(len(things)):
                # with sqlite, don't want
                thing = things[cnt]#.decode("utf-8")
                # When creating collection tree only 
                #  allow certain things based on the filter.
                if (filt is not None) and (filt.lower() not in thing.toLower()):
                    continue
                thing = QTreeWidgetItem([thing])
                thing.setChildIndicatorPolicy(0)
                self.ui_main.collect_tree.addTopLevelItem(thing)
            
    def set_play_type(self, checked):
        if checked is True:
            self.ui_main.play_type_bttn.setText("R")
        else:
            self.ui_main.play_type_bttn.setText("N")
            
    def pop_playlist_view(self):
        font = QFont()
        font.setBold(True)        
        self.ui_main.playlist_tree.clear()
        playlists = self.ui_main.media_db.playlist_list()
        #podcasts = None
        #streams = None
        headers = [QTreeWidgetItem(["%s" % tit]) for tit in [
                                    "Podcasts", "Radio Streams",  "Playlists"]]
        for hdr in headers:
            hdr.setFont(0, font)
            hdr.setChildIndicatorPolicy(2)
        
        for cnt in range(3):
            if cnt == 2:
                for play in playlists:
                    now = QTreeWidgetItem([QString(play)])
                    headers[cnt].addChild(now)
                    tracks = self.ui_main.media_db.playlist_tracks(
                                unicode(play))
                    for track in tracks:
                        info = self.ui_main.media_db.get_info(track)
                        now.addChild(QTreeWidgetItem([QString("%s - %s"
                                                    % (info[2], info[1])) ]))       
                                                                                      
            self.ui_main.playlist_tree.addTopLevelItem(headers[cnt])
                
                
    def icon_change(self, state):
        if state == "play":
            icon = QIcon(QPixmap(":/Icons/media-playback-pause.png"))
            tray = QIcon(QPixmap(":/Icons/app.png"))
        elif state == "pause":
            icon = QIcon(QPixmap(":/Icons/media-playback-start.png"))
            tray = QIcon(QPixmap(":/Icons/app-paused.png"))

        self.ui_main.play_bttn.setIcon(icon)
        self.ui_main.tray_icon.setIcon(tray)
