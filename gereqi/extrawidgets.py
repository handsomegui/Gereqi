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
import gereqi.devices


class SetupExtraWidgets:
    """
    This should be done before the main ui is shown
    """
    def __init__(self, parent):
        self.ui_main = parent
        self.dev_man = gereqi.devices.Devices()
        
        self.__setup_filesystem_tree()
        self.__create_tray_menu()

        self.__setup_misc()
        self.__key_shortcuts()
        self.__icons()
        self.pop_devs()
        
    def __setup_filesystem_tree(self):
        """
        A filesystem_tree browser where tracks can be (eventually)
        added to the playlist
        """
        self.ui_main.dir_model = QDirModel()
        filters = QDir.Files|QDir.AllDirs|QDir.Readable|QDir.NoDotAndDotDot
        self.ui_main.dir_model.setFilter(filters)
        self.ui_main.dir_model.setReadOnly(True)
        self.ui_main.dir_model.setNameFilters(["*.ogg", "*.flac", "*.mp3", 
                                               "*.m4a"])
        self.ui_main.filesystem_tree.setModel(self.ui_main.dir_model) 
        self.ui_main.filesystem_tree.setColumnHidden(1, True)
        self.ui_main.filesystem_tree.setColumnHidden(2, True)
        self.ui_main.filesystem_tree.setColumnHidden(3, True)
        self.ui_main.filesystem_tree.expandToDepth(0)
        
    def __create_tray_menu(self):
        """
        The tray menu contains shortcuts to features
        in the main UI
        """
        quit_action = QAction(QIcon().fromTheme("process-stop"),
                              QString("&Quit"), self.ui_main)
        self.ui_main.play_action = QAction(QIcon().fromTheme("media-playback-start"),
                                           QString("&Play"), self.ui_main)
        next_action = QAction(QIcon().fromTheme("media-skip-forward"),
                              QString("&Next"), self.ui_main)
        prev_action = QAction(QIcon().fromTheme("media-skip-backward"),
                              QString("&Previous"), self.ui_main)
        stop_action = QAction(QIcon().fromTheme("media-playback-stop"),
                              QString("&Stop"), self.ui_main)
        self.ui_main.play_action.setCheckable(True)
        self.ui_main.view_action = QAction(QString("&Visible"), self.ui_main)
        self.ui_main.view_action.setCheckable(True)
        self.ui_main.view_action.setChecked(True)
        tray_menu = QMenu(self.ui_main)
        icon_normal = QIcon("gereqi/icons/app.png")
        tray_menu.addAction(icon_normal, QString("Gereqi"))
        tray_menu.addSeparator()
        tray_menu.addAction(prev_action)
        tray_menu.addAction(self.ui_main.play_action)
        tray_menu.addAction(stop_action)
        tray_menu.addAction(next_action)
        tray_menu.addSeparator()
        tray_menu.addAction(self.ui_main.view_action)
        tray_menu.addAction(quit_action)
        self.ui_main.tray_icon = QSystemTrayIcon(self.ui_main)
        icon_stopped = QIcon("gereqi/icons/app-paused.png")
        self.ui_main.tray_icon.setIcon(icon_stopped)
        self.ui_main.tray_icon.setContextMenu(tray_menu)
        self.ui_main.tray_icon.setToolTip("Stopped")    
        
        self.ui_main.play_action.toggled.connect(self.ui_main.play_bttn.setChecked)
        self.ui_main.view_action.toggled.connect(self.ui_main.minimise_to_tray)
        self.ui_main.tray_icon.activated.connect(self.ui_main.tray_event)
        next_action.triggered.connect(self.ui_main.next_bttn.click)
        prev_action.triggered.connect(self.ui_main.prev_bttn.click)
        stop_action.triggered.connect(self.ui_main.stop_bttn.click)
        quit_action.triggered.connect(qApp.quit)     
       
    # TODO: separate certain things
    def __setup_misc(self):
        """
        Extra __init__ things to add to the UI
        """        
        self.ui_main.progress_sldr.setPageStep(0)
        self.ui_main.progress_sldr.setSingleStep(0)
        self.ui_main.stat_lbl = QLabel("Finished")
        self.ui_main.stat_prog = QProgressBar()
        
        self.ui_main.stat_prog.setRange(0, 100)
        self.ui_main.stat_prog.setValue(100)
        self.ui_main.stat_prog.setMaximumSize(QSize(100, 18))
        
        
        self.ui_main.stat_bttn = QToolButton()
        self.ui_main.stat_bttn.setIcon(QIcon().fromTheme("application-exit"))
        self.ui_main.stat_bttn.setAutoRaise(True)
        self.ui_main.stat_bttn.setEnabled(False)
        
        self.ui_main.play_type_bttn = QToolButton()  
        self.ui_main.play_type_bttn.setCheckable(True)
        self.ui_main.play_type_bttn.setAutoRaise(True)
        self.ui_main.play_type_bttn.setIcon(QIcon("gereqi/icons/dice-icon2.png"))
        self.ui_main.play_type_bttn.toggled.connect(self.__mode_change)
        
        self.ui_main.statusBar.addPermanentWidget(self.ui_main.stat_lbl)
        self.ui_main.statusBar.addPermanentWidget(self.ui_main.stat_prog)
        self.ui_main.statusBar.addPermanentWidget(self.ui_main.stat_bttn)
        self.ui_main.statusBar.addPermanentWidget(self.ui_main.play_type_bttn)
        # Headers for the Playlist widget
        headers = [QString("Track"), QString("Title"), QString("Artist"),
                   QString("Album"), QString("Year"), QString("Genre"),  
                   QString("Length"), QString("Bitrate"), QString("FileName")]
        for val in range(len(headers)):
            self.ui_main.track_tbl.insertColumn(val)
        self.ui_main.track_tbl.setHorizontalHeaderLabels(headers)
        
        self.ui_main.collect_tree_hdr = self.ui_main.collect_tree.header()
        self.ui_main.collect_tree_hdr.setClickable(True)
        
        
        # Disables the webView link-clicks as we want to manually handle them
        self.ui_main.info_view.page().setLinkDelegationPolicy(2)
        self.ui_main.wiki_view.page().setLinkDelegationPolicy(2)
        
        # FIXME: will not work in PyQT <4.6 i.e. Ubuntu 9.10
        # The images are scaled smoothly using billinear interp and 
        # antialias edges of primitives(?)
        try:
            self.ui_main.info_view.setRenderHint(1|4)
        except AttributeError,e:
            print('''WARNING: it's likely you are using an old\n
            version of PyQt4 which lacks the option to antialias\n
            This means cover art will look rubbish.\n
            Full error:- %s''' % e)

    def __key_shortcuts(self):
        """
        various keyboard shortcuts 
        """
        # remove the selected track from the playlist
        delete = QShortcut(QKeySequence(QString("Del")), self.ui_main)
        delete.activated.connect(self.ui_main.playlisting.del_track)
        
    def __mode_change(self, check):
        """
        Changes the icon of the random mode button depending
        if checked or not
        """
        if check:
            icon = QIcon("gereqi/icons/dice-icon.png")
        else:
            icon = QIcon("gereqi/icons/dice-icon2.png")            
        self.ui_main.play_type_bttn.setIcon(icon)
        
        
    def __icons(self):
        """
        Using the theme's icons
        """
        self.ui_main.clear_collect_bttn.setIcon(QIcon().fromTheme("edit-clear"))
        self.ui_main.clear_search_bttn.setIcon(QIcon().fromTheme("edit-clear"))
        self.ui_main.clear_trktbl_bttn.setIcon(QIcon().fromTheme("window-new"))
        self.ui_main.save_trktbl_bttn.setIcon(QIcon().fromTheme("document-save-as"))
        self.ui_main.prev_trktbl_bttn.setIcon(QIcon().fromTheme("edit-undo"))
        self.ui_main.next_trktbl_bttn.setIcon(QIcon().fromTheme("edit-redo"))
        
        self.ui_main.prev_bttn.setIcon(QIcon().fromTheme("media-skip-backward"))
        self.ui_main.play_bttn.setIcon(QIcon().fromTheme("media-playback-start"))
        self.ui_main.stop_bttn.setIcon(QIcon().fromTheme("media-playback-stop"))
        self.ui_main.next_bttn.setIcon(QIcon().fromTheme("media-skip-forward"))   
        
        self.ui_main.rename_playlist_bttn.setIcon(QIcon().fromTheme("edit-rename")) # NONSTD
        self.ui_main.delete_playlist_bttn.setIcon(QIcon().fromTheme("edit-delete")) # NONSTD
        
        app_icon = QIcon("gereqi/icons/app.png")
        self.ui_main.setWindowIcon(app_icon)
        
        self.ui_main.mute_bttn.setIcon(QIcon().fromTheme("player-volume"))
        
        
    def __dev_view_expand(self,item):
        par = item.parent()
        if not par:
            artist = str(item.text(0))
            if item.childCount() > 0:
                return
            albums = self.dev_interface.albums(artist)
            for alb in albums:
                now = QTreeWidgetItem([alb])
                now.setChildIndicatorPolicy(0)
                item.addChild(now)
            return
            
        elif not par.parent():
            artist = str(par.text(0))
            album = str(item.text(0))
            if item.childCount() > 0:
                return
            
            tracks = self.dev_interface.tracks(artist,album)
            for trk in tracks:
                now = QTreeWidgetItem([trk])
                now.setChildIndicatorPolicy(1)
                item.addChild(now)
            return
            
        
    def __add_from_dev(self, item):
        self.__dev_view_expand(item)
        par = item.parent()
        if not par:
            art = str(item.text(0))
            tracks = self.dev_interface.filename(artist=art)
            # List comps or generators are very,very flakey
            for trk in tracks:
                info = self.dev_interface.metadata(trk)
                self.ui_main.playlisting.add_to_playlist(trk,info)
            return
        
        par_par = par.parent()
        if not par_par:
            art = str(par.text(0))
            alb = str(item.text(0))
            tracks = self.dev_interface.filename(artist=art,album=alb)
            for trk in tracks:
                info = self.dev_interface.metadata(trk)
                self.ui_main.playlisting.add_to_playlist(trk,info)
                
        else:
            artist = str(par_par.text(0))
            album = str(par.text(0))
            title = str(item.text(0))
            track = self.dev_interface.filename(artist, album, title)
            info = self.dev_interface.metadata(track)
            self.ui_main.playlisting.add_to_playlist(track,info)
            
            
        
    def __pop_dev_view(self):
        arts = self.dev_interface.artists()
        for art in arts:
            row = QTreeWidgetItem([art])
            row.setChildIndicatorPolicy(0)
            self.ui_main.device_view.addTopLevelItem(row)
        
        
    def __ipod_view(self,m_point):
        self.ui_main.device_view.clear()
        self.dev_interface = gereqi.devices.Ipod(m_point)
        self.__pop_dev_view()
        
        
    def __mount_dev(self):
        dev_now = str(self.ui_main.devices_box.currentText())
        m_point = self.dev_man.mount(dev_now)
        for dev in self.dev_man.device_list:
            if (dev["PATH"] != dev_now):
                continue
            
            dev["MOUNTPOINT"] = m_point
            if (dev["PROTOCOL"] == "ipod"):
                self.__ipod_view(m_point)
                return
        
    def __umount_dev(self):
        dev = str(self.ui_main.devices_box.currentText())
        self.dev_man.unmount(dev)
        self.ui_main.device_view.clear()
        
        
    def pop_devs(self):
        self.ui_main.connect_dev.clicked.connect(self.__mount_dev)
        self.ui_main.disconnect_dev.clicked.connect(self.__umount_dev)
        self.ui_main.device_view.itemExpanded.connect(self.__dev_view_expand)
        self.ui_main.device_view.itemDoubleClicked.connect(self.__add_from_dev)
        for dev in self.dev_man.device_list:
            self.ui_main.devices_box.addItem(dev["PATH"])
        

   
