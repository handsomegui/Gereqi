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
import gereqi.icons.configuration
import gereqi.icons.icons_resource

class MyDelegate(QItemDelegate):
    mode = "artist"
    def __init__(self):
        super(MyDelegate,self).__init__()
        
    def sizeHint(self,option,index):
        parent = index.parent()
        if parent.isValid() and  not parent.parent().isValid():
            if self.mode == "artist":
                return QSize(48,48)
            else:
                return QSize(24,24)
            
        if self.mode == "artist":
            return QSize(24,24)
        else:
            return QSize(48,48)
            
    

class SetupExtraWidgets:
    """
    This should be done before the main ui is shown
    e.g. on app initialisation
    """
    def __init__(self, parent):
        self.ui = parent
        

        
        self.ui.track_tbl.horizontalHeader().setMovable(True)
        
        self.__setup_filesystem_tree()
        self.__create_tray_menu()
        

        self.__setup_misc()
        self.__key_shortcuts()
        # Load all the button/action icons
        gereqi.icons.configuration.Setup(self.ui)
        
    def __setup_filesystem_tree(self):
        """
        A filesystem_tree browser where tracks can be (eventually)
        added to the playlist
        """
        self.ui.dir_model = QDirModel()
        filters = QDir.Files|QDir.AllDirs|QDir.Readable|QDir.NoDotAndDotDot
        self.ui.dir_model.setFilter(filters)
        self.ui.dir_model.setReadOnly(True)
        self.ui.dir_model.setNameFilters(self.ui.format_filter)
        self.ui.filesystem_tree.setModel(self.ui.dir_model) 
        self.ui.filesystem_tree.setColumnHidden(1, True)
        self.ui.filesystem_tree.setColumnHidden(2, True)
        self.ui.filesystem_tree.setColumnHidden(3, True)
        self.ui.filesystem_tree.expandToDepth(0)
        
    def __create_tray_menu(self):
        """
        The tray menu contains shortcuts to features
        in the main UI
        """
        #FIXME: the icons do not show in Ubuntu
        icon = QIcon().fromTheme("process-stop")
        quit_action = QAction(icon, QString("&Quit"), self.ui)
        
        icon = QIcon().fromTheme("media-playback-start", QIcon(":/icons/media-playback-start.png"))
        self.ui.play_action = QAction(icon, QString("&Play"), self.ui)
        
        icon = QIcon().fromTheme("media-skip-forward", QIcon(":/icons/media-skip-forward.png"))
        next_action = QAction(icon, QString("&Next"), self.ui)
        
        icon = QIcon().fromTheme("media-skip-backward", QIcon(":/icons/media-skip-backward.png"))
        prev_action = QAction(icon, QString("&Previous"), self.ui)
        
        icon = QIcon().fromTheme("media-playback-stop", QIcon(":/icons/media-playback-stop.png"))
        stop_action = QAction(icon, QString("&Stop"), self.ui)
        
        self.ui.play_action.setCheckable(True)
        self.ui.view_action = QAction(QString("&Visible"), self.ui)
        self.ui.view_action.setCheckable(True)
        self.ui.view_action.setChecked(True)
        tray_menu = QMenu(self.ui)
        tray_menu.addAction(QIcon(":/icons/app.png"), QString("Gereqi"))
        tray_menu.addSeparator()
        tray_menu.addAction(prev_action)
        tray_menu.addAction(self.ui.play_action)
        tray_menu.addAction(stop_action)
        tray_menu.addAction(next_action)
        tray_menu.addSeparator()
        tray_menu.addAction(self.ui.view_action)
        tray_menu.addAction(quit_action)
        self.ui.tray_icon = QSystemTrayIcon(self.ui)
        self.ui.tray_icon.setIcon(QIcon(":/icons/app-paused.png"))
        self.ui.tray_icon.setContextMenu(tray_menu)
        self.ui.tray_icon.setToolTip("Stopped")    
        
        self.ui.play_action.toggled.connect(self.ui.play_bttn.setChecked)
        self.ui.view_action.toggled.connect(self.ui.minimise_to_tray)
        self.ui.tray_icon.activated.connect(self.ui.tray_event)
        next_action.triggered.connect(self.ui.next_bttn.click)
        prev_action.triggered.connect(self.ui.prev_bttn.click)
        stop_action.triggered.connect(self.ui.stop_bttn.click)
        quit_action.triggered.connect(qApp.quit)     
       
    def __setup_misc(self):
        """
        Extra __init__ things to add to the UI
        """
        self.ui.stat_lbl = QLabel("Finished")
        self.ui.stat_prog = QProgressBar()
        
        self.ui.stat_prog.setRange(0, 100)
        self.ui.stat_prog.setValue(100)
        self.ui.stat_prog.setMaximumSize(QSize(100, 18))
        
        
        self.ui.stat_bttn = QToolButton()
        self.ui.stat_bttn.setIcon(QIcon().fromTheme("application-exit"))
        self.ui.stat_bttn.setAutoRaise(True)
        self.ui.stat_bttn.setEnabled(False)
        
        self.ui.play_type_bttn = QToolButton()  
        self.ui.play_type_bttn.setCheckable(True)
        self.ui.play_type_bttn.setAutoRaise(True)
        self.ui.play_type_bttn.setIcon(QIcon(":/icons/dice-icon2.png"))
        
        self.ui.statusBar.addPermanentWidget(self.ui.stat_lbl)
        self.ui.statusBar.addPermanentWidget(self.ui.stat_prog)
        self.ui.statusBar.addPermanentWidget(self.ui.stat_bttn)
        self.ui.statusBar.addPermanentWidget(self.ui.play_type_bttn)
        # Headers for the Playlist widget
        headers = [QString("Track"), QString("Title"), QString("Artist"),
                   QString("Album"), QString("Year"), QString("Genre"),  
                   QString("Length"), QString("Bitrate"), QString("FileName")]
        for val in range(len(headers)):
            self.ui.track_tbl.insertColumn(val)
        self.ui.track_tbl.setHorizontalHeaderLabels(headers)
        
        self.ui.collect_tree_hdr = self.ui.collect_tree.header()
        self.ui.collect_tree_hdr.setClickable(True)
        
        
        # Disables the webView link-clicks as we want to manually handle them
        self.ui.info_view.page().setLinkDelegationPolicy(2)
        self.ui.wiki_view.page().setLinkDelegationPolicy(2)
        
        # FIXME: will not work in PyQT <4.6 i.e. Ubuntu 9.10
        # The images are scaled smoothly using billinear interp and 
        # antialias edges of primitives(?)
        try:
            self.ui.info_view.setRenderHint(1|4)
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
        delete = QShortcut(QKeySequence(QString("Del")), self.ui)
        delete.activated.connect(self.ui.playlisting.del_tracks)
        

        

