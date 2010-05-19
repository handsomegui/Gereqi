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


from PyQt4.QtGui import QSystemTrayIcon, QIcon, QTreeWidgetItem, \
QPixmap, QFont, QShortcut, QKeySequence, QLabel, QProgressBar, \
QToolButton, QAction, QSystemTrayIcon, qApp, QDirModel, QMenu
from PyQt4.QtCore import QString, SIGNAL, SLOT, QDir, QSize, QObject

from database import Media


class SetupExtraWidgets:
    def __init__(self, parent):
        # Basically,the parent.
        self.ui_main = parent
        self.__setup_filesystem_tree()
        self.__create_tray_menu()
        self.__playlist_add_menu()
        self.__disable_tabs()
        self.__setup_misc()
        self.__key_shortcuts()
        
    def __setup_filesystem_tree(self):
        """
        A filesystem_tree browser where tracks can be (eventually)
        added to the playlist
        """
        self.dir_model = QDirModel()
        filters = QDir.Files|QDir.AllDirs|QDir.Readable|QDir.NoDotAndDotDot
        self.dir_model.setFilter(filters)
        self.dir_model.setReadOnly(True)
        self.dir_model.setNameFilters(["*.ogg", "*.flac", "*.mp3",  "*.m4a"])
        self.ui_main.filesystem_tree.setModel(self.dir_model) 
        self.ui_main.filesystem_tree.setColumnHidden(1, True)
        self.ui_main.filesystem_tree.setColumnHidden(2, True)
        self.ui_main.filesystem_tree.setColumnHidden(3, True)
        self.ui_main.filesystem_tree.expandToDepth(0)
        
    def __create_tray_menu(self):
        """
        The tray menu contains shortcuts to features
        in the main UI
        """
        quit_action = QAction(QString("&Quit"), self.ui_main)
        self.play_action = QAction(QString("&Play"), self.ui_main)
        next_action = QAction(QString("&Next"), self.ui_main)
        prev_action = QAction(QString("&Previous"), self.ui_main)
        stop_action = QAction(QString("&Stop"), self.ui_main)
        self.play_action.setCheckable(True)
        self.view_action = QAction(QString("&Visible"), self.ui_main)
        self.view_action.setCheckable(True)
        self.view_action.setChecked(True)
        tray_icon_menu = QMenu(self.ui_main)
        icon_normal = QIcon(QPixmap(":/Icons/app.png"))
        tray_icon_menu.addAction(icon_normal, QString("Gereqi"))
        tray_icon_menu.addSeparator()
        tray_icon_menu.addAction(prev_action)
        tray_icon_menu.addAction(self.play_action)
        tray_icon_menu.addAction(stop_action)
        tray_icon_menu.addAction(next_action)
        tray_icon_menu.addSeparator()
        tray_icon_menu.addAction(self.view_action)
        tray_icon_menu.addAction(quit_action)
        self.tray_icon = QSystemTrayIcon(self.ui_main)
        icon_stopped = QIcon(QPixmap(":/Icons/app-paused.png"))
        self.tray_icon.setIcon(icon_stopped)
        self.tray_icon.setContextMenu(tray_icon_menu)
        self.tray_icon.show()
        self.tray_icon.setToolTip("Stopped")    
        
        QObject.connect(self.play_action, SIGNAL("toggled(bool)"), 
                        self.ui_main.play_bttn, SLOT("setChecked(bool)"))
        QObject.connect(next_action, SIGNAL("triggered()"),
                        self.ui_main.next_bttn, SLOT("click()"))
        QObject.connect(prev_action, SIGNAL("triggered()"), 
                        self.ui_main.prev_bttn, SLOT("click()"))
        QObject.connect(stop_action, SIGNAL("triggered()"), 
                        self.ui_main.stop_bttn, SLOT("click()"))
        QObject.connect(self.view_action, SIGNAL("toggled(bool)"), 
                        self.ui_main.minimise_to_tray)  
        QObject.connect(quit_action, SIGNAL("triggered()"), 
                        qApp, SLOT("quit()"))
        QObject.connect(self.tray_icon, 
                        SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), 
                        self.ui_main.tray_event)
     
    def __playlist_add_menu(self):
        """
        In the 'playlist' tab a menu is required for
        the 'add' button
        """
        menu = QMenu(self.ui_main)
        playlist_menu = QMenu(self.ui_main)
        playlist_menu.setTitle(QString("Playlist"))
        new = QAction(QString("New..."), self.ui_main)
        existing = QAction(QString("Import Existing..."), self.ui_main)
        playlist_menu.addAction(new)
        playlist_menu.addAction(existing)        
        menu.addMenu(playlist_menu)
        smart = QAction(QString("Smart Playlist..."), self.ui_main)
        dynamic = QAction(QString("Dynamic Playlist..."), self.ui_main)
        radio = QAction(QString("Radio Stream..."), self.ui_main)
        podcast = QAction(QString("Podcast..."), self.ui_main)
        menu.addAction(smart)
        menu.addAction(dynamic)
        menu.addAction(radio)
        menu.addAction(podcast)
        self.ui_main.add_playlist_bttn.setMenu(menu)
        
    def __disable_tabs(self):
        self.ui_main.horizontal_tabs.setTabEnabled(1, False)
        self.ui_main.horizontal_tabs.setTabEnabled(2, False)
        self.ui_main.vertical_tabs.setTabEnabled(3, False)
        
    def __setup_misc(self):
        """
        Extra __init__ things to add to the UI
        """        
        self.ui_main.progress_sldr.setPageStep(0)
        self.ui_main.progress_sldr.setSingleStep(0)
        self.stat_lbl = QLabel("Finished")
        self.stat_prog = QProgressBar()
        self.stat_bttn = QToolButton()
        self.play_type_bttn = QToolButton()
        icon = QIcon(QPixmap(":/Icons/application-exit.png"))
        self.stat_prog.setRange(0, 100)
        self.stat_prog.setValue(100)
        self.stat_prog.setMaximumSize(QSize(100, 18))
        self.stat_bttn.setIcon(icon)
        self.stat_bttn.setAutoRaise(True)
        self.stat_bttn.setEnabled(False)
        self.play_type_bttn.setText("N")
        self.play_type_bttn.setCheckable(True)
        self.play_type_bttn.setAutoRaise(True)
        self.ui_main.statusBar.addPermanentWidget(self.stat_lbl)
        self.ui_main.statusBar.addPermanentWidget(self.stat_prog)
        self.ui_main.statusBar.addPermanentWidget(self.stat_bttn)
        self.ui_main.statusBar.addPermanentWidget(self.play_type_bttn)
        # Headers for the Playlist widget
        headers = [QString("Track"), QString("Title"), QString("Artist"), \
                   QString("Album"), QString("Year"), QString("Genre"),   \
                   QString("Length"), QString("Bitrate"), QString("FileName")]
        for val in range(len(headers)):
            self.ui_main.track_tbl.insertColumn(val)
        self.ui_main.track_tbl.setHorizontalHeaderLabels(headers)
        
        self.ui_main.collect_tree_hdr = self.ui_main.collect_tree.header()
        self.ui_main.collect_tree_hdr.setClickable(True)

    def __key_shortcuts(self):
        delete = QShortcut(QKeySequence(QString("Del")), self.ui_main)
        QObject.connect(delete, SIGNAL("activated()"), 
                        self.ui_main.playlisting.del_track)   
        
        