class WidgetManips:
    """
    For repeated custom widget actions
    """
    def __init__(self, parent):
        parent.track_tbl.setContextMenuPolicy(Qt.CustomContextMenu)
        parent.track_tbl.customContextMenuRequested.connect(self.__context_menu)
        
        self.ui_main = parent
        
    def __context_menu(self,pos):
        # do nothing if table is empty
        if self.ui_main.track_tbl.rowCount() > 0:
            menu = QMenu()
            play_action = menu.addAction(QIcon().fromTheme("media-playback-start"),
                                         "Play")
            menu.addSeparator()
            manage_action = menu.addAction(QIcon().fromTheme("document-open"),
                                           "Manage File")
            copy_tags_action = menu.addAction(QIcon().fromTheme("edit-copy"),
                                              "Copy Tags to Clipboard")
            edit_action = menu.addAction("Edit Track Information")
            
            action = menu.exec_(self.ui_main.track_tbl.mapToGlobal(pos))

            print "CONTEXT MENU",pos,action
        
    def __time_filt_now(self):
        """
        Based on the combobox selection, the collection
        browser is filtered by addition date
        """
        index = self.ui_main.collect_time_box.currentIndex()
        calc = lambda val: int(round(time.time() - val))
        now = time.localtime()
        today = ((now[3] * 60) +  now[4] ) * 60 + now[5]
        filts = [today, 604800, 2629743, 7889229, 31556926]   
        if index > 0:
            return calc(filts[index - 1])
        else:
            return 0
        
    def setup_db_tree(self):
        """
        viewing the media database in the QTreeView
        """
        media_db = self.ui_main.media_db
        self.ui_main.collect_tree.clear()
        # This gives multiples of the same thing i.e albums
        filt = self.ui_main.search_collect_edit.text()
        time_filt = self.__time_filt_now()
        
        text_now = self.ui_main.collect_tree.headerItem().text(0)
        if text_now == "Artist/Album":
            mode = "artist"
        else:
            mode = "album"
                
        if mode == "artist":
            things = media_db.get_artists(time_filt)
        elif mode == "album":
            things = media_db.get_albums_all(time_filt)
        
        # FIXME: UGLY!!!!
        if things is not None:
            for cnt in range(len(things)):
                thing = things[cnt]
                # When creating collection tree only 
                #  allow certain things based on the filter.
                if (filt is not None) and (filt.toLower() not in thing.toLower()):
                    continue
                thing = QTreeWidgetItem([thing])
                thing.setChildIndicatorPolicy(0)
                self.ui_main.collect_tree.addTopLevelItem(thing)
            
    def pop_playlist_view(self):
        """
        Populates the playlist listview
        """
        font = QFont()
        font.setBold(True)        
        self.ui_main.playlist_tree.clear()
        playlists = self.ui_main.media_db.playlist_list()