class WidgetManips:
    """
    For repeated custom widget actions
    """
    def __init__(self, parent):
        parent.track_tbl.setContextMenuPolicy(Qt.CustomContextMenu)
        parent.track_tbl.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        
        parent.track_tbl.customContextMenuRequested.connect(self.__context_menu)
        parent.track_tbl.horizontalHeader().customContextMenuRequested.connect(self.__header_menu)
        parent.vertical_tabs.currentChanged.connect(self.__tab_changed)
        parent.play_type_bttn.toggled.connect(self.__play_mode_changed)
        self.__hdr_menu_setup()
        self.ui = parent
        self.dev_man = None
        
        self.mydel = MyDelegate()
        self.mydel.mode = "artist"
        self.ui.collect_tree.setItemDelegate(self.mydel)
        self.ui.collect_tree.setUniformRowHeights(False)
        self.ui.collect_tree.setIconSize(QSize(46,46))
        
        
    def __play_mode_changed(self, check):
        """
        Changes the icon of the random mode button depending
        if checked or not
        """
        if check:
            icon = QIcon(":/icons/dice-icon.png")
        else:
            icon = QIcon(":/icons/dice-icon2.png")            
        self.ui.play_type_bttn.setIcon(icon)
        
        
    def __add_from_dev(self, item):
        self.__dev_view_expand(item)
        par = item.parent()
        if not par:
            art = str(item.text(0))
            tracks = self.dev_interface.filename(artist=art)
            # List comps or generators are very,very flakey
            for trk in tracks:
                info = self.dev_interface.metadata(trk)
                self.ui.playlisting.add_to_playlist(trk,info)
            return
        
        par_par = par.parent()
        if not par_par:
            art = str(par.text(0))
            alb = str(item.text(0))
            tracks = self.dev_interface.filename(artist=art,album=alb)
            for trk in tracks:
                info = self.dev_interface.metadata(trk)
                self.ui.playlisting.add_to_playlist(trk,info)
                
        else:
            artist = str(par_par.text(0))
            album = str(par.text(0))
            title = str(item.text(0))
            track = self.dev_interface.filename(artist, album, title)
            info = self.dev_interface.metadata(track)
            self.ui.playlisting.add_to_playlist(track,info)
        
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
        
    def __hdr_menu_setup(self):
        """
            Setup the Context Menu for the table headers.
            Needed to keep the checkbox states
        """        
        self.hdr_menu = QMenu()
        hdrs = ["Track","Title","Artist","Album","Year","Genre","Length",
                "Bitrate","FileName"]
        for hdr in hdrs:
            action = self.hdr_menu.addAction(hdr)
            action.setCheckable(True)
            action.setChecked(True)
        
    def __header_menu(self,pos): 
        """
            The names of each header column is checkable
            for viewing of its column
        """
        action = self.hdr_menu.exec_(self.ui.track_tbl.horizontalHeader().mapToGlobal(pos))
        hdr_pos = self.ui.playlisting.header_search(action.iconText())
        hdr_view = False if action.isChecked() else True
        self.ui.track_tbl.setColumnHidden(hdr_pos,hdr_view)
        
    def __tab_changed(self,pos):
        if (pos == 4):
            if not self.dev_man:
                self.dev_man = gereqi.devices.Devices()
                
            self.ui.connect_dev.clicked.connect(self.__mount_dev)
            self.ui.disconnect_dev.clicked.connect(self.__umount_dev)
            self.ui.device_view.itemExpanded.connect(self.__dev_view_expand)
            self.ui.device_view.itemDoubleClicked.connect(self.__add_from_dev)
            for dev in self.dev_man.device_list:
                self.ui.devices_box.addItem(dev["PATH"])
                
                
    def __pop_dev_view(self):
        """
            Populate the treeView based on the
            currently mounted device
        """
        arts = self.dev_interface.artists()
        for art in arts:
            row = QTreeWidgetItem([art])
            row.setChildIndicatorPolicy(0)
            self.ui.device_view.addTopLevelItem(row)
        
    def __ipod_view(self,m_point):
        """
            Shows the iPods contents in the treeview
        """
        self.ui.device_view.clear()
        self.dev_interface = gereqi.devices.Ipod(m_point)
        self.__pop_dev_view()
        
    def __mount_dev(self):
        """
            Mount the device shown in the combobox
        """
        dev_now = str(self.ui.devices_box.currentText())
        m_point = self.dev_man.mount(dev_now)
        self.ui.connect_dev.setEnabled(False)
        self.ui.disconnect_dev.setEnabled(True)
        for dev in self.dev_man.device_list:
            if (dev["PATH"] != dev_now):
                continue
            
            dev["MOUNTPOINT"] = m_point
            if (dev["PROTOCOL"] == "ipod"):
                self.__ipod_view(m_point)
                return
        
    def __umount_dev(self):
        """
            Unmount current device
        """
        dev = str(self.ui.devices_box.currentText())
        self.dev_man.unmount(dev)
        self.ui.device_view.clear()
        self.ui.disconnect_dev.setEnabled(False)
        self.ui.connect_dev.setEnabled(True)
        
    def __context_menu(self,pos):
        # do nothing if table is empty
        if self.ui.track_tbl.rowCount() > 0:
            item_now = self.ui.track_tbl.itemAt(pos)
            col_now = self.ui.track_tbl.column(item_now)
            tag_name = self.ui.track_tbl.horizontalHeaderItem(col_now).text()
            
            menu = QMenu()
            icon = QIcon().fromTheme("media-playback-start")
            play_action = menu.addAction(icon, "Play")
            menu.addSeparator()
            
            remove_action = menu.addAction("Remove From Playlist")
            
            menu.addSeparator()
            
            icon = QIcon().fromTheme("document-open")
            manage_menu = QMenu("Manage File")
            manage_menu.setIcon(icon)
            manage_organise = manage_menu.addAction("Organise File")
            manage_delete = manage_menu.addAction("Delete File")
            
            menu.addMenu(manage_menu)
            
            icon = QIcon().fromTheme("edit-copy", QIcon(":/icon/edit-copy.png"))
            # Can't change these aspects of the file
            copy_tags_action = menu.addAction(icon, "Copy Tags to Clipboard")
            if tag_name not in ["FileName","Length", "Bitrate"]:
                edit_tag = menu.addAction("Edit Tag '%s'" % tag_name)
            
            action = menu.exec_(self.ui.track_tbl.mapToGlobal(pos))
            if not action:
                return
                        
            row = item_now.row()
            
            if action == play_action:
                # Stop playback then start again 
                self.ui.play_bttn.setChecked(False)
                self.ui.play_bttn.setChecked(True)
                
            # Honestly, I have no idea what use this is. 
            # At least it's easy to implement
            elif action == copy_tags_action:
                row = self.ui.track_tbl.itemAt(pos).row()
                col = self.ui.playlisting.header_search("Title")
                tag = self.ui.track_tbl.item(row,col).text()
                clip = QApplication.clipboard()
                clip.setText(tag)
                
            elif action == remove_action:
                self.ui.playlisting.del_track(row)
                
            elif action == manage_organise:
                print "ORGANISE?"
                
            elif action == manage_delete:
                print "YEAH, I'M NOT DELETING"
                
            elif action == edit_tag:
                text = QInputDialog.getText(None, QString(tag_name),
                                         QString("Change the tag to:"),
                                         QLineEdit.Normal,
                                         item_now.text())
                
                if text[1]:
                    col = self.ui.playlisting.header_search("FileName")
                    fname = self.ui.track_tbl.item(row,col).text()
                    self.ui.media_db.update_tag(fname,tag_name.toLower(),text[0])
                    item_now.setText(text[0])
                

        
    def __time_filt_now(self):
        """
        Based on the combobox selection, the collection
        browser is filtered by addition date
        """
        index = self.ui.collect_time_box.currentIndex()
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
        media_db = self.ui.media_db
        self.ui.collect_tree.clear()
        # This gives multiples of the same thing i.e albums
        filt = self.ui.search_collect_edit.text()
        time_filt = self.__time_filt_now()
        
        text_now = self.ui.collect_tree.headerItem().text(0)
        if text_now == "Artist/Album":
            mode = "artist"
        else:
            mode = "album"
                
        if mode == "artist":
            things = media_db.get_artists(time_filt)
        elif mode == "album":
            things = media_db.get_albums_all(time_filt)
        
        if things is None:
            return
        
        for thing in things:
            # When creating collection tree only 
            #  allow certain things based on the filter.
            if (filt is not None) and (filt.toLower() not in thing.toLower()):
                continue
            thing = QTreeWidgetItem([thing])
            thing.setChildIndicatorPolicy(0)
            self.ui.collect_tree.addTopLevelItem(thing)
            
    def pop_playlist_view(self):
        """
        Populates the playlist listview
        """
        font = QFont()
        font.setBold(True)        
        self.ui.playlist_tree.clear()
        playlists = self.ui.media_db.playlist_list()