class WidgetManips:
    def __init__(self, parent):
        self.ui_main = parent
        
    def setup_db_tree(self, filt=None, time_filt=None, mode=None):
        """
        viewing the media database in the QTreeView
        """
        media_db = Media()
        self.ui_main.collect_tree.clear()
        # This gives multiples of the same thing i.e albums
            
        if mode is None:
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
                things = media_db.get_artists(time_filt)
            elif mode == "album":
                things = media_db.get_albums_all_timed(time_filt)
                
        things = sorted(things)
        old_char = None
        char = None
        font = QFont()
        font.setBold(True)
        for cnt in range(len(things)):
            thing = things[cnt]
            # When creating collection tree only 
            #  allow certain things based on the filter.
            if (filt is not None) and (filt.lower() not in thing.lower()):
                continue
            thing = QTreeWidgetItem([QString(thing)])
            thing.setChildIndicatorPolicy(0)
            self.ui_main.collect_tree.addTopLevelItem(thing)
            
    def set_play_type(self, checked):
        if checked is True:
            self.ui_main.xtrawdgt.play_type_bttn.setText("R")
        else:
            self.ui_main.xtrawdgt.play_type_bttn.setText("N")
            
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
        self.ui_main.xtrawdgt.tray_icon.setIcon(tray)