#        podcasts = None
#        streams = None
        headers = [QTreeWidgetItem(["%s" % tit]) for tit in [
                                    "Podcasts", "Radio Streams",  "Playlists"]]
        for hdr in headers:
            hdr.setFont(0, font)
            hdr.setChildIndicatorPolicy(2)
        
        for cnt in range(3):
            if cnt == 2:
                for play in playlists:
                    # Ignore the auto-save playlist
                    if play == "!!##gereqi.remembered##!!":
                        continue
                    now = QTreeWidgetItem([QString(play)])
                    headers[cnt].addChild(now)
                    tracks = self.ui_main.media_db.playlist_tracks(play)
                    for track in tracks:
                        info = self.ui_main.media_db.get_info(track)
                        if info is not None:
                            now.addChild(QTreeWidgetItem([QString("%s - %s" %
                                         (info["title"], info["artist"])) ]))       
                                                                                      
            self.ui_main.playlist_tree.addTopLevelItem(headers[cnt])
                
    def icon_change(self, state):
        """
        Depending on the specific state of the program
        the play button's icon will vary
        """
        if state == "play":
            icon = QIcon().fromTheme("media-playback-pause")
            tray = QIcon("gereqi/icons/app.png")
        elif state == "pause":            
            icon = QIcon().fromTheme("media-playback-start")
            tray = QIcon("gereqi/icons/app-paused.png")

        self.ui_main.play_bttn.setIcon(icon)
        self.ui_main.tray_icon.setIcon(tray)