#        podcasts = None
#        streams = None
        hdr_names = ["Playlists"] # Podcasts Radio Streams
        headers = [QTreeWidgetItem(["%s" % tit]) for tit in hdr_names ]
        for hdr in headers:
            hdr.setFont(0, font)
            hdr.setChildIndicatorPolicy(2)
         
            if hdr.text(0) == "Playlists":
                for play in playlists:
                    # Ignore the auto-save playlist
                    if play == "!!##gereqi.remembered##!!":
                        continue
                    now = QTreeWidgetItem([QString(play)])
                    hdr.addChild(now)
                    tracks = self.ui.media_db.playlist_tracks(play)
                    for track in tracks:
                        info = self.ui.media_db.get_info(track)
                        if info is not None:
                            now.addChild(QTreeWidgetItem([QString("%s - %s" %
                                         (info["title"], info["artist"])) ]))       
                                                                                      
            self.ui.playlist_tree.addTopLevelItem(hdr)
                
    def icon_change(self, state):
        """
        Depending on the specific state of the program
        the play button's icon will vary
        """
        if state == "play":
            icon = QIcon().fromTheme("media-playback-pause")
            tray = QIcon(":/icons/app.png")
        elif state == "pause":            
            icon = QIcon().fromTheme("media-playback-start")
            tray = QIcon(":/icons/app-paused.png")

        self.ui.play_bttn.setIcon(icon)
        self.ui.tray_icon.setIcon(tray)
